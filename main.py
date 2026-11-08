"""
Точка входа программы «Расчёт расхода жидкости через сечение трубопровода»
Связывает модули:меню,валидацию,расчёты
"""

from validation import input_size,input_speed
from menu import show_menu,select_section,section_name
from operations import (
    area_circle,area_rectangle,area_ring,flow_rate,diameter_class,
)
def main()->None:
    """Главный сценарий:меню→ввод→расчёт→вывод"""
    print("=== Расчёт расхода жидкости через сечение трубопровода ===")

    while True:
        show_menu()
        code=select_section()
        if code is None:
            print("Работа завершена")
            break
        match code:
            case 1:
                d=input_size("Введите диаметр d,мм (5..500):")
                area=area_circle(d)
                cls=diameter_class(d)
            case 2:
                a=input_size("Введите сторону a,мм (5..500):")
                b=input_size("Введите сторону b,мм (5..500):")
                area=area_rectangle(a,b)
                cls="—"
            case 3:
                D=input_size("Введите внешний диаметр D,мм (5..500):")
                d=input_size("Введите внутренний диаметр d,мм (5..500):")
                if D<=d:
                    print("Ошибка:внешний диаметр должен быть больше внутреннего")
                    continue
                area=area_ring(D,d)
                cls="—"
        v=input_speed()
        q=flow_rate(area,v)

        print("\n=== Результаты ===")
        print(f"Тип сечения: {section_name(code)}")
        print(f"Площадь A:   {area:.6f} м²")
        print(f"Расход Q:    {q:.2f} м³/ч")
        print(f"Класс:       {cls}")
        print()

if __name__=="__main__":
    main()