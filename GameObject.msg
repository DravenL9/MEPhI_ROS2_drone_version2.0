# GameObject.msg — описание обнаруженного игрового объекта

uint32 object_id                # ID объекта из find_object_2d
string quality                  # "good" / "normal" / "bad"

# Координаты центра объекта в пикселях (из камеры)
float64 pixel_x
float64 pixel_y

# Координаты центра объекта в реальном мире (мм)
float64 world_x
float64 world_y

# Положение на карте (индексы клетки)
int32 cell_row                  # строка в map_aruco [0..6]
int32 cell_col                  # столбец в map_aruco [0..4]
int32 cell_id                   # ID aruco маркера клетки (или -1 для чёрных)

# Гомография доступна
bool localized                  # true если world_x/world_y вычислены
