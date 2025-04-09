# MEPhI_ROS2_drone Apps

Этот пакет содержит приложения для работы с MEPhI_ROS2_drone.

# Приложения

## Gazebo classic simulation + Nav2

Файл для запуска и моделирования MEPhI_ROS2_drone_gz_classic и стека Nav2. По умолчанию используется мир [`turtlebot3_world`](https://github.com/ROBOTIS-GIT/turtlebot3_simulations/tree/master).

```
 ros2 launch andino_apps andino_simulation_navigation.launch.py
```

Для визуализации робота MEPhI_ROS2_drone и взаимодействия с ним в `RViz`:

- Нажмите кнопку `2D Pose Estimate` и выберите начальную позу робота
- Нажмите кнопку `2D Goal Pose` и выберите конечную точку

Робот начнет двигаться к выбранной цели.

![Rviz_example_Nav2](docs/Rviz_example_Nav2.gif)

Для получения дополнительной информации и примеров вы можете ознакомиться с [Nav2 tutorials](https://docs.nav2.org/tutorials/index.html).

Изменяя файл world, не забудьте также изменить файл map.
