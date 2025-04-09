
# Симуляция робота MEPhI_ROS2_drone в Gazebo

## Сборка

Установите зависимости пакетов:

```
rosdep install --from-paths src -i -y
```

Создайте пакет:

```
colcon build
```

Примечание: `--symlink-install` при необходимости может быть добавлен.

Наконец, создайте исходную папку установки:

```
. install/setup.bash
```

Примечание: `gazebo` возможно, потребуется найти источник:

```
. /usr/share/gazebo/setup.bash
```

# Использование 

## MEPhI_ROS2_drone симуляция с плагином Gazebo diff drive


```
ros2 launch andino_gz_classic andino_one_robot.launch.py initial_pose_x:=3.0
```

Этот файл запуска поддерживает следующие параметры запуска:

- `use_sim_time`: этот параметр указывает rviz, что он должен работать со временем моделирования (по умолчанию: `true`)
- `rviz`: этот параметр позволяет определить, хотите ли вы запускать rviz при этом запуске. Значение `False` может быть полезно, если вы хотите просмотреть rviz на другом компьютере (по умолчанию: `true`)
- `world`: SDF-файл мира, в котором будет запущен MEPhI_ROS2_drone. Обратите внимание, что мир должен быть доступен в `gazebo paths` (по умолчанию: `empty_world.world`)


Наконец, доступны все параметры запуска MEPhI_ROS2_drone для перевода робота в определенное положение. Для получения дополнительной информации обо всех параметрах дочерних файлов запуска вы можете написать:
```
ros2 launch andino_gz_classic andino_one_robot.launch.py -s
```

## MEPhI_ROS2_drone симуляция с плагином Gazebo ros2 control

```
ros2 launch andino_gz_classic andino_one_robot.launch.py use_gazebo_ros_control:=true
```

## Создание MEPhI_ROS2_drone robot

```
ros2 launch andino_gz_classic spawn_robot.launch.py initial_pose_x:=3.0 entity:=andino robot_description_topic:=/andino/robot_description
```

Параметры этого запуска позволяют поместить робота в любое место симуляции.

- `use_sim_time`: используйте часы моделирования (Gazebo), если значение `true` (по умолчанию: `true`)

- `initial_pose_x`: начальная x-поза MEPhI_ROS2_drone в моделировании (по умолчанию: `0.0`)

- `initial_pose_y`: начальная y-поза MEPhI_ROS2_drone в моделировании (по умолчанию: `0.0`)

- `initial_pose_z`: начальная z-поза MEPhI_ROS2_drone в моделировании (по умолчанию: `0.0`)

- `robot_description_topic`: топик с описанием робота (по умолчанию: `/robot_description`)

- `initial_pose_yaw`: начальная yaw-поза (угол рыскания) MEPhI_ROS2_drone в моделировании (по умолчанию: `0.0`)

- `use_gazebo_ros_control`: значение `True` для использования плагина `gazebo_ros_control` (по умолчанию: `false`)

- `entity`: имя робота (по умолчанию: `MEPhI_ROS2_drone`)

- `rsp_frequency`: частота публикации состояния робота (по умолчанию: `30.0`)
