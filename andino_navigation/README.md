# MEPhI_ROS2_drone Navigation

Мы полагаемся на стек [Nav2](https://github.com/ros-planning/navigation2) для навигации MEPhI_ROS2_drone.

# Использование

## Предварительные требования
  1. Запустите основной стек на MEPhI_ROS2_drone:

```
ros2 launch andino_bringup andino_robot.launch.py
```

  2. Запишите карту с помощью [`MEPhI_ROS2_drone_slam`](../andino_slam/README.md).

## Run Nav Stack

Запустите стек навигации командой:

```
ros2 launch andino_navigation bringup.launch.py map:=<path-to-my-map-yaml-file>
```

По умолчанию используется [config file](params/nav2_params.yaml). Для использования пользовательского файла параметров выполните:

```
ros2 launch andino_navigation bringup.launch.py map:=<path-to-my-map-yaml-file> params_file:=<path-to-my-param-file>
```
