#!/usr/bin/env python3
"""
game_detect — нода ROS2 для обнаружения и классификации игровых объектов.

Подписывается на топик /objects от find_object_2d,
вычисляет центр каждого объекта через гомографию,
классифицирует объект ("good"/"normal"/"bad"),
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


class GameDetectNode(Node):
    def __init__(self):
        super().__init__('game_detect')

        # ====================================================================
        # ПОЛЬЗОВАТЕЛЬСКАЯ НАСТРОЙКА: классификация объектов
        # Укажите ID объектов из find_object_2d и их "качество".
        # ID назначаются find_object_2d при добавлении объектов (1, 2, 3, ...).
        # ====================================================================
        self.declare_parameter('good_objects', [1, 2])       # IDs "хороших" объектов
        self.declare_parameter('normal_objects', [3, 4])      # IDs "нормальных" объектов
        self.declare_parameter('bad_objects', [5, 6])         # IDs "плохих" объектов

        good_ids = self.get_parameter('good_objects').get_parameter_value().integer_array_value
        normal_ids = self.get_parameter('normal_objects').get_parameter_value().integer_array_value
        bad_ids = self.get_parameter('bad_objects').get_parameter_value().integer_array_value

        # Словарь: object_id -> quality
        self.quality_map = {}
        for oid in good_ids:
            self.quality_map[oid] = 'good'
        for oid in normal_ids:
            self.quality_map[oid] = 'normal'
        for oid in bad_ids:
            self.quality_map[oid] = 'bad'

        self.get_logger().info(f'Quality map: {self.quality_map}')

        # Подписка на топик /objects от find_object_2d
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/objects',
            self.objects_callback,
            10
        )

        # Публикация обнаруженных объектов
        self.publisher = self.create_publisher(
            GameObjectArray,
            '/game_objects',
            10
        )

        self.get_logger().info('game_detect запущен. Ожидание данных из /objects...')

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

        game_objects_msg = GameObjectArray()

        for i in range(num_objects):
            offset = i * VALUES_PER_OBJECT
            obj_id = int(data[offset])
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

            # Определяем качество
            quality = self.quality_map.get(obj_id, 'unknown')

            # Формируем сообщение
            go = GameObject()
            go.object_id = obj_id
            go.quality = quality
            go.pixel_x = float(pixel_x)
            go.pixel_y = float(pixel_y)
            go.world_x = 0.0
            go.world_y = 0.0
            go.cell_row = -1
            go.cell_col = -1
            go.cell_id = -1
            go.localized = False

            game_objects_msg.objects.append(go)

            self.get_logger().debug(
                f'Object id={obj_id} quality={quality} '
                f'pixel=({pixel_x:.1f}, {pixel_y:.1f})'
            )

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
