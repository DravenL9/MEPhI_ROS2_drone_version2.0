# MEPhI_ROS2_drone_slam

## Описание

Для запуска SLAM мы полагаемся на замечательный пакет [`slam_toolbox`](https://github.com/SteveMacenski/slam_toolbox/tree/ros2).

## Использование

После запуска робота просто запустите файл запуска SLAM:
```
ros2 launch andino_slam slam_toolbox_online_async.launch.py
```

Несколько конфигураций могут быть перенаправлены в `slam_toolbox_node`. По умолчанию параметры конфигурации получены из [config/slam_toolbox_only_async.yaml](config/slam_toolbox_online_async.yaml). В случае, если требуется передать пользовательский файл, просто используйте аргумент launch file для указания пути к новому файлу:

```
ros2 launch andino_slam slam_toolbox_online_async.launch.py slams_param_file:=<my_path>
```

Для сохранения карты вы можете использовать узел `map_saver_cli`, предоставляемый Nav2:

```
ros2 run nav2_map_server map_saver_cli -f <my-map-name>
```

Вы можете изменить пороговое значение для свободного пространства (0.25) и занятого пространства (0.65), используя аргументы
`--free` и `--occ`:

```
ros2 run nav2_map_server map_saver_cli --free 0.15 -f <my-map-name>
```

Больше информации тут:
 - https://github.com/ros-planning/navigation2/tree/main/nav2_map_server

Сохранив карту, вы сможете перемещаться по ней! Перейдите на страницу [`MEPhI_ROS2_drone_navigation`](../andino_navigation/README.md), чтобы узнать, как это сделать.
