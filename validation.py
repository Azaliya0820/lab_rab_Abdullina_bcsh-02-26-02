"""
Валидация пользовательского ввода
Проверка границ через if-elif-else
Циклический ввод до корректного значения
"""
from __future__ import annotations
from constants import SIZE_MIN, SIZE_MAX, V_MIN, V_MAX
from logger import log_error

def validate_range(value:float,low:float,high:float)->tuple[bool,str]:
    """
    Проверка попадания value в [low, high] через if-elif-else
    :return:(True,"") или (False,сообщение)
    """
    if value<low:
        return False,f"Ошибка:значение меньше нижней границы ({low})"
    elif value>high:
        return False,f"Ошибка:значение больше верхней границы ({high})"
    else:
        return True,""

def input_number(prompt:str,low:float,high:float)->float:
    """
    Циклически запрашивать число,пока не будет корректного
    Проверяет тип (float) через try/except ValueError и границы
    """
    is_valid=False
    value=0.0
    while not is_valid:
        raw=input(prompt).strip()
        try:
            value=float(raw)
        except ValueError:
            msg=f"Ошибка:введено не число ('{raw}')."
            print(msg)
            log_error(msg)
            continue

        is_valid,msg=validate_range(value,low,high)
        if not is_valid:
            print(msg+" Повторите ввод.")
            log_error(msg)
    return value

def input_size(prompt:str)->float:
    """Циклический ввод размера сечения,мм (5..500)"""
    return input_number(prompt,SIZE_MIN,SIZE_MAX)

def input_speed()->float:
    """Циклический ввод скорости потока,м/с (0.1..10)"""
    return input_number(
        "Введите скорость потока v,м/с (0.1..10):",
        V_MIN,V_MAX,
    )