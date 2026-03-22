#!/usr/bin/env python3
"""
game_detect — нода ROS2 для обнаружения и классификации игровых объектов.

Подписывается на топик /objects от find_object_2d и /aruco_objects,
вычисляет центр каждого объекта через гомографию,
проставляет состояние ("field"/"basket") и стоимость,
публикует результаты в /game_objects.

find_object_2d публикует в /objects сообщение типа std_msgs/Float32MultiArray:
  data = [objectId1, objectWidth1, objectHeight1, h00, h01, h02, h10, h11, h12, h20, h21, h22,
          objectId2, ...]
  Каждый объект занимает 12 значений: id, width, height, 9 элементов гомографии (3x3).
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from game_vision.msg import GameObject, GameObjectArray
import numpy as np

SKIP_FIND_OBJECT_IDS = {1, 2, 20, 21}  # find_object IDs, обрабатываемые через ArUco 20/21


class GameDetectNode(Node):
    def __init__(self):
        super().__init__('game_detect')

        # ====================================================================
        # ПОЛЬЗОВАТЕЛЬСКАЯ НАСТРОЙКА: ID объектов и стоимость
        # ID объектов укажите вручную в порядке таблицы.
        # ====================================================================
        self.object_costs = [
            # Белый куб с маркером 50*50*50 мм - id 20
            {"name": "white_cube_id20", "id": 1, "field": 1, "basket": 2},
            # Белый куб с маркером 50*50*50 мм - id 21
            {"name": "white_cube_id21", "id": 2, "field": -2, "basket": 4},
            # Красный куб 50*50*50 мм
            {"name": "red_cube_50", "id": 3, "field": -4, "basket": 4},
            # Синий куб 40*40*40 мм
            {"name": "blue_cube_40", "id": 4, "field": 2, "basket": 4},
            # Красный цилиндр 40мм (диаметр) * 50мм высота
            {"name": "red_cylinder_40x50", "id": 5, "field": 3, "basket": 6},
            # Пингвин голубой
            {"name": "blue_penguin", "id": 6, "field": -6, "basket": 6},
            # Осьминог красный
            {"name": "red_octopus", "id": 7, "field": 5, "basket": 10},
            # Кролик зелёный
            {"name": "green_rabbit", "id": 8, "field": 4, "basket": 8},
        ]

        self.get_logger().info(f'Object cost table: {self.object_costs}')

        self.find_object_objects = []
        self.aruco_objects = []

        # Подписка на топик /objects от find_object_2d
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/objects',
            self.objects_callback,
            10
        )

        # Подписка на центры ArUco-объектов (ID 20/21)
        self.aruco_subscription = self.create_subscription(
            GameObjectArray,
            '/aruco_objects',
            self.aruco_objects_callback,
            10
        )

        # Публикация обнаруженных объектов
        self.publisher = self.create_publisher(
            GameObjectArray,
            '/game_objects',
            10
        )

        self.get_logger().info('game_detect запущен. Ожидание данных из /objects...')

    def _get_cost(self, obj_id: int, state: str) -> int:
        for item in self.object_costs:
            if item["id"] == obj_id:
                return int(item[state])
        return 0

    def objects_callback(self, msg: Float32MultiArray):
        """
        Обработка данных из find_object_2d.
        Каждый объект = 12 float: [id, width, height, h00..h22]
        """
        data = msg.data
        if len(data) == 0:
            return

        VALUES_PER_OBJECT = 12
        num_objects = len(data) // VALUES_PER_OBJECT

        self.find_object_objects = []

        for i in range(num_objects):
            offset = i * VALUES_PER_OBJECT
            obj_id = int(data[offset])
            if obj_id in SKIP_FIND_OBJECT_IDS:
                continue
            obj_width = data[offset + 1]
            obj_height = data[offset + 2]

            # Матрица гомографии 3x3
            h = np.array([
                [data[offset + 3], data[offset + 4], data[offset + 5]],
                [data[offset + 6], data[offset + 7], data[offset + 8]],
                [data[offset + 9], data[offset + 10], data[offset + 11]]
            ], dtype=np.float64)

            # Вычисляем центр объекта в пикселях кадра камеры
            # Центр сохранённого изображения объекта
            center_src = np.array([obj_width / 2.0, obj_height / 2.0, 1.0])

            # Применяем гомографию: p_dst = H * p_src
            center_dst = h @ center_src
            if abs(center_dst[2]) < 1e-9:
                continue

            pixel_x = center_dst[0] / center_dst[2]
            pixel_y = center_dst[1] / center_dst[2]

            # Состояние и стоимость (по умолчанию: на поле)
            state = 'field'
            cost = self._get_cost(obj_id, state)

            go = self._build_game_object(obj_id, pixel_x, pixel_y, state)
            self.find_object_objects.append(go)

            self.get_logger().debug(
                f'Object id={obj_id} state={state} cost={cost} '
                f'pixel=({pixel_x:.1f}, {pixel_y:.1f})'
            )

        self._publish_combined_objects()

    def aruco_objects_callback(self, msg: GameObjectArray):
        self.aruco_objects = []
        for go in msg.objects:
            state = go.state if go.state else 'field'
            self.aruco_objects.append(
                self._build_game_object(go.object_id, go.pixel_x, go.pixel_y, state)
            )
        self._publish_combined_objects()

    def _build_game_object(self, obj_id: int, pixel_x: float, pixel_y: float, state: str) -> GameObject:
        cost = self._get_cost(obj_id, state)
        go = GameObject()
        go.object_id = obj_id
        go.state = state
        go.cost = int(cost)
        go.pixel_x = float(pixel_x)
        go.pixel_y = float(pixel_y)
        go.world_x = 0.0
        go.world_y = 0.0
        go.cell_row = -1
        go.cell_col = -1
        go.cell_id = -1
        go.localized = False
        return go

    def _publish_combined_objects(self):
        game_objects_msg = GameObjectArray()
        game_objects_msg.objects.extend(self.find_object_objects)
        game_objects_msg.objects.extend(self.aruco_objects)

        if game_objects_msg.objects:
            self.publisher.publish(game_objects_msg)
            self.get_logger().debug(
                f'Опубликовано {len(game_objects_msg.objects)} объектов в /game_objects'
            )


def main(args=None):
    rclpy.init(args=args)
    node = GameDetectNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
