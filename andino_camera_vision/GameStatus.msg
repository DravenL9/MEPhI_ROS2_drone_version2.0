# GameStatus.msg — состояние игры

bool game_started               # true когда найден центральный маркер [3][2]
string robot_side                # "A" (верхняя половина) / "B" (нижняя половина) / "unknown"

# Позиция робота
float64 robot_pixel_x
float64 robot_pixel_y
float64 robot_world_x
float64 robot_world_y
int32 robot_cell_row
int32 robot_cell_col

# ID aruco маркера робота (6x6)
uint32 robot_aruco_id
