import autoit
import time
import random
import win32gui


def determining_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def make_active_window(process, win):  # Сделать окно активным
    if autoit.process_exists(process):
        autoit.win_activate(win)
        print("Сделано!")
        return 1
    print("Окно не найдено!")
    return 0


def temp_move(win):  # случайное перемещение и возврат назад
    x = 954
    y = 485
    dx = random.randint(50, 200)
    dy = random.randint(-200, 200)
    if autoit.win_wait_active(win):
        time.sleep(0.5)
        autoit.mouse_click("left", x + dx, y + dy)
        t = random.randint(1, 3)
        time.sleep(t)
        autoit.mouse_click("left", x - dx, y - dy)
        time.sleep(0.5)


if __name__ == "__main__":

    poePros = "PathofExile_x64.exe"
    poeWin = "Path of Exile"
    # minute = 0.5
    minute = random.randint(10, 15)

    while True:
        time.sleep(minute * 60)

        winActivate = determining_active_window()

        if make_active_window(poePros, poeWin):
            temp_move(poeWin)

        autoit.win_activate(winActivate)
