#!/usr/bin/env python3
"""
aruco_mapping — нода ROS2 для работы с ArUco-картой.

Функции:
1. Создаёт словарь ArUco 4x4 маркеров, заполняет map_aruco[7][5] в шахматном порядке.
2. Вычисляет aruco_map_coords[7][5][2] — координаты центров всех клеток
   (чёрные клетки интерполируются по соседним маркерам).
3. Распознаёт ArUco 6x6 маркер на роботе, определяет его координаты.
4. Принимает данные из /game_objects, вычисляет мировые координаты через гомографию
   от ArUco маркеров, определяет клетку для каждого объекта.
5. Публикует маркеры в /visualization_marker_array для rviz.
6. Публикует обновлённые объекты с привязкой к клеткам в /game_objects_localized.
7. Публикует GameStatus с флагами игры.
8. Публикует центры ArUco-маркеров объектов в /aruco_objects.

Карта (из изображения):
  Строка 0: A1  [m]  A   [m]  A3     (верх, сторона A)
  Строка 1: [m]  _   [m]  A2  [m]
  Строка 2:  _  [m]   _   [m]  _
  Строка 3: [m]  C1  [m]  C2  [m]    (середина)
  Строка 4:  _  [m]   _   [m]  _
  Строка 5: [m]  _   [m]  B2  [m]
  Строка 6: B1  [m]  B   [m]  B3     (низ, сторона B)

Шахматный порядок: строка 0 начинается 0,1,0,1,0
  0 = чёрная клетка (без маркера)
  1 = белая клетка (ArUco маркер)

Размер клетки: 250×250 мм
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from game_vision.msg import GameObject, GameObjectArray, GameStatus
from cv_bridge import CvBridge
import cv2
import numpy as np
import cv2.aruco as aruco

# ============================================================================
# КОНФИГУРАЦИЯ КАРТЫ
# ============================================================================
ROWS = 7
COLS = 5
CELL_SIZE_MM = 250.0  # Размер клетки и маркера в мм

# IDs ArUco, которые принадлежат игровым объектам, а не карте
ARUCO_OBJECT_ID_MAP = {
    20: 1,  # Белый куб с маркером 20 -> object_id=1
    21: 2,  # Белый куб с маркером 21 -> object_id=2
}
ARUCO_OBJECT_MARKER_IDS = set(ARUCO_OBJECT_ID_MAP.keys())
SKIP_MARKER_IDS = set(ARUCO_OBJECT_MARKER_IDS)

# Шахматный порядок: 0 — чёрная (нет маркера), 1 — белая (есть маркер)
# Строка 0 начинается с 0: [0, 1, 0, 1, 0]
CHESS_PATTERN = []
for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append((r + c) % 2)  # 0 для чётной суммы, 1 для нечётной
    CHESS_PATTERN.append(row)
# Результат:
# Row 0: [0, 1, 0, 1, 0]  — чёрн, маркер, чёрн, маркер, чёрн
# Row 1: [1, 0, 1, 0, 1]  — маркер, чёрн, маркер, чёрн, маркер
# Row 2: [0, 1, 0, 1, 0]
# Row 3: [1, 0, 1, 0, 1]
# Row 4: [0, 1, 0, 1, 0]
# Row 5: [1, 0, 1, 0, 1]
# Row 6: [0, 1, 0, 1, 0]


class ArucoMappingNode(Node):
    def __init__(self):
        super().__init__('aruco_mapping')

        self.calib_loaded = False
        self.map1 = None
        self.map2 = None
        self.use_undistort = True
        self.load_calibration("camera_calib.yml")

        self.last_ids_4x4 = set()

        self.bridge = CvBridge()

        # ====================================================================
        # ArUco словари
        # ====================================================================
        # 4x4 — маркеры на карте (на белых клетках)
        self.aruco_dict_4x4 = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
        self.aruco_params_4x4 = aruco.DetectorParameters()

        # 6x6 — маркер на роботе
        self.aruco_dict_6x6 = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        self.aruco_params_6x6 = aruco.DetectorParameters()

        # ====================================================================
        # Карта ArUco маркеров: map_aruco[row][col]
        # 0 = чёрная клетка (нет маркера), >0 = ID маркера
        # ID маркеров назначаются последовательно при обнаружении
        # ====================================================================
        self.map_aruco = [[0] * COLS for _ in range(ROWS)]

        # Координаты центров клеток в мировой СК (мм)
        # aruco_map_coords[row][col] = (x_mm, y_mm)
        self.aruco_map_coords = [[(0.0, 0.0)] * COLS for _ in range(ROWS)]

        # Заполняем идеальные координаты центров
        # Начало координат — левый нижний угол карты
        for r in range(ROWS):
            for c in range(COLS):
                cx = c * CELL_SIZE_MM + CELL_SIZE_MM / 2.0  # мм
                cy = (ROWS - 1 - r) * CELL_SIZE_MM + CELL_SIZE_MM / 2.0  # мм
                self.aruco_map_coords[r][c] = (cx, cy)

        # Словарь: aruco_id (4x4) -> (row, col) на карте
        # Заполняется при первом обнаружении маркеров
        self.aruco_id_to_cell = {}

        # Гомография: пиксели камеры -> мировые координаты (мм)
        self.homography = None
        self.homography_valid = False

        # Параметры камеры (для undistort, если понадобится)
        self.camera_matrix = None
        self.dist_coeffs = None

        # Данные робота
        self.robot_aruco_id = -1
        self.robot_pixel = (0.0, 0.0)
        self.robot_world = (0.0, 0.0)
        self.robot_cell = (-1, -1)

        # Флаги игры
        self.game_started = False
        self.robot_side = 'unknown'

        # Последние game_objects из game_detect
        self.current_game_objects = []
        self.localized_game_objects = []

        # ====================================================================
        # Подписки
        # ====================================================================
        self.sub_image = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10
        )
        self.sub_camera_info = self.create_subscription(
            CameraInfo, '/camera/camera_info', self.camera_info_callback, 10
        )
        self.sub_game_objects = self.create_subscription(
            GameObjectArray, '/game_objects', self.game_objects_callback, 10
        )

        # ====================================================================
        # Публикации
        # ====================================================================
        self.pub_markers = self.create_publisher(
            MarkerArray, '/visualization_marker_array', 10
        )
        self.pub_localized = self.create_publisher(
            GameObjectArray, '/game_objects_localized', 10
        )
        self.pub_status = self.create_publisher(
            GameStatus, '/game_status', 10
        )
        self.pub_debug_image = self.create_publisher(
            Image, '/aruco_debug_image', 10
        )
        self.pub_aruco_objects = self.create_publisher(
            GameObjectArray, '/aruco_objects', 10
        )

        # Таймер для публикации визуализации (10 Hz)
        self.timer = self.create_timer(0.1, self.publish_visualization)

        self.get_logger().info('aruco_mapping запущен.')
        self.get_logger().info(f'Шахматный порядок карты ({ROWS}x{COLS}):')
        for r in range(ROWS):
            self.get_logger().info(f'  Row {r}: {CHESS_PATTERN[r]}')

    # ========================================================================
    # Callback: параметры камеры
    # ========================================================================
    def camera_info_callback(self, msg: CameraInfo):
        if self.camera_matrix is None:
            self.camera_matrix = np.array(msg.k).reshape(3, 3)
            self.dist_coeffs = np.array(msg.d)
            self.get_logger().info('Параметры камеры получены.')

    # ========================================================================
    # Callback: game_objects от game_detect
    # ========================================================================
    def game_objects_callback(self, msg: GameObjectArray):
        self.current_game_objects = list(msg.objects)

    # ========================================================================
    # Callback: обработка кадра камеры
    # ========================================================================
    def image_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        if self.use_undistort and self.calib_loaded and self.map1 is not None:
            frame = cv2.remap(frame, self.map1, self.map2, interpolation=cv2.INTER_LINEAR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ---- Обнаружение маркеров 4x4 (карта) ----
        corners_4x4, ids_4x4, _ = aruco.detectMarkers(
            gray, self.aruco_dict_4x4, parameters=self.aruco_params_4x4
        )

        if ids_4x4 is not None:
            self.last_ids_4x4 = set(int(x) for x in ids_4x4.flatten())
        else:
            self.last_ids_4x4 = set()

        self._publish_aruco_object_centers(corners_4x4, ids_4x4)

        # ---- Обнаружение маркеров 6x6 (робот) ----
        corners_6x6, ids_6x6, _ = aruco.detectMarkers(
            gray, self.aruco_dict_6x6, parameters=self.aruco_params_6x6
        )

        # ---- Обновляем гомографию по маркерам 4x4 ----
        if ids_4x4 is not None and len(ids_4x4) >= 4:
            self._update_homography(corners_4x4, ids_4x4)

        # ---- Обрабатываем маркер робота (6x6) ----
        if ids_6x6 is not None and len(ids_6x6) > 0:
            self._process_robot_marker(corners_6x6, ids_6x6)

        # ---- Локализуем game_objects ----
        if self.homography_valid and self.current_game_objects:
            self._localize_game_objects()

        # ---- Проверяем флаг игры ----
        self._check_game_flags()

        # ---- Debug image ----
        debug_frame = frame.copy()
        if ids_4x4 is not None:
            aruco.drawDetectedMarkers(debug_frame, corners_4x4, ids_4x4)
        if ids_6x6 is not None:
            aruco.drawDetectedMarkers(debug_frame, corners_6x6, ids_6x6)

        self._draw_map_centers(debug_frame)

        debug_msg = self.bridge.cv2_to_imgmsg(debug_frame, encoding='bgr8')
        self.pub_debug_image.publish(debug_msg)

    # ========================================================================
    # Построение гомографии: пиксели -> мировые координаты
    # ========================================================================
    def _update_homography(self, corners_4x4, ids_4x4):
        """
        На основе обнаруженных ArUco 4x4 маркеров строим гомографию
        pixel -> world (мм).

        Маркеры находятся на белых клетках шахматной доски.
        При первом обнаружении назначаем каждому маркеру позицию на карте.
        """
        pts_pixel = []
        pts_world = []

        for i, marker_id in enumerate(ids_4x4.flatten()):
            marker_id = int(marker_id)

            if marker_id in SKIP_MARKER_IDS:
                continue

            # Центр маркера в пикселях
            c = corners_4x4[i][0]
            cx_px = float(np.mean(c[:, 0]))
            cy_px = float(np.mean(c[:, 1]))

            if marker_id in self.aruco_id_to_cell:
                row, col = self.aruco_id_to_cell[marker_id]
            else:
                row, col = self._assign_marker_to_cell(cx_px, cy_px, marker_id)
                if row < 0:
                    continue

            world_x, world_y = self.aruco_map_coords[row][col]
            pts_pixel.append([cx_px, cy_px])
            pts_world.append([world_x, world_y])

        if len(pts_pixel) >= 4:
            pts_pixel = np.array(pts_pixel, dtype=np.float64)
            pts_world = np.array(pts_world, dtype=np.float64)
            H, status = cv2.findHomography(pts_pixel, pts_world, cv2.RANSAC, 5.0)
            if H is not None:
                self.homography = H
                self.homography_valid = True

        # Обновляем координаты чёрных клеток (интерполяция по соседям)
        self._interpolate_black_cells()

    def _assign_marker_to_cell(self, cx_px, cy_px, marker_id):
        """
        Назначает маркер на ближайшую свободную белую клетку.
        Для продакшена лучше задать маппинг ID->клетка в конфигурации.
        """
        if marker_id in SKIP_MARKER_IDS:
            return (-1, -1)

        if not self.homography_valid:
            # Без гомографии назначаем последовательно
            # по списку белых клеток
            white_cells = []
            for r in range(ROWS):
                for c in range(COLS):
                    if CHESS_PATTERN[r][c] == 1:
                        white_cells.append((r, c))

            assigned = set(self.aruco_id_to_cell.values())
            for cell in white_cells:
                if cell not in assigned:
                    self.aruco_id_to_cell[marker_id] = cell
                    self.map_aruco[cell[0]][cell[1]] = marker_id
                    self.get_logger().info(
                        f'Маркер ID={marker_id} назначен на клетку [{cell[0]}][{cell[1]}]'
                    )
                    return cell
            return (-1, -1)
        else:
            # С гомографией — находим ближайшую белую клетку
            world_pt = self._pixel_to_world(cx_px, cy_px)
            if world_pt is None:
                return (-1, -1)

            best_dist = float('inf')
            best_cell = (-1, -1)
            assigned = set(self.aruco_id_to_cell.values())

            for r in range(ROWS):
                for c in range(COLS):
                    if CHESS_PATTERN[r][c] == 1 and (r, c) not in assigned:
                        wx, wy = self.aruco_map_coords[r][c]
                        dist = (world_pt[0] - wx) ** 2 + (world_pt[1] - wy) ** 2
                        if dist < best_dist:
                            best_dist = dist
                            best_cell = (r, c)

            if best_cell[0] >= 0:
                self.aruco_id_to_cell[marker_id] = best_cell
                self.map_aruco[best_cell[0]][best_cell[1]] = marker_id
                self.get_logger().info(
                    f'Маркер ID={marker_id} назначен на клетку '
                    f'[{best_cell[0]}][{best_cell[1]}]'
                )
            return best_cell

    def _interpolate_black_cells(self):
        """
        Вычисляет координаты центров чёрных клеток
        по 2 соседним ArUco маркерам (горизонтальным соседям).
        Если горизонтальных нет — берём вертикальных.
        """
        for r in range(ROWS):
            for c in range(COLS):
                if CHESS_PATTERN[r][c] == 0:
                    # Чёрная клетка — интерполируем
                    neighbors = []

                    # Левый сосед
                    if c > 0 and CHESS_PATTERN[r][c - 1] == 1:
                        neighbors.append(self.aruco_map_coords[r][c - 1])
                    # Правый сосед
                    if c < COLS - 1 and CHESS_PATTERN[r][c + 1] == 1:
                        neighbors.append(self.aruco_map_coords[r][c + 1])
                    # Верхний сосед
                    if r > 0 and CHESS_PATTERN[r - 1][c] == 1:
                        neighbors.append(self.aruco_map_coords[r - 1][c])
                    # Нижний сосед
                    if r < ROWS - 1 and CHESS_PATTERN[r + 1][c] == 1:
                        neighbors.append(self.aruco_map_coords[r + 1][c])

                    if len(neighbors) >= 2:
                        avg_x = sum(n[0] for n in neighbors) / len(neighbors)
                        avg_y = sum(n[1] for n in neighbors) / len(neighbors)
                        self.aruco_map_coords[r][c] = (avg_x, avg_y)

    # ========================================================================
    # Обработка маркера робота (6x6)
    # ========================================================================
    def _process_robot_marker(self, corners_6x6, ids_6x6):
        """Находит маркер 6x6 на роботе, определяет его координаты."""
        # Берём первый найденный 6x6 маркер
        idx = 0
        self.robot_aruco_id = int(ids_6x6[idx][0])

        c = corners_6x6[idx][0]
        cx_px = float(np.mean(c[:, 0]))
        cy_px = float(np.mean(c[:, 1]))
        self.robot_pixel = (cx_px, cy_px)

        # Вычисляем мировые координаты
        if self.homography_valid:
            world_pt = self._pixel_to_world(cx_px, cy_px)
            if world_pt is not None:
                self.robot_world = (world_pt[0], world_pt[1])
                # Определяем клетку робота
                self.robot_cell = self._find_cell(world_pt[0], world_pt[1])

    # ========================================================================
    # Обработка ArUco-маркеров на объектах (ID 20/21)
    # ========================================================================
    def _publish_aruco_object_centers(self, corners_4x4, ids_4x4):
        """Публикует центры ArUco-маркеров объектов в /aruco_objects."""
        aruco_objects_msg = GameObjectArray()

        if ids_4x4 is not None:
            for i, marker_id in enumerate(ids_4x4.flatten()):
                marker_id = int(marker_id)
                if marker_id not in ARUCO_OBJECT_ID_MAP:
                    continue

                c = corners_4x4[i][0]
                cx_px = float(np.mean(c[:, 0]))
                cy_px = float(np.mean(c[:, 1]))

                go = GameObject()
                go.object_id = ARUCO_OBJECT_ID_MAP[marker_id]
                go.state = 'field'
                go.cost = 0
                go.pixel_x = cx_px
                go.pixel_y = cy_px
                go.world_x = 0.0
                go.world_y = 0.0
                go.cell_row = -1
                go.cell_col = -1
                go.cell_id = -1
                go.localized = False

                aruco_objects_msg.objects.append(go)

        self.pub_aruco_objects.publish(aruco_objects_msg)

    def _draw_map_centers(self, debug_frame):
        """Рисует красные точки — центры карты, проецированные в пиксели."""
        if not self.homography_valid or self.homography is None:
            return

        try:
            homography_inv = np.linalg.inv(self.homography)
        except np.linalg.LinAlgError:
            return

        height, width = debug_frame.shape[:2]
        for r in range(ROWS):
            for c in range(COLS):
                wx, wy = self.aruco_map_coords[r][c]
                pt_world = np.array([wx, wy, 1.0], dtype=np.float64)
                pt_pixel = homography_inv @ pt_world
                if abs(pt_pixel[2]) < 1e-9:
                    continue
                px = pt_pixel[0] / pt_pixel[2]
                py = pt_pixel[1] / pt_pixel[2]
                if 0 <= px < width and 0 <= py < height:
                    cv2.circle(
                        debug_frame,
                        (int(round(px)), int(round(py))),
                        4,
                        (0, 0, 255),
                        -1
                    )

    # ========================================================================
    # Локализация game_objects
    # ========================================================================
    def _localize_game_objects(self):
        """
        Для каждого game_object вычисляет мировые координаты и клетку.
        Публикует обновлённые данные.
        """
        localized_msg = GameObjectArray()

        for go in self.current_game_objects:
            new_go = GameObject()
            new_go.object_id = go.object_id
            new_go.quality = go.quality
            new_go.pixel_x = go.pixel_x
            new_go.pixel_y = go.pixel_y

            world_pt = self._pixel_to_world(go.pixel_x, go.pixel_y)
            if world_pt is not None:
                new_go.world_x = world_pt[0]
                new_go.world_y = world_pt[1]
                row, col = self._find_cell(world_pt[0], world_pt[1])
                new_go.cell_row = row
                new_go.cell_col = col
                if 0 <= row < ROWS and 0 <= col < COLS:
                    new_go.cell_id = self.map_aruco[row][col]
                else:
                    new_go.cell_id = -1
                new_go.localized = True
            else:
                new_go.world_x = 0.0
                new_go.world_y = 0.0
                new_go.cell_row = -1
                new_go.cell_col = -1
                new_go.cell_id = -1
                new_go.localized = False

            localized_msg.objects.append(new_go)

        self.pub_localized.publish(localized_msg)
        self.localized_game_objects = list(localized_msg.objects)

    # ========================================================================
    # Флаги игры
    # ========================================================================
    def _check_game_flags(self):
        """
        Флаг game_started: true когда найден центральный маркер [3][2].
        Флаг robot_side: "A" если робот в верхней половине (строки 0-2),
                         "B" если в нижней (строки 4-6),
                         "center" если в строке 3.
        """
        # Проверяем: есть ли маркер в клетке [3][2]?
        center_marker_id = self.map_aruco[3][2]
        if center_marker_id > 0 and center_marker_id in self.last_ids_4x4:
            self.game_started = True  # change game_started logic
        # Keep other logic unchanged

        # Определяем сторону робота
        if self.robot_cell[0] >= 0:
            if self.robot_cell[0] <= 2:
                self.robot_side = 'A'
            elif self.robot_cell[0] >= 4:
                self.robot_side = 'B'
            else:
                self.robot_side = 'center'

        # Публикуем статус
        status = GameStatus()
        status.game_started = self.game_started
        status.robot_side = self.robot_side
        status.robot_pixel_x = self.robot_pixel[0]
        status.robot_pixel_y = self.robot_pixel[1]
        status.robot_world_x = self.robot_world[0]
        status.robot_world_y = self.robot_world[1]
        status.robot_cell_row = self.robot_cell[0]
        status.robot_cell_col = self.robot_cell[1]
        status.robot_aruco_id = max(0, self.robot_aruco_id)
        self.pub_status.publish(status)

    # ========================================================================
    # Визуализация в rviz
    # ========================================================================
    def publish_visualization(self):
        """Публикует маркеры для rviz: сетку карты, объекты, робота."""
        marker_array = MarkerArray()
        marker_id = 0

        object_cells = {
            (go.cell_row, go.cell_col)
            for go in self.localized_game_objects
            if go.localized and 0 <= go.cell_row < ROWS and 0 <= go.cell_col < COLS
        }

        # ---- Сетка карты (квадраты) ----
        for r in range(ROWS):
            for c in range(COLS):
                marker = Marker()
                marker.header.frame_id = 'map'
                marker.header.stamp = self.get_clock().now().to_msg()
                marker.ns = 'grid'
                marker.id = marker_id
                marker_id += 1
                marker.type = Marker.CUBE
                marker.action = Marker.ADD

                wx, wy = self.aruco_map_coords[r][c]
                marker.pose.position.x = wx / 1000.0  # мм -> м
                marker.pose.position.y = wy / 1000.0
                marker.pose.position.z = 0.0
                marker.pose.orientation.w = 1.0

                marker.scale.x = CELL_SIZE_MM / 1000.0
                marker.scale.y = CELL_SIZE_MM / 1000.0
                marker.scale.z = 0.005  # тонкая плоскость

                if (r, c) in object_cells:
                    marker.color = ColorRGBA(r=0.0, g=0.0, b=1.0, a=0.8)
                elif CHESS_PATTERN[r][c] == 1:
                    # Белая клетка (маркер)
                    marker.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=0.8)
                else:
                    # Чёрная клетка
                    marker.color = ColorRGBA(r=0.1, g=0.1, b=0.1, a=0.8)

                marker_array.markers.append(marker)

                # Текст с номером клетки
                text_marker = Marker()
                text_marker.header.frame_id = 'map'
                text_marker.header.stamp = self.get_clock().now().to_msg()
                text_marker.ns = 'grid_labels'
                text_marker.id = marker_id
                marker_id += 1
                text_marker.type = Marker.TEXT_VIEW_FACING
                text_marker.action = Marker.ADD
                text_marker.pose.position.x = wx / 1000.0
                text_marker.pose.position.y = wy / 1000.0
                text_marker.pose.position.z = 0.02
                text_marker.pose.orientation.w = 1.0
                text_marker.scale.z = 0.05
                text_marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0)

                cell_label = f'[{r},{c}]'
                if self.map_aruco[r][c] > 0:
                    cell_label += f'\nID:{self.map_aruco[r][c]}'
                text_marker.text = cell_label
                marker_array.markers.append(text_marker)

        # ---- Центры карты (сферы), показываем только при видимой карте ----
        if self.homography_valid and len(self.last_ids_4x4) > 0:
            for r in range(ROWS):
                for c in range(COLS):
                    center_marker = Marker()
                    center_marker.header.frame_id = 'map'
                    center_marker.header.stamp = self.get_clock().now().to_msg()
                    center_marker.ns = 'grid_centers'
                    center_marker.id = marker_id
                    marker_id += 1
                    center_marker.type = Marker.SPHERE
                    center_marker.action = Marker.ADD

                    wx, wy = self.aruco_map_coords[r][c]
                    center_marker.pose.position.x = wx / 1000.0
                    center_marker.pose.position.y = wy / 1000.0
                    center_marker.pose.position.z = 0.02
                    center_marker.pose.orientation.w = 1.0

                    center_marker.scale.x = 0.03
                    center_marker.scale.y = 0.03
                    center_marker.scale.z = 0.03
                    center_marker.color = ColorRGBA(r=0.0, g=1.0, b=1.0, a=0.9)

                    marker_array.markers.append(center_marker)

        # ---- ID видимых ArUco маркеров ----
        for marker_id_value in sorted(self.last_ids_4x4):
            if marker_id_value in self.aruco_id_to_cell:
                row, col = self.aruco_id_to_cell[marker_id_value]
                wx, wy = self.aruco_map_coords[row][col]

                id_marker = Marker()
                id_marker.header.frame_id = 'map'
                id_marker.header.stamp = self.get_clock().now().to_msg()
                id_marker.ns = 'visible_aruco_ids'
                id_marker.id = marker_id
                marker_id += 1
                id_marker.type = Marker.TEXT_VIEW_FACING
                id_marker.action = Marker.ADD
                id_marker.pose.position.x = wx / 1000.0
                id_marker.pose.position.y = wy / 1000.0
                id_marker.pose.position.z = 0.08
                id_marker.pose.orientation.w = 1.0
                id_marker.scale.z = 0.06
                id_marker.color = ColorRGBA(r=0.0, g=1.0, b=1.0, a=1.0)
                id_marker.text = f'ID:{marker_id_value}'

                marker_array.markers.append(id_marker)

        # ---- Маркер робота ----
        if self.robot_aruco_id >= 0:
            robot_marker = Marker()
            robot_marker.header.frame_id = 'map'
            robot_marker.header.stamp = self.get_clock().now().to_msg()
            robot_marker.ns = 'robot'
            robot_marker.id = marker_id
            marker_id += 1
            robot_marker.type = Marker.CYLINDER
            robot_marker.action = Marker.ADD
            robot_marker.pose.position.x = self.robot_world[0] / 1000.0
            robot_marker.pose.position.y = self.robot_world[1] / 1000.0
            robot_marker.pose.position.z = 0.05
            robot_marker.pose.orientation.w = 1.0
            robot_marker.scale.x = 0.1
            robot_marker.scale.y = 0.1
            robot_marker.scale.z = 0.1
            robot_marker.color = ColorRGBA(r=0.0, g=0.0, b=1.0, a=0.9)
            marker_array.markers.append(robot_marker)

            # Текст робота
            robot_text = Marker()
            robot_text.header.frame_id = 'map'
            robot_text.header.stamp = self.get_clock().now().to_msg()
            robot_text.ns = 'robot_label'
            robot_text.id = marker_id
            marker_id += 1
            robot_text.type = Marker.TEXT_VIEW_FACING
            robot_text.action = Marker.ADD
            robot_text.pose.position.x = self.robot_world[0] / 1000.0
            robot_text.pose.position.y = self.robot_world[1] / 1000.0
            robot_text.pose.position.z = 0.15
            robot_text.pose.orientation.w = 1.0
            robot_text.scale.z = 0.06
            robot_text.color = ColorRGBA(r=0.0, g=1.0, b=1.0, a=1.0)
            robot_text.text = (
                f'Robot ID:{self.robot_aruco_id}\n'
                f'Side: {self.robot_side}\n'
                f'Cell: [{self.robot_cell[0]},{self.robot_cell[1]}]'
            )
            marker_array.markers.append(robot_text)

        # ---- Объекты ----
        for go in self.localized_game_objects:
            if not go.localized:
                continue

            obj_marker = Marker()
            obj_marker.header.frame_id = 'map'
            obj_marker.header.stamp = self.get_clock().now().to_msg()
            obj_marker.ns = 'game_objects'
            obj_marker.id = marker_id
            marker_id += 1
            obj_marker.type = Marker.SPHERE
            obj_marker.action = Marker.ADD
            obj_marker.pose.position.x = go.world_x / 1000.0
            obj_marker.pose.position.y = go.world_y / 1000.0
            obj_marker.pose.position.z = 0.05
            obj_marker.pose.orientation.w = 1.0
            obj_marker.scale.x = 0.08
            obj_marker.scale.y = 0.08
            obj_marker.scale.z = 0.08

            # Цвет по качеству
            if go.quality == 'good':
                obj_marker.color = ColorRGBA(r=0.0, g=1.0, b=0.0, a=0.9)
            elif go.quality == 'normal':
                obj_marker.color = ColorRGBA(r=1.0, g=1.0, b=0.0, a=0.9)
            elif go.quality == 'bad':
                obj_marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=0.9)
            else:
                obj_marker.color = ColorRGBA(r=0.5, g=0.5, b=0.5, a=0.9)

            marker_array.markers.append(obj_marker)

            # Текст с ID объекта
            obj_text = Marker()
            obj_text.header.frame_id = 'map'
            obj_text.header.stamp = self.get_clock().now().to_msg()
            obj_text.ns = 'game_object_ids'
            obj_text.id = marker_id
            marker_id += 1
            obj_text.type = Marker.TEXT_VIEW_FACING
            obj_text.action = Marker.ADD
            obj_text.pose.position.x = go.world_x / 1000.0
            obj_text.pose.position.y = go.world_y / 1000.0
            obj_text.pose.position.z = 0.12
            obj_text.pose.orientation.w = 1.0
            obj_text.scale.z = 0.06
            obj_text.color = ColorRGBA(r=1.0, g=1.0, b=1.0, a=1.0)
            obj_text.text = f'ID:{go.object_id}'

            marker_array.markers.append(obj_text)

        # ---- Линии разделения: A / B ----
        divider = Marker()
        divider.header.frame_id = 'map'
        divider.header.stamp = self.get_clock().now().to_msg()
        divider.ns = 'divider'
        divider.id = marker_id
        marker_id += 1
        divider.type = Marker.LINE_STRIP
        divider.action = Marker.ADD
        divider.scale.x = 0.01
        divider.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0)

        if 0 <= 3 < ROWS and 0 <= 4 < ROWS:
            y_div_mm = (self.aruco_map_coords[3][0][1] + self.aruco_map_coords[4][0][1]) / 2.0
            y_div = y_div_mm / 1000.0
        else:
            y_div = 3.5 * CELL_SIZE_MM / 1000.0  # между строками 3 и 4
        p1 = Point()
        p1.x = 0.0
        p1.y = y_div
        p1.z = 0.01
        p2 = Point()
        p2.x = COLS * CELL_SIZE_MM / 1000.0
        p2.y = y_div
        p2.z = 0.01
        divider.points = [p1, p2]
        marker_array.markers.append(divider)

        # Метки A и B
        label_rows = {'A': 1, 'B': 5}
        for label, row in label_rows.items():
            y_pos = self.aruco_map_coords[row][0][1] / 1000.0
            lm = Marker()
            lm.header.frame_id = 'map'
            lm.header.stamp = self.get_clock().now().to_msg()
            lm.ns = 'side_labels'
            lm.id = marker_id
            marker_id += 1
            lm.type = Marker.TEXT_VIEW_FACING
            lm.action = Marker.ADD
            lm.pose.position.x = -0.1
            lm.pose.position.y = y_pos
            lm.pose.position.z = 0.1
            lm.pose.orientation.w = 1.0
            lm.scale.z = 0.15
            lm.color = ColorRGBA(r=1.0, g=1.0, b=0.0, a=1.0)
            lm.text = label
            marker_array.markers.append(lm)

        self.pub_markers.publish(marker_array)

    # ========================================================================
    # Вспомогательные функции
    # ========================================================================
    def _pixel_to_world(self, px, py):
        """Преобразование пикселей в мировые координаты через гомографию."""
        if not self.homography_valid or self.homography is None:
            return None
        pt = np.array([px, py, 1.0], dtype=np.float64)
        result = self.homography @ pt
        if abs(result[2]) < 1e-9:
            return None
        return (result[0] / result[2], result[1] / result[2])

    def _find_cell(self, world_x, world_y):
        """Определяет клетку (row, col) по мировым координатам (мм)."""
        col = int(world_x / CELL_SIZE_MM)
        row = ROWS - 1 - int(world_y / CELL_SIZE_MM)
        col = max(0, min(col, COLS - 1))
        row = max(0, min(row, ROWS - 1))
        return (row, col)

    def load_calibration(self, path):
        fs = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
        if not fs.isOpened():
            self.get_logger().warn(f"Calibration file not found: {path}")
            return
        K = fs.getNode("camera_matrix").mat()
        D = fs.getNode("dist_coeffs").mat()
        w = int(fs.getNode("image_width").real())
        h = int(fs.getNode("image_height").real())
        fs.release()

        self.camera_matrix = K
        self.dist_coeffs = D
        self.map1, self.map2 = cv2.initUndistortRectifyMap(
            K, D, None, K, (w, h), cv2.CV_16SC2
        )
        self.calib_loaded = True
        self.get_logger().info("Camera calibration loaded")


def main(args=None):
    rclpy.init(args=args)
    node = ArucoMappingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
