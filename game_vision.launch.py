"""
Launch файл для game_vision.

Запускает:
1. find_object_2d (из отдельного пакета)
2. game_detect
3. aruco_mapping
4. game_node
5. rviz2 (опционально)
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node as RosNode
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('game_vision')
    config_file = os.path.join(pkg_share, 'config', 'game_config.yaml')

    # Аргументы
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz', default_value='true',
        description='Запускать rviz2'
    )
    camera_topic_arg = DeclareLaunchArgument(
        'camera_topic', default_value='/camera/image_raw',
        description='Топик камеры'
    )

    # ---- find_object_2d ----
    # Предполагается что пакет find_object_2d установлен
    find_object_node = RosNode(
        package='find_object_2d',
        executable='find_object_2d',
        name='find_object_2d',
        output='screen',
        remappings=[
            ('image', LaunchConfiguration('camera_topic')),
        ],
        parameters=[{
            'subscribe_depth': False,
            'gui': True,
        }]
    )

    # ---- game_detect ----
    game_detect_node = RosNode(
        package='game_vision',
        executable='game_detect.py',
        name='game_detect',
        output='screen',
        parameters=[config_file]
    )

    # ---- aruco_mapping ----
    aruco_mapping_node = RosNode(
        package='game_vision',
        executable='aruco_mapping.py',
        name='aruco_mapping',
        output='screen',
        parameters=[config_file]
    )

    # ---- game_node ----
    game_node = RosNode(
        package='game_vision',
        executable='game_node.py',
        name='game_node',
        output='screen',
        parameters=[config_file]
    )

    # ---- rviz2 ----
    rviz_node = RosNode(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'config', 'game_vision.rviz')],
        condition=None  # Всегда запускается, управляйте через параметр
    )

    return LaunchDescription([
        use_rviz_arg,
        camera_topic_arg,
        find_object_node,
        game_detect_node,
        aruco_mapping_node,
        game_node,
        rviz_node,
    ])
