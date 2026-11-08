import math
#---диапазоны размеров сечения---
SIZE_MIN: float=5.0
SIZE_MAX: float=500.0
#---диапазон скорости потока---
V_MIN: float=0.1
V_MAX: float=10.0
#---пороги классификации---
D_SMALL_LIMIT: float=25.0
D_LARGE_LIMIT: float=200.0
#---число пи---
PI: float=math.pi
#---файл журнала ошибок---
LOG_FILE: str='input_errors.log'