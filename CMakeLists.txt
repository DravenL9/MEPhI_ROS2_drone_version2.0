cmake_minimum_required(VERSION 3.8)
project(game_vision)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# ============================================================================
# Генерация сообщений
# ============================================================================
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/GameObject.msg"
  "msg/GameObjectArray.msg"
  "msg/GameStatus.msg"
  DEPENDENCIES std_msgs geometry_msgs
)

# ============================================================================
# Установка Python нод
# ============================================================================
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  game_vision/game_detect.py
  game_vision/aruco_mapping.py
  game_vision/game_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# ============================================================================
# Launch файлы
# ============================================================================
install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
