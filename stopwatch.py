import tkinter
import datetime


def start_sw():
    button1.grid_forget()
    button2.grid(row=1, columnspan=2, sticky="ew")
    tick()


def tick():
    global temp, afler_id
    afler_id = root.after(1000, tick)
    f_temp = datetime.datetime.fromtimestamp(temp).strftime("%M:%S")
    label1.configure(text=str(f_temp))
    temp += 1


def stop_sw():
    button2.grid_forget()
    button3.grid(row=1, column=0, sticky="ew")
    button4.grid(row=1, column=1, sticky="ew")
    root.after_cancel(afler_id)


def continue_sw():
    button3.grid_forget()
    button4.grid_forget()
    button2.grid(row=1, columnspan=2, sticky="ew")
    tick()


def reset_sw():
    global temp
    temp = 0
    label1.configure(text="00:00")
    button3.grid_forget()
    button4.grid_forget()
    button1.grid(row=1, columnspan=2, sticky="ew")


def on_mouse_down(event):
    global dif_x, dif_y
    win_position = [int(coord) for coord in root.wm_geometry().split("+")[1:]]
    dif_x, dif_y = win_position[0] - event.x_root, win_position[1] - event.y_root


def update_position(event):
    root.wm_geometry("+%d+%d" % (event.x_root + dif_x, event.y_root + dif_y))


root = tkinter.Tk()
temp = 0
afto_id = ""
dif_x, dif_y = 80, 950

root.title("Stopwatch")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.5)
root.geometry(f"+{dif_x}+{dif_y}")


label1 = tkinter.Label(root, width=5, font="Arial 25", text="00:00")
label1.grid(row=0, columnspan=2)

button1 = tkinter.Button(root, text="Start", command=start_sw)
button2 = tkinter.Button(root, text="Stop", command=stop_sw)
button3 = tkinter.Button(root, text="Cont", command=continue_sw)
button4 = tkinter.Button(root, text="Reset", command=reset_sw)

button1.grid(row=1, columnspan=2, sticky="ew")

root.bind("<ButtonPress-1>", on_mouse_down)
root.bind("<B1-Motion>", update_position)

root.mainloop()
