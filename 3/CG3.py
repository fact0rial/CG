import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

lines_data = {
    "step_by_step": {"points": [], "color": "blue"},
    "dda": {"points": [], "color": "green"},
    "bresenham": {"points": [], "color": "purple"},
    "circle": {"points": [], "color": "red"}
}

labels = ['step_by_step', 'dda', 'bresenham', 'circle']


def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    return result, execution_time


def validate_input_lines(*args):
    try:
        return [int(arg.get()) for arg in args]
    except ValueError:
        error_label.config(text="Ошибка: введите целочисленные значения для полей X1, X2, Y1, Y2.")
        return None


def validate_input_circle(*args):
    try:
        return [int(arg.get()) for arg in args]
    except ValueError:
        error_label.config(text="Ошибка: введите целочисленные значения для полей X1, X2, Радиус.")
        return None


def step_by_step_line(x1, y1, x2, y2):
    points = []
    if x2 != x1:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
    else:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            points.append((x1, y))
        return points
    if x1 > x2:
        x1, x2 = x2, x1
    while x1 <= x2:
        y = k * x1 + b
        points.append((round(x1), round(y)))
        x1 += 0.1
    return points


def dda_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    L = max(abs(dx), abs(dy))
    points.append((x1,y1))
    if L == 0:
        return points
    x = x1
    y = y1
    i = 0
    while(i<=L):
        x = x + dx / L
        y = y + dy / L
        i += 1
        points.append((int(x), int(y)))
    return points


def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points


def bresenham_circle(x1, y1, radius):
    radius = abs(radius)
    points = []
    x = 0
    y = radius
    e = 3 - 2 * radius
    points.extend([
            (x1 + x, y1 + y), (x1 - x, y1 + y), (x1 + x, y1 - y), (x1 - x, y1 - y),
            (x1 + y, y1 + x), (x1 - y, y1 + x), (x1 + y, y1 - x), (x1 - y, y1 - x)])
    while x < y:
        if (e >= 0):
            e = e + 4 * (x - y) + 10
            x += 1
            y -= 1
        else:
            e = e + 4 * x + 6
            x = x + 1
        points.extend([
            (x1 + x, y1 + y), (x1 - x, y1 + y), (x1 + x, y1 - y), (x1 - x, y1 - y),
            (x1 + y, y1 + x), (x1 - y, y1 + x), (x1 + y, y1 - x), (x1 - y, y1 - x)])
    return points


def plot_points(ax, points, color='red'):
    for x, y in points:
        square = patches.Rectangle((x, y), 1, 1, linewidth=0, facecolor=color)
        ax.add_patch(square)


def draw_graph():
    global canvas, fig, ax

    if canvas:
        canvas.get_tk_widget().destroy()

    fig.clf()
    ax = fig.add_subplot(111)

    ax.set_xticks(range(-15, 16, 1))
    ax.set_yticks(range(-15, 16, 1))
    ax.grid(True, which='both', color='lightgray', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_aspect('equal')

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)

    for label in labels:
        line_data = lines_data[label]
        if line_data['points']:
            plot_points(ax, line_data["points"], color=line_data["color"])

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def draw_step_by_step():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(step_by_step_line, x1, y1, x2, y2)
        lines_data["step_by_step"]["points"] = points
        error_label.config(text=f"Пошаговый алгоритм: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_dda():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(dda_line, x1, y1, x2, y2)
        lines_data["dda"]["points"] = points
        error_label.config(text=f"Алгоритм ЦДА: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_bresenham():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(bresenham_line, x1, y1, x2, y2)
        lines_data["bresenham"]["points"] = points
        error_label.config(text=f"Алгоритм Брезенхема: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_circle():
    inputs = validate_input_circle(entry_x1, entry_y1, entry_radius)
    if inputs:
        x1, y1, radius = inputs
        points, exec_time = measure_time(bresenham_circle, x1, y1, radius)
        lines_data["circle"]["points"] = points
        error_label.config(text=f"Алгоритм Брезенхема (окружность): время выполнения {exec_time:.2f} мс")
        draw_graph()


def clear_all():
    for key in lines_data:
        lines_data[key]["points"] = []
    error_label.config(text="Все линии удалены")
    draw_graph()


app = tk.Tk()
app.title("Алгоритмы растеризации")

left_frame = ttk.Frame(app)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = ttk.Frame(app)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

ttk.Label(left_frame, text="X1:").pack(pady=2)
entry_x1 = ttk.Entry(left_frame, width=5)
entry_x1.pack(pady=2)

ttk.Label(left_frame, text="Y1:").pack(pady=2)
entry_y1 = ttk.Entry(left_frame, width=5)
entry_y1.pack(pady=2)

ttk.Label(left_frame, text="X2:").pack(pady=2)
entry_x2 = ttk.Entry(left_frame, width=5)
entry_x2.pack(pady=2)

ttk.Label(left_frame, text="Y2:").pack(pady=2)
entry_y2 = ttk.Entry(left_frame, width=5)
entry_y2.pack(pady=2)

ttk.Label(left_frame, text="Радиус:").pack(pady=2)
entry_radius = ttk.Entry(left_frame, width=5)
entry_radius.pack(pady=2)

button1 = ttk.Button(left_frame, text="Пошагово", command=draw_step_by_step)
button1.pack(pady=5)

button2 = ttk.Button(left_frame, text="DDA", command=draw_dda)
button2.pack(pady=5)

button3 = ttk.Button(left_frame, text="Брезенхэм", command=draw_bresenham)
button3.pack(pady=5)

button4 = ttk.Button(left_frame, text="Брезенхэм (окружность)", command=draw_circle)
button4.pack(pady=5)

button_clear_all = ttk.Button(left_frame, text="Очистить", command=clear_all)
button_clear_all.pack(pady=10)

error_frame = ttk.Frame(left_frame, width=200, height=100)
error_frame.pack(side="top", pady=5)
error_frame.pack_propagate(False)

error_label = ttk.Label(error_frame, text="", foreground="red", anchor="center", justify='center', wraplength=180)
error_label.pack(fill="both", expand=True)

fig = plt.Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = None

draw_graph()

app.mainloop()