# скрипт для подсчета предметов брони для рецепта на каусы
import keyboard, wx
import time
import autoit
import pyautogui, cv2, imutils
import os
import numpy as np


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

        self.typeList = [
            "Weapon",
            "Shields",
            "Body Armour",
            "Helmets",
            "Gloves",
            "Boots",
            "Ring",
            "Amulet",
            "Belt",
        ]
        self.listItems = dict.fromkeys(self.typeList, 0)

        # self.pass_inventar()

        # print(1)

    def take_screenshot(self):  # делаем снимок экрана
        img = pyautogui.screenshot(region=(5, 70, 680, 780))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def show_image(self, image):
        cv2.imshow("Image", image)
        cv2.waitKey(0)

    def start_scanning(self):  # начало сканирования
        if self.determining_size_tab():  # определение ращзмера вкладки
            return
        print(f"scale = {self.scale}")

        self.screenshot = self.take_screenshot()

        self.mainImag_2 = self.take_screenshot()

        # directory = "E:\python\PRO\PoE\data\images\Body Armour"
        # directory = "E:\python\PRO\PoE\data\images\Boots"
        # directory = "E:\python\PRO\PoE\data\images\Shields"
        # directory = "E:\python\PRO\PoE\data\images\Helmets"
        directory = "E:\python\PRO\PoE\data\images"
        for top, dirs, files in os.walk(directory):
            for nm in files:
                print(os.path.join(top, nm))
                self.mainImag = self.take_screenshot()
                listItem = self.search_items(os.path.join(top, nm))
                if listItem:
                    typeItem = top[top.rfind("\\") + 1 :]
                    self.listItems[typeItem] += len(listItem)
            # self.show_image(self.mainImag)
        self.show_image(self.mainImag_2)

    def determining_size_tab(self):  # определение ращзмера вкладки
        app = wx.App()
        # app.MainLoop()
        winMessage = wx.MessageBox(
            "Открыта большая вкладка?",
            "Вопрос",
            wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_QUESTION,
        )
        if winMessage == wx.YES:
            # print("Нажата кнопка (да)")
            self.scale = 3  # коэффициент уменьшение шаблона
        elif winMessage == wx.NO:
            # print("Нажата кнопка (нет)")
            self.scale = 1.5  # коэффициент уменьшение шаблона
        elif winMessage == wx.CANCEL:
            app.Destroy()
            return 1
        # print(winMessage)

        app.Destroy()

    def search_items(self, template):  # поиск предметов на вкладке

        img_gray = cv2.cvtColor(self.screenshot, cv2.COLOR_BGRA2GRAY)

        template = cv2.imread(template, 0)
        resized_img = imutils.resize(
            template, width=int(template.shape[1] / self.scale)
        )
        w_template, h_template = resized_img.shape[::-1]

        # self.show_image(img_gray)
        # self.show_image(resized_img)

        res = cv2.matchTemplate(img_gray, resized_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            arr = [0, 0]
            arr[0] = loc[1].tolist()
            arr[1] = loc[0].tolist()
            arr = list(zip(arr[0], arr[1]))
            arr = self.remove_duplicates(arr, resized_img.shape[::-1])

            for pt in arr:
                col = (0, 0, 255)
                bottom_right = (pt[0] + w_template, pt[1] + h_template)
                cv2.rectangle(
                    self.mainImag, pt, bottom_right, col, 2,
                )

            for pt in zip(*loc[::-1]):
                col = (0, 0, 255)
                bottom_right = (pt[0] + w_template, pt[1] + h_template)
                cv2.rectangle(
                    self.mainImag_2, pt, bottom_right, col, 2,
                )

            return arr
        return 0

    def remove_duplicates(self, tmpArr, size):  # сокращение дублируемых точек
        arr = [tmpArr[0]]
        for dup in tmpArr[1:]:
            if self.check_entry(arr, dup, size):
                arr.append(dup)
        return arr

    def check_entry(self, arr, dup, size):
        for item in arr:
            deltaX = abs(dup[0] - item[0])
            deltaY = abs(dup[1] - item[1])
            if deltaX < size[0] * 0.8 and deltaY < size[1] * 0.8:
                return 0
        return 1

    def print_list_Items(self):
        print(self.listItems)

    def clier_list_Items(self):
        self.listItems = dict.fromkeys(self.typeList, 0)


if __name__ == "__main__":
    main = Main()
    poeWin = "Path of Exile"
    autoit.win_activate(poeWin)
    # keyboard.add_hotkey("alt+1", main)
    keyboard.add_hotkey("ctrl+1", main.start_scanning)
    keyboard.add_hotkey("alt+1", main.print_list_Items)
    keyboard.add_hotkey("alt+3", main.clier_list_Items)

    # keyboard.add_hotkey("alt+2", transfer_inventory)

    keyboard.wait("ctrl+alt+1")
