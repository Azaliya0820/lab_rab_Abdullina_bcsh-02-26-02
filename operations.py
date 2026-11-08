from constants import PI,D_SMALL_LIMIT,D_LARGE_LIMIT
from typing import Annotated
def area_circle(
        d:Annotated[float,'диаметр сечения,мм'],)->float:
    """
    площадь круглого сечения A=π*d²/4,м²

    Args: 
         d: диаметр сечения
    Returns:
         площадь в м²
    """
    d_m=d/1000
    return PI*d_m**2/4.00
def area_rectangle(
        a:Annotated[float,'первая сторона,мм'],
        b:Annotated[float,'вторая сторона,мм'],)->float:
    """
    площадь прямоугольного сечения A=a*b,м²
    Args:
         a:первая сторона,мм
         b:вторая сторона,мм
    Returns:
         площадь в м²
    """
    return (a/1000.0)*(b/1000.0)
def area_ring(D:Annotated[float,'внешний диаметр,мм'],
        d:Annotated[float,'внутренний диаметр,мм'],)->float:
    """
    площадь кольцевого сечения A=π*(D²-d²)/4,м²
    Args:
         D:внешний диаметр,мм
         d:внутренний диаметр,мм
    Returns:
         площадь в м²
    """
    D_m=D/1000.0
    d_m=d/1000.0
    return PI*(D_m**2-d_m**2)/4.0
def flow_rate(area:float,v:float)->float:
    """
    Расход жидкости Q=A*v*3600,м³/ч
    Args:
        area:площадь сечения,м²
        v:скорость потока,м/с
    Returns:
        Расход в м³/ч
    """
    return area*v*3600.0


def diameter_class(d: float)->str:
    """
    Классифицировать размер сечения через if-elif-else
    d<25—малое сечение;
    25≤d≤200—нормальное сечение;
    d>200—крупное сечение
    Args:
        d:размер сечения,мм
    Returns:
        Строка с названием класса сечения
    """
    if d<D_SMALL_LIMIT:
        return "малое сечение"
    elif d<=D_LARGE_LIMIT:
        return "нормальное сечение"
    else:
        return "крупное сечение"