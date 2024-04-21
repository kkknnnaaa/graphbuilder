from tkinter import *
from math import *
from functools import partial
from PIL import ImageGrab
from tkinter import filedialog as fd
from tkinter import colorchooser
from PIL import Image
import io
import tkinter as tk

root = Tk()

left_mouse_press = False
entry_btns = []
functions = {}  # ключ(номер поля ввода) - значение(ввод пользователя)
colors = {}

screen_width = 600
screen_height = 600

root.geometry(str(screen_width) + 'x' + str(screen_height) + '+600+50')


def quater(str):
    str = str.replace('^', '**')
    return str

# --ПРОВЕРКА ВВОДА НА КОРРЕКТНОСТЬ--


def check(str):
    str = quater(str)
    str = str.replace('x', '1')
    try:
        eval(str)
    except:
        return False
    return True

# --ВЫЧЕСЛЕНИЕ ЗНАЧЕНИЯ ФУНКЦИИ--


def calc(s, x):
    # s = s.replace('x', str(x))
    try:
        return eval(s)
    except:
        return 0

# -- ДЕЙСТВИЕ ДЛЯ ГАЛОЧКИ --


def ok_mark(ind):
    print("ind={}".format(ind))
    text = entry_btns[ind][0].get()
    print("text={}".format(text))
    if check(text):
        functions[ind] = quater(text)
        redraw_all()
    else:
        print("не коректно")

    # for vvod in fs:
    #     print(vvod[0].get())


def x_mark(ind):
    print("ind={}".format(ind))
    del functions[ind]
    redraw_all()

# -- ДЕЙСТВИЕ ДЛЯ '+',  --


def plus_f():
    frame_line = Frame(frame_left)
    frame_line.pack(side='top', fill='x')
    index_entry_btns = len(entry_btns)
    btn9 = Button(frame_line, width=2, height=1, text='❎', fg='red', command=partial(x_mark, index_entry_btns))
    btn9.pack(side='left')
    frame_sep = Frame(frame_line, width=5)  # разделение слева
    frame_sep.pack(side='left')
    f = Entry(frame_line, bg='#D7E1D7', fg='#133313', selectforeground='#FFFFFF')  # окно ввода
    f.pack(side='left')
    btn = Button(frame_line, width=2, height=1, text='✅', fg='green', command=partial(ok_mark, index_entry_btns))
    btn.pack(side='left')
    frame_sep = Frame(frame_line, width=5)  # разделение слева
    frame_sep.pack(side='left')

    btn8 = Button(frame_line, width=2, text='█', fg='blue', command=partial(color_chooser, index_entry_btns))
    btn8.pack(side='left')

    frame_sep = Frame(frame_line, width=5)  # разделение слева
    frame_sep.pack(side='right')
    btn.pack()
    frame_sep = Frame(frame_line, width=5)
    frame_sep.pack(side='right')
    entry_btns.append((f, btn, btn8))

# --ОКНО С ПАРАМЕТРАМИ ДЛЯ ГРАФИКА--


def color_chooser(ind):
    rgb, hx = colorchooser.askcolor()
    print(rgb, hx)
    colors[ind] = hx
    entry_btns[ind][2]['foreground'] = hx
    redraw_all()


frame_left = Frame(root, width=120)  # поле для кнопок слева
frame_left.pack(side='left', fill='y')

canv = Canvas(root, bg='white')  # поле для координат
canv.pack(fill=BOTH, expand=1)

screen_width = canv.winfo_screenmmwidth()
screen_height = canv.winfo_screenmmheight()

xc = screen_width//2
yc = screen_height//2
scale = 30

# --СОЗДАНИЕ КООРДИНАТ--


def create_coordinates(scale, color, width, xc, yc):
    ''' ------=: сетка :=-----------
    scale - шаг сетки
    color - цвет линии сетки
    width - толщина линии сетки
    '''
    dx = 0
    while dx < screen_width:
        canv.create_line(xc+dx, screen_height, xc+dx, 0, width=width, fill=color)
        canv.create_line(xc-dx, screen_height, xc-dx, 0, width=width, fill=color)
        dx += scale
    dx = 0

    dy = 0
    while dy < screen_height:
        canv.create_line(0, yc+dy, screen_width, yc+dy, width=width, fill=color)
        canv.create_line(0, yc-dy, screen_width, yc-dy, width=width, fill=color)
        dy += scale
    # ------------------

# --СОЗДАНИЕ ЦИФР ДЛЯ МАШТАБА--


def drawnum(scale, xc, yc, color):
    kpoints = (screen_width//scale)-1
    num = 1
    for kx in range(scale, kpoints*scale+1, scale):
        canv.create_text(xc+kx, yc+scale//2, font=("Arial", scale//3), fill=color, text=str(num))
        canv.create_text(xc-kx, yc+scale//2, font=("Arial", scale//3), fill=color, text=str(-num))
        num += 1
    kpoints = (screen_height//scale)-1
    num = 1
    for ky in range(scale, kpoints*scale+1, scale):
        canv.create_text(xc+scale//2, yc+ky, font=("Arial", scale//3), fill=color, text=str(-num))
        canv.create_text(xc+scale//2, yc-ky, font=("Arial", scale//3), fill=color, text=str(num))
        num += 1
    # --------------------------

# --ПЕРЕРИСОВКА ВСЕГО--


def redraw_all():
    global scale, xc, yc
    redraw(scale, xc, yc)

# --РИСОВАНИЕ КООРДИНАТ, ФУНКЦИИ, МАШТАБА--


def redraw(scale, xc, yc):
    canv.delete(ALL)
    create_coordinates(scale//5, 'lightgray', 1, xc, yc)
    create_coordinates(scale, 'gray', 1, xc, yc)

    canv.create_line(xc, screen_height, xc, 0, width=3, arrow=LAST)
    canv.create_line(0, yc, screen_width, yc, width=3, arrow=LAST)

    canv.create_text(screen_width-18, yc-12, text='x')
    canv.create_text(xc+10, 10, text='y')
    drawnum(scale, xc, yc, color='black')
    for key, value in functions.items():
        # print(key, value)
        draw(value, scale, xc, yc, colors.get(key, 'blue'), -screen_width/2, screen_width/2)

    # --------------------------------------

# --РИСОВАНИЕ КООРДИНАТ И ФУНКЦИИ--


def draw(fstr, scale, xc, yc, color='green', x_start=-1000, x_finish=1000):
    prev_xd = x_start
    prev_yd = calc(fstr, x_start)
    x = x_start
    while x < x_finish:
        x += 0.1
        y = calc(fstr, x)

        draw_prev_xd = (xc + prev_xd*scale)
        draw_prev_yd = (yc - prev_yd*scale)
        draw_xd = (xc + x*scale)
        draw_yd = (yc - y*scale)

        canv.create_line(draw_prev_xd, draw_prev_yd, draw_xd, draw_yd, fill=color)
        prev_xd = x
        prev_yd = y

# --ДЕЙСТВИЕ ПРИ НАЖАТИИ НА КНОПКУ МЫШИ--


def butt_press(event):
    global left_mouse_press
    if event.num == 1:
        left_mouse_press = True
    # -------------------------------------

# --ДЕЙСТВИЕ ПРИ ОТЖАТИИ КНОПКИ МЫШИ--


def butt_release(event):
    global scale, left_mouse_press
    if event.num == 1:
        left_mouse_press = False
        # scale *= 2
        xc = event.x
        yc = event.y
        redraw(scale, xc, yc)
    # --------------------------------

# --ДЕЙСТВИЕ ПРИ ДВИЖЕНИИ МЫШКИ--


def mouse_move(event):
    global left_mouse_press
    if left_mouse_press:
        xc = event.x
        yc = event.y
        redraw(scale, xc, yc)
    # --------------------------

# -- ДЕЙСТВИЕ ДЛЯ КОЛЕСИКА МЫШКИ --


def change_scale(event):
    global scale, xc, yc
    if event.delta > 0:
        scale += 10
    else:
        scale -= 10
        if scale <= 0:
            scale = 10
    xc = event.x
    yc = event.y
    redraw(scale, xc, yc)
    '''print(event.delta)'''
    # -----------------------------


def change_window_size(event):
    global scale, screen_width, screen_height, xc, yc
    screen_width = event.width
    screen_height = event.height
    xc = screen_width//2
    yc = screen_height//2
    redraw(scale, xc, yc)


def create_box():
        print('canv.winfo_rootx() = ', canv.winfo_rootx())
        print('canv.winfo_rooty() = ', canv.winfo_rooty())
        print('canv.winfo_x() =', canv.winfo_x())
        print('canv.winfo_y() =', canv.winfo_y())
        print('canv.winfo_width() =', canv.winfo_width())
        print('canv.winfo_height() =', canv.winfo_height())

        x = canv.winfo_rootx()+canv.winfo_x()
        y = canv.winfo_rooty()+canv.winfo_y()
        x1 = x+canv.winfo_width()
        y1 = y+canv.winfo_height()
        # box=(x,y,x1,y1)
        box = (canv.winfo_rootx(), canv.winfo_rooty(), canv.winfo_rootx()+canv.winfo_width(), canv.winfo_rooty()+canv.winfo_height())
        print('box = ', box)
        return box


def save_image_to_file():
    box = create_box()
    name = fd.asksaveasfilename(filetypes=(("PNG files", "*.png"),))
    ImageGrab.grab(bbox=box).save(name+'.png')


def exit_f():
    quit()


def about_f():
    about = tk.Toplevel(root)
    caption = tk.Label(about, text="Проект: Программа построения 2D графиков функций.")
    target = tk.Label(about, text="Цель: Создание программы на языке программирования Python для построения графиков функций.")
    creator = tk.Label(about, text="Выполнила: Киселева Наталья")
    school = tk.Label(about, text="Школа 1550")
    year = tk.Label(about, text="2021г.")
    button = tk.Button(about, text="Закрыть", command=about.destroy)

    caption.pack(padx=10, pady=10)
    target.pack(padx=10, pady=10)
    creator.pack(padx=10, pady=10)
    school.pack(padx=10, pady=10)
    year.pack(padx=10, pady=10)
    button.pack(pady=5, ipadx=2, ipady=2)
    about.grab_set()


# -- ДЛЯ МЕНЮ --
main_menu = Menu()
file_menu = Menu()
file_menu.add_command(label="About", command=about_f)
file_menu.add_command(label="Exit", command=exit_f)

main_menu.add_cascade(label="New", command=plus_f)
main_menu.add_cascade(label="Save", command=save_image_to_file)
main_menu.add_cascade(label="File", menu=file_menu)
# --------------

plus_f()

redraw(scale, xc, yc)
canv.bind('<MouseWheel>', change_scale)
canv.bind('<ButtonPress>', butt_press)
canv.bind('<ButtonRelease>', butt_release)
canv.bind('<Motion>', mouse_move)
canv.bind('<Configure>', change_window_size)
root.config(menu=main_menu)

root.mainloop()
