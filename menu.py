"""
Меню выбора типа сечения через match-case
"""
def show_menu()->None:
    print('\nвыберите тип сечения')
    print('1-круглое')
    print('2-прямоугольное')
    print('3-кольцевое')
    print('0-выход')
def select_section()->int|None:
    while True:
        choice=input('введите номер типа сечения(0-3):').strip()
        match choice:
            case '1':
                return 1
            case '2':
                return 2
            case '3':
                return 3
            case '0':
                return None
            case _:
                print('ошибка:неверный пункт меню. повторите ввод')
def section_name(code:int)->str:
    match code:
        case 1:
            return 'круглое'
        case 2:
            return 'прямоугольное'
        case 3:
            return 'кольцевое'
        case _:
            return 'неизвестное'