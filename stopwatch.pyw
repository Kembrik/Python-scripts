import keyboard
import random
import time
import datetime
import autoit
import tkinter
import threading


class Stopwatch():
    def __init__(self):
        self.root = tkinter.Tk()

        self.stopwatch()
        self.root.mainloop()

    def stopwatch(self):
        # self.root = tkinter.Tk()

        self.temp = 0
        self.afto_id = ""
        self.dif_x, self.dif_y = 80, 950

        self.root.title("Stopwatch")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.5)
        self.root.config(bg="black")
        self.root.geometry(f"+{self.dif_x}+{self.dif_y}")

        self.label1 = tkinter.Label(
            self.root, width=5, font="Arial 25", text="00:00")
        self.label1.grid(row=0, columnspan=2)

        self.button1 = tkinter.Button(
            self.root, text="Start", command=self.start_sw)
        self.button2 = tkinter.Button(
            self.root, text="Stop", command=self.stop_sw)
        self.button3 = tkinter.Button(
            self.root, text="Cont", command=self.continue_sw)
        self.button4 = tkinter.Button(
            self.root, text="Reset", command=self.reset_sw)

        self.button1.grid(row=1, columnspan=2, sticky="ew")

        self.root.bind("<ButtonPress-1>", self.on_mouse_down)
        self.root.bind("<B1-Motion>", self.update_position)

        self.menu = tkinter.Menu(self.root.master, tearoff=0)
        self.menu.add_command(label="Выход", command=self.onExit)

        self.root.bind("<Button-3>", self.showMenu)

        self.hotkey()

    def start_sw(self):
        self.button1.grid_forget()
        self.button2.grid(row=1, columnspan=2, sticky="ew")
        self.tick()

    def tick(self):
        global temp, afler_id
        afler_id = self.root.after(1000, self.tick)
        f_temp = datetime.datetime.fromtimestamp(self.temp).strftime("%M:%S")
        self.label1.configure(text=str(f_temp))
        self.temp += 1

    def stop_sw(self):
        self.button2.grid_forget()
        self.button3.grid(row=1, column=0, sticky="ew")
        self.button4.grid(row=1, column=1, sticky="ew")
        self.root.after_cancel(afler_id)

    def continue_sw(self):
        self.button3.grid_forget()
        self.button4.grid_forget()
        self.button2.grid(row=1, columnspan=2, sticky="ew")
        self.tick()

    def reset_sw(self):
        self.temp = 0
        self.label1.configure(text="00:00")
        self.button3.grid_forget()
        self.button4.grid_forget()
        self.button1.grid(row=1, columnspan=2, sticky="ew")

    def on_mouse_down(self, event):
        win_position = [int(coord)
                        for coord in self.root.wm_geometry().split("+")[1:]]
        self.dif_x, self.dif_y = win_position[0] - \
            event.x_root, win_position[1] - event.y_root

    def update_position(self, event):
        self.root.wm_geometry("+%d+%d" %
                              (event.x_root + self.dif_x, event.y_root + self.dif_y))

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.root.quit()

    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = threading.Thread(
                target=func, args=args, kwargs=kwargs)
            current_thread.start()
        return wrapper

    @thread
    def hotkey(self):
        keyboard.add_hotkey('F1', self.random_send)
        keyboard.wait()

    def random_send(self):
        keys = ['1', '2', '3', '4']
        random.shuffle(keys)
        for k in keys:
            t = random.random()
            keyboard.send(k)
            time.sleep(t*0.1)


if __name__ == "__main__":
    watch = Stopwatch()
