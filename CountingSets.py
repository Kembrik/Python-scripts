# скрипт для подсчета предметов брони для рецепта на каусы
import keyboard
import time
import autoit


class Item:
    def __init__(self, item=0):
        self.delta = [53, 53]
        self.dimensions = [0, 0]
        self.typeList = []
        self.type = ""
        self.name = ""

        # self.listItems = self.creating_list_items()
        self.creating_list_items()
        self.creating_dim_items()

        if item:
            self.identification(item)
            self.dimensions = self.dimensionsItems[self.type]

    def creating_list_items(self):  # создание списка предметов
        itemList = []
        with open(r"poe\data\ListOfItems.txt") as f:
            items = f.readlines()
        for item in items:
            if "#" in item:
                self.typeList.append(item[1:-2])
            else:
                itemList.append(item[:-1].split(","))
        self.listItems = dict(zip(self.typeList, itemList))

    def creating_dim_items(self):  # создание списка размеров
        dimList = [
            [1, 3],
            [2, 2],
            [2, 2],
            [2, 4],
            [2, 2],
            [2, 2],
            [1, 1],
            [1, 1],
            [2, 1],
        ]
        self.dimensionsItems = dict(zip(self.typeList, dimList))

    def identification(self, item):  # оперделение предмета
        self.determining_type_item(item)
        item = item.split("\n")

        # print(type(item))

    def determining_type_item(self, item):  # определение типа предмета
        for typeItem in self.listItems:
            for i in self.listItems[typeItem]:
                tmpType = item[: item.find("-")]
                tmpType = tmpType[tmpType[:-1].rfind("\n") + 1 : -2]
                if i in tmpType:
                    self.type = typeItem
                    return


class Main:
    def __init__(self):
        self.startCoor = [43, 181]

        self.typeList = [
            "Weapon",
            "Shield",
            "Body Armou",
            "Helmet",
            "Glove",
            "Boot",
            "Ring",
            "Amulet",
            "Belt",
        ]
        self.listItems = dict.fromkeys(self.typeList, 0)

        # self.pass_inventar()

        print(1)

    def pass_inventar(self):  # проход про вкладке
        item = Item()
        while True:
            self.mouse_move(item)
            if not self.definition_item():
                break
            break

    def mouse_move(self, itemPos):  # перемещение курсора
        x = self.startCoor[0] + itemPos.dimensions[0] * itemPos.delta[0]
        y = self.startCoor[1] + itemPos.dimensions[1] * itemPos.delta[1]
        autoit.mouse_move(x, y)
        time.sleep(0.2)

    def definition_item(self):  # определение предмета
        # item = self.scanning()
        time.sleep(0.1)
        if autoit.clip_get():
            item = autoit.clip_get()
            time.sleep(0.1)
            autoit.clip_put("")
            item = Item(item)
            self.listItems[item.type] += 1
        else:
            autoit.tooltip("Неполучилось сосканировать предмет")
            time.sleep(0.5)
            autoit.tooltip("")

    def scanning(self):  # копирование характеристик предмета
        autoit.clip_put("")
        keyboard.send("ctrl+c")
        time.sleep(0.2)
        if autoit.clip_get():
            item = autoit.clip_get()
            autoit.clip_put("")
            return item

    def print_list_Items(self):
        print(self.listItems)

    def clier_list_Items(self):
        self.listItems = dict.fromkeys(self.typeList, 0)


if __name__ == "__main__":
    main = Main()
    autoit.clip_put("")
    poeWin = "Path of Exile"
    autoit.win_activate(poeWin)
    # keyboard.add_hotkey("alt+1", main)
    keyboard.add_hotkey("ctrl+c", main.definition_item)
    keyboard.add_hotkey("alt+1", main.print_list_Items)
    keyboard.add_hotkey("alt+3", main.clier_list_Items)

    # keyboard.add_hotkey("alt+2", transfer_inventory)

    keyboard.wait("ctrl+alt+1")
