# сравнение нескольких предметов на максимальное количество резов

import tkinter
import keyboard
import time

class Item:
    def __init__(self, text, mousePos):




class Win:
    def __init__(self, listWin):
        self.startX = 23.5
        self.startY = 167
        self.delta = 53
        self.h = 20
        self.w = 20

        root = tkinter.Tk()
        root.overrideredirect(True)
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-alpha", 0.5)
        root.geometry("%dx%d+%d+%d" % (150, 20, 200, 100))
        text = tkinter.Label(text="Сортировка колец")
        text.pack()

        if listWin:
            self.create_window(listWin)

        root.mainloop()

    def create_window(self, listWin):
        for position in listWin:
            posXandY = self.position_determination(position)
            win = tkinter.Toplevel()
            win.overrideredirect(True)
            win.wm_attributes("-topmost", True)
            # win.wm_attributes("-transparentcolor", position[2])
            win.configure(bg=position[2])
            x = self.startX + posXandY[0] * self.delta
            y = self.startY + posXandY[1] * self.delta
            win.geometry("%dx%d+%d+%d" % (self.h, self.w, x, y))

    def position_determination(self, pos):
        x = (int(pos[0]) - self.startX) // self.delta
        y = (int(pos[1]) - self.startY) // self.delta
        return [x, y]


class maxResistance:
    def __init__(self):
        self.maxResistance = [[0, 0, 0], []]
        self.listWin = []
        self.colors = ["green", "red", "cyan", "blue"]

    def add_item(self, item, mousePos):
        self.textItem = item
        self.mouseX = mousePos[0]
        self.mouseY = mousePos[1]

        self.check_item()

    def check_item(self):
        resistance = [self.search_for_resistance()]
        resistance.append([mouseX, mouseY])
        self.compare_items(resistance)

        self.listWin = self.maxResistance[1]

    def search_for_resistance(self):
        res = [0, 0, 0]
        text = self.textItem.split("\n")
        text = [x[1:] for x in text if x.find("Resistance") > 0]

        for x in text:
            x = x.split("%")
            if x[1].find("Fire") > 0:
                res[0] += int(x[0])
            if x[1].find("Cold") > 0:
                res[1] += int(x[0])
            if x[1].find("Lightning") > 0:
                res[2] += int(x[0])
            if x[1].find("all Elemental") > 0:
                res[0] += int(x[0])
                res[1] += int(x[0])
                res[2] += int(x[0])
        return res

    def compare_items(self, resistance):
        if self.maxResistance[1]:
            self.compare_resistance(resistance)
        else:
            self.maxResistance[0] = resistance[0]
            self.maxResistance[1].append(resistance[1] + [self.colors[0]])

    def compare_resistance(self, resistance):
        if resistance[0][0] >= self.maxResistance[0][0]:
            self.maxResistance[0][0] = resistance[0][0]
            if self.add_maxResItem(resistance[1]):
                self.maxResistance[1][:1].append(self.colors[1])
        if resistance[0][1] >= self.maxResistance[0][1]:
            self.maxResistance[0][1] = resistance[0][1]
            self.maxResistance[1].append(resistance[1] + [self.colors[2]])
        if resistance[0][2] >= self.maxResistance[0][2]:
            self.maxResistance[0][2] = resistance[0][2]
            self.maxResistance[1].append(resistance[1] + [self.colors[3]])

        if sum(resistance[0]) >= sum(self.maxResistance[0]):
            self.maxResistance[0] = resistance[0]
            self.maxResistance[1].append(resistance[1] + [self.colors[0]])

    def add_maxResItem(self, newIitem):
        chek = 1
        for item in self.maxResistance[1]:
            if newIitem in item:
                chek = 0
                break
        if chek:
            self.maxResistance[1].append(item[1])
        return chek


if __name__ == "__main__":
    mouse = tkinter.Tk()
    items = maxResistance()
    while 1:
        if keyboard.is_pressed("ctrl+c"):
            time.sleep(0.5)
            mouseY = mouse.winfo_pointery()
            mouseX = mouse.winfo_pointerx()
            text = tkinter.Tk().clipboard_get()
            newItem = Item(text, [mouseX, mouseY])
            items.add_item(newItem)
            print(items.maxResistance)

        if keyboard.is_pressed("alt+1"):
            time.sleep(1)
            if item.listWin:
                root = Win(item.listWin)
            print("1")

        if keyboard.is_pressed("alt+ctrl+1"):
            break

    # listWin = [[0, 0, "white"], [1, 0, "black"], [1, 1, "green"]]
    # root = Win(listWin)

