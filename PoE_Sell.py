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
    arrQuality = sorting_quality(arrItems)
    # print_list(arrQuality)
    # print("-" * 20)
    return grouping_items(arrQuality)


def sorting_quality(arrItems):  # сортировка качества
    arrQuality = [[] for x in range(20)]
    for item in arrItems:
        quality = item[0]
        arrQuality[quality].append(item[1:])
    # arrQuality = [x for x in arrQuality if x]
    return arrQuality


def grouping_items(arrQuality):  # грипировка предметов по сумме качеств
    tmpList = {"qual": 19, "sum": 40, "setTtems": []}
    setItems = []
    while tmpList["qual"]:
        tmpList = {"qual": 19, "sum": 40, "setTtems": []}
        tmpSet, arrQuality = recursiv_sum(arrQuality, tmpList)
        if tmpList["qual"]:
            setItems.append(tmpList["setTtems"])
    return setItems


def recursiv_sum(arrQuality, tmpList):
    for qual in range(tmpList["qual"], 0, -1):
        if len(arrQuality[qual]):
            tmpSum = tmpList["sum"] - qual
            pop = arrQuality[qual][-1]
            if tmpSum == 0:
                tmpList["qual"] = qual
                tmpList["setTtems"].append(pop)
                arrQuality[qual].pop(-1)
                return tmpList, arrQuality
            elif tmpSum > 0:
                tmpList["qual"] = qual
                tmpList["sum"] = tmpSum
                if tmpList["sum"] <= qual:
                    tmpList["qual"] = tmpList["sum"]
                tmp_arrQuality = copy.deepcopy(arrQuality)
                tmp_arrQuality[qual].pop(-1)
                tmpList, tmp_arrQuality = recursiv_sum(tmp_arrQuality, tmpList)

                if tmpList["qual"] > 0:
                    arrQuality = tmp_arrQuality.copy()
                    tmpList["setTtems"].append(pop)
                    return tmpList, arrQuality
                else:
                    tmpList["sum"] += qual
            else:
                tmpList["sum"] += qual
                tmpList["qual"] = 0
                return tmpList, arrQuality
    # tmpList["sum"] += tmpList["qual"]
    tmpList["qual"] = 0
    return tmpList, arrQuality


def transfer_inventory():  # перекладываем сеты в инвертарь
    # global arrGroupItems
    print(arrGroupItems)


if __name__ == "__main__":
    arrGroupItems = []
    dimensions = []
    keyboard.add_hotkey("alt+1", creation_array)
    keyboard.add_hotkey("alt+2", transfer_inventory)

    keyboard.wait("ctrl+alt+1")
