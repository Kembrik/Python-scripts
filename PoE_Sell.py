import tkinter, tkinter.messagebox
import keyboard
import time, copy
import autoit


def creation_array():  # создаем массив предметов
    global arrGroupItems
    global dimensions
    dimensions = select_area_sort()
    # heightItem = sel_type_item() + 1  # при бутылках увелитивается высота в 2
    heightItem = 2
    arrItems = array_write(dimensions, heightItem)
    arrGroupItems = sorting_items(arrItems)
    print(arrGroupItems)


def select_area_sort():  # определение облости сортировки
    mousePos = []
    while len(mousePos) < 2:
        if len(mousePos) == 0:
            autoit.tooltip("StartPoint (Press Ctrl+1)")
        if len(mousePos) == 1:
            autoit.tooltip("EndPoint")
        # keyboard.add_hotkey("ctrl+1", lambda: mousePos.append(mouse_pos()))
        if keyboard.is_pressed("ctrl+1"):
            mousePos.append(mouse_pos())
            time.sleep(0.2)
    autoit.tooltip("")
    return mousePos


def mouse_pos():
    # time.sleep(0.1)
    # return 1
    return autoit.mouse_get_pos()


def sel_type_item():  # выбор типа предмета сортировки
    root = tkinter.Tk()
    root.withdraw()
    answer = tkinter.messagebox.askyesno(
        title="Выбор предметов", message="Продаем камни?"
    )

    root.destroy()
    return 1
    # return answer


def array_write(dimensions, heightItem):  # запись предемеов в массив
    arr_items = []
    delta = [53, 53 * heightItem]
    posX, posY = 0, 0
    endX = round(
        (dimensions[1][0] - dimensions[0][0]) / delta[0]
    )  # количестворедметов  по оси X
    endY = round(
        (dimensions[1][1] - dimensions[0][1]) / delta[1]
    )  # количество предметов в по оси Y
    while posY <= endY:
        while posX <= endX:
            mouse_move(dimensions[0], posX, posY, delta)
            quality = determ_quality()
            if quality:
                arr_items.append([quality, posX, posY])
            posX += 1
        posX = 0
        posY += 1
    return arr_items


def mouse_move(coordinates, posX, posY, delta):  # перемещение курсора
    x = coordinates[0] + posX * delta[0]
    y = coordinates[1] + posY * delta[1]
    autoit.mouse_move(x, y)


def determ_quality():  # определение качества
    time.sleep(0.2)
    keyboard.send("ctrl+c")
    time.sleep(0.1)
    item = autoit.clip_get()
    autoit.clip_put("")
    if item.find("Quality") > 0:
        item = item.split("\n")
        for l in item:
            if l.find("Quality") != -1:
                item = l
                break
        item = [x for x in item if x.isdigit()]
        return int("".join(item))


def sorting_items(arrItems):  # сортировка предметов
    tmpSet = 1
    arrQuality = []
    while tmpSet:
        tmpSet = grouping_items(len(arrItems), tmpSet, arrItems)
        if tmpSet:
            arrQuality.append(creat_set(arrItems, tmpSet))
            arrItems = updating_set_Quality(arrItems, tmpSet)

    return arrQuality


def creat_set(arrItems, tmpSet):  # создание сета суммы предметов
    setItem = [x[1:] for n, x in enumerate(arrItems) if tmpSet[n]]
    return setItem


def grouping_items(n, tmpSet, arrItems, prefix=[]):  # генерирование вариантов
    if n == 0:
        if calculation(prefix, arrItems):
            tmpSet = prefix[:]
            return tmpSet
    else:
        tmpSet = grouping_items(n - 1, tmpSet, arrItems, prefix + [0])
        if tmpSet:
            return tmpSet
        tmpSet = grouping_items(n - 1, tmpSet, arrItems, prefix + [1])
        if tmpSet:
            return tmpSet
    return []


def calculation(prefix, arrItems):  # подсчет суммы
    # mass = 0
    sumQuality = 40
    for i in range(len(prefix)):
        if prefix[i] == 1:
            sumQuality -= arrItems[i][0]
    if not sumQuality:
        return 1
    return 0


def updating_set_Quality(arrItems, tmpSet):  # обновление списка предметов
    setQuality = [x for n, x in enumerate(arrItems) if not tmpSet[n]]
    return setQuality


def transfer_inventory():  # перекладываем сеты в инвертарь
    # global arrGroupItems
    print(arrGroupItems)


if __name__ == "__main__":
    arrGroupItems = []
    dimensions = []
    keyboard.add_hotkey("alt+1", creation_array)
    keyboard.add_hotkey("alt+2", transfer_inventory)

    keyboard.wait("ctrl+alt+1")
