import keyboard
import time
import autoit


def creation_array():  # создаем массив предметов и их сортировка
    delta = 53
    # arealPoint = select_area_sort()
    arealPoint = [(45, 178), (621, 722)]

    typeItem = select_type_item()
    print(typeItem)


def select_area_sort():  # выбираем область предметов
    arealPoint = []
    while len(arealPoint) < 2:
        if len(arealPoint) == 0:
            autoit.tooltip("  StartPoint (press ctrl+1)")
        if len(arealPoint) == 1:
            autoit.tooltip("  EndPoint (press ctrl+1)")

        if keyboard.is_pressed("ctrl+1"):
            time.sleep(0.5)
            arealPoint.append(mouse_pos())
    return arealPoint


def mouse_pos():
    return autoit.mouse_get_pos()


def select_type_item():
    autoit.MSG(3 + 32, "Выбор предметов", "Продаем камни?")


# Case 6
# 	Return 1
# Case 7
# 	Return 2
# Case 2
# 	Return 0

if __name__ == "__main__":

    while 1:
        if keyboard.is_pressed("alt+1"):
            time.sleep(0.5)
            creation_array()
            print(1)

        if keyboard.is_pressed("alt+2"):
            time.sleep(0.5)
            print(2)

        if keyboard.is_pressed("alt+ctrl+1"):
            break
