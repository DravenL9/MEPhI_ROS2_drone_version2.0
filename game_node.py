#!/usr/bin/env python3
"""
game_node — нода игры ROS2.

Функции:
1. Подписывается на /game_status (от aruco_mapping) и /game_objects_localized.
2. Отслеживает флаг начала игры (game_started) — true когда
   найден центральный ArUco маркер в клетке [3][2].
3. Определяет на какой стороне (A — верхняя, B — нижняя) находится робот.
4. Ведёт учёт объектов на поле, их качества и позиций.
5. Публикует текущее состояние игры в /game_state_info (для отладки).
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from game_vision.msg import GameObjectArray, GameStatus


class GameNode(Node):
    def __init__(self):
        super().__init__('game_node')

        # ====================================================================
        # Состояние игры
        # ====================================================================
        self.game_started = False
        self.robot_side = 'unknown'
        self.robot_cell = (-1, -1)
        self.robot_world = (0.0, 0.0)
        self.robot_aruco_id = 0

        # Объекты на поле: {object_id: GameObject}
        self.field_objects = {}

        # Счёт / статистика
        self.objects_collected = {'good': 0, 'normal': 0, 'bad': 0}

        # ====================================================================
        # Подписки
        # ====================================================================
        self.sub_status = self.create_subscription(
            GameStatus, '/game_status', self.status_callback, 10
        )
        self.sub_objects = self.create_subscription(
            GameObjectArray, '/game_objects_localized', self.objects_callback, 10
        )

        # ====================================================================
        # Публикации
        # ====================================================================
        self.pub_info = self.create_publisher(
            String, '/game_state_info', 10
        )

        # Таймер для вывода состояния (1 Hz)
        self.timer = self.create_timer(1.0, self.publish_state)

        self.get_logger().info('game_node запущен. Ожидание начала игры...')

    # ========================================================================
    # Callbacks
    # ========================================================================
    def status_callback(self, msg: GameStatus):
        """Обработка статуса от aruco_mapping."""
        prev_started = self.game_started
        self.game_started = msg.game_started
        self.robot_side = msg.robot_side
        self.robot_cell = (msg.robot_cell_row, msg.robot_cell_col)
        self.robot_world = (msg.robot_world_x, msg.robot_world_y)
        self.robot_aruco_id = msg.robot_aruco_id

        if not prev_started and self.game_started:
            self.get_logger().info(
                '========================================\n'
                '  ИГРА НАЧАЛАСЬ!\n'
                '  Центральный маркер [3][2] найден.\n'
                '========================================'
            )

        if self.game_started:
            if self.robot_side == 'A':
                side_desc = 'Сторона A (верхняя половина)'
            elif self.robot_side == 'B':
                side_desc = 'Сторона B (нижняя половина)'
            elif self.robot_side == 'center':
                side_desc = 'Центр (строка 3)'
            else:
                side_desc = 'Не определена'

            self.get_logger().debug(
                f'Робот: сторона={side_desc}, '
                f'клетка=[{self.robot_cell[0]},{self.robot_cell[1]}], '
                f'ArUco ID={self.robot_aruco_id}'
            )

    def objects_callback(self, msg: GameObjectArray):
        """Обработка локализованных объектов."""
        if not self.game_started:
            return

        self.field_objects.clear()
        for go in msg.objects:
            self.field_objects[go.object_id] = {
                'quality': go.quality,
                'pixel': (go.pixel_x, go.pixel_y),
                'world': (go.world_x, go.world_y),
                'cell': (go.cell_row, go.cell_col),
                'cell_id': go.cell_id,
                'localized': go.localized,
            }

    # ========================================================================
    # Публикация состояния (для отладки и мониторинга)
    # ========================================================================
    def publish_state(self):
        """Публикует текстовое описание состояния игры."""
        info = String()

        lines = []
        lines.append('=' * 50)
        lines.append(f'ИГРА: {"АКТИВНА" if self.game_started else "НЕ НАЧАТА"}')

        if self.game_started:
            lines.append(f'Робот: сторона={self.robot_side}, '
                         f'клетка=[{self.robot_cell[0]},{self.robot_cell[1]}], '
                         f'мир=({self.robot_world[0]:.1f}, {self.robot_world[1]:.1f}) мм')
            lines.append(f'Объектов на поле: {len(self.field_objects)}')

            for oid, data in self.field_objects.items():
                loc_str = ''
                if data['localized']:
                    loc_str = (f'клетка=[{data["cell"][0]},{data["cell"][1]}], '
                               f'мир=({data["world"][0]:.1f}, {data["world"][1]:.1f}) мм')
                else:
                    loc_str = 'не локализован'
                lines.append(
                    f'  ID={oid}: качество={data["quality"]}, {loc_str}'
                )

            # Объекты по сторонам
            a_objects = [oid for oid, d in self.field_objects.items()
                         if d['localized'] and 0 <= d['cell'][0] <= 2]
            b_objects = [oid for oid, d in self.field_objects.items()
                         if d['localized'] and 4 <= d['cell'][0] <= 6]
            center_objects = [oid for oid, d in self.field_objects.items()
                              if d['localized'] and d['cell'][0] == 3]

            lines.append(f'Объектов на стороне A: {len(a_objects)}')
            lines.append(f'Объектов на стороне B: {len(b_objects)}')
            lines.append(f'Объектов в центре: {len(center_objects)}')

        lines.append('=' * 50)
        info.data = '\n'.join(lines)
        self.pub_info.publish(info)

        # Также в лог (раз в секунду)
        if self.game_started:
            self.get_logger().info(info.data)

    # ========================================================================
    # API для расширения: методы которые можно вызвать из внешнего кода
    # ========================================================================
    def get_objects_by_quality(self, quality: str) -> list:
        """Возвращает список объектов заданного качества."""
        return [
            (oid, data) for oid, data in self.field_objects.items()
            if data['quality'] == quality
        ]

    def get_objects_on_side(self, side: str) -> list:
        """Возвращает объекты на стороне 'A' или 'B'."""
        if side == 'A':
            return [(oid, d) for oid, d in self.field_objects.items()
                    if d['localized'] and 0 <= d['cell'][0] <= 2]
        elif side == 'B':
            return [(oid, d) for oid, d in self.field_objects.items()
                    if d['localized'] and 4 <= d['cell'][0] <= 6]
        return []

    def is_robot_on_side(self, side: str) -> bool:
        """Проверяет находится ли робот на стороне A или B."""
        return self.robot_side == side


def main(args=None):
    rclpy.init(args=args)
    node = GameNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
