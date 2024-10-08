import tkinter as tk
from tkinter import colorchooser


def rgb_to_hls(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    maximum = max(r, g, b)
    minimum = min(r, g, b)
    l = (maximum + minimum) / 2
    h = 0
    s = 0
    if (maximum == minimum):
        h = 0
        s = 0
        return h, l, s
    elif (l <= 0.5):
        s = (maximum - minimum) / (maximum + minimum)
    else:
        s = (maximum - minimum) / (2.0 - maximum - minimum)
    if (maximum == r):
        h = (g - b) / (maximum - minimum)
    elif (maximum == g):
        h = 2 + (b - r) / (maximum - minimum)
    else:
        h = 4 + (r - g) / (maximum - minimum)
    if h < 0:
        h = h + 6
    h = h * 60
    return int(h), int(100 * l), int(100 * s)
            
def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return int(100 * c), int(100 * m), int(100 * y), int(100 * k)

def hls_to_rgb(h, l, s):
    l = l / 100
    s = s / 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    rr, gg, bb = 0, 0, 0
    if (h < 60):
        rr,gg,bb = c,x,0
    elif (h < 120):
        rr,gg,bb = x,c,0
    elif (h < 180):
        rr,gg,bb = 0,c,x
    elif (h < 240):
        rr,gg,bb = 0,x,c
    elif (h < 300):
        rr,gg,bb = x,0,c
    else:
        rr,gg,bb = c,0,x
    return int((rr + m) * 255), int((gg + m) * 255), int((bb + m) * 255)

def cmyk_to_rgb(c, m, y, k):
    c = c / 100
    m = m / 100
    y = y / 100
    k = k / 100
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose a color")
    if color_code:
        rgb = color_code[0]
        update_labels(rgb)

def update_labels(rgb):
    r, g, b = map(int, rgb)
    rgb_entries[0].delete(0, tk.END)
    rgb_entries[0].insert(0, str(r))
    rgb_entries[1].delete(0, tk.END)
    rgb_entries[1].insert(0, str(g))
    rgb_entries[2].delete(0, tk.END)
    rgb_entries[2].insert(0, str(b))

    h, l, s = rgb_to_hls(r, g, b)
    hls_entries[0].delete(0, tk.END)
    hls_entries[0].insert(0, str(h))
    hls_entries[1].delete(0, tk.END)
    hls_entries[1].insert(0, str(l))
    hls_entries[2].delete(0, tk.END)
    hls_entries[2].insert(0, str(s))

    c, m, y, k = rgb_to_cmyk(r, g, b)
    cmyk_entries[0].delete(0, tk.END)
    cmyk_entries[0].insert(0, str(c))
    cmyk_entries[1].delete(0, tk.END)
    cmyk_entries[1].insert(0, str(m))
    cmyk_entries[2].delete(0, tk.END)
    cmyk_entries[2].insert(0, str(y))
    cmyk_entries[3].delete(0, tk.END)
    cmyk_entries[3].insert(0, str(k))
    
    update_sliders(r,g,b,h,l,s,c,m,y,k)
    color_display.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    
def update_sliders(r,g,b, h, l,s, c, m, y, k):
    rgb_sliders[0].set(r)
    rgb_sliders[1].set(g)
    rgb_sliders[2].set(b)
    hls_sliders[0].set(h)
    hls_sliders[1].set(l)
    hls_sliders[2].set(s)
    cmyk_sliders[0].set(c)
    cmyk_sliders[1].set(m)
    cmyk_sliders[2].set(y)
    cmyk_sliders[3].set(k)
    
def update_from_rgb():
    r, g, b = int(rgb_entries[0].get()), int(rgb_entries[1].get()), int(rgb_entries[2].get())
    update_labels((r,g,b))
    
def update_from_hls():
    h,l,s = float(hls_entries[0].get()), float(hls_entries[1].get()), float(hls_entries[2].get())
    r,g,b = hls_to_rgb(h,l,s)
    
    rgb_entries[0].delete(0, tk.END)
    rgb_entries[0].insert(0, str(r))
    rgb_entries[1].delete(0, tk.END)
    rgb_entries[1].insert(0, str(g))
    rgb_entries[2].delete(0, tk.END)
    rgb_entries[2].insert(0, str(b))

    c, m, y, k = rgb_to_cmyk(r, g, b)
    cmyk_entries[0].delete(0, tk.END)
    cmyk_entries[0].insert(0, str(c))
    cmyk_entries[1].delete(0, tk.END)
    cmyk_entries[1].insert(0, str(m))
    cmyk_entries[2].delete(0, tk.END)
    cmyk_entries[2].insert(0, str(y))
    cmyk_entries[3].delete(0, tk.END)
    cmyk_entries[3].insert(0, str(k))
    
    update_sliders(r,g,b,h,l,s,c,m,y,k)
    color_display.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    
def update_from_slider_cmyk():
    for i in range(4):
        cmyk_entries[i].delete(0, tk.END)
        cmyk_entries[i].insert(0, str(cmyk_sliders[i].get()))
    update_from_cmyk()
    
def update_from_slider_hls():
    for i in range(3):
        hls_entries[i].delete(0, tk.END)
        hls_entries[i].insert(0, str(hls_sliders[i].get()))
    update_from_hls()
    
def update_from_slider_rgb():
    for i in range(3):
        rgb_entries[i].delete(0, tk.END)
        rgb_entries[i].insert(0, str(rgb_sliders[i].get()))
    update_from_rgb()
    
def update_from_cmyk():
    c,m,y,k = float(cmyk_entries[0].get()), float(cmyk_entries[1].get()), float(cmyk_entries[2].get()), float(cmyk_entries[3].get())
    r,g,b = cmyk_to_rgb(c,m,y,k)
    rgb_entries[0].delete(0, tk.END)
    rgb_entries[0].insert(0, str(r))
    rgb_entries[1].delete(0, tk.END)
    rgb_entries[1].insert(0, str(g))
    rgb_entries[2].delete(0, tk.END)
    rgb_entries[2].insert(0, str(b))

    h, l, s = rgb_to_hls(r, g, b)
    hls_entries[0].delete(0, tk.END)
    hls_entries[0].insert(0, str(h))
    hls_entries[1].delete(0, tk.END)
    hls_entries[1].insert(0, str(l))
    hls_entries[2].delete(0, tk.END)
    hls_entries[2].insert(0, str(s))
    
    update_sliders(r,g,b,h,l,s,c,m,y,k)
    color_display.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    
app = tk.Tk()
app.title("Color Picker")

color_display = tk.Label(app, text="", width=20, height=2)
color_display.pack(pady=10)

rgb_frame = tk.Frame(app)
rgb_frame.pack()
tk.Label(rgb_frame, text="RGB:").grid(row=0, column=0)
rgb_entries = [tk.Entry(rgb_frame, width=7) for num in range(3)]
rgb_sliders = [tk.Scale(rgb_frame, from_=0, to_ = 255, orient = "horizontal") for _ in range(3)]
for i, entry in enumerate(rgb_entries):
    entry.grid(row=i+1, column=0, sticky='W')
    entry.bind("<Return>", lambda _: update_from_rgb())
for i, entry in enumerate(rgb_sliders):
    entry.grid(row=i+1, column=1, ipady=10)
    entry.bind("<ButtonRelease-1>", lambda _: update_from_slider_rgb())

hls_frame = tk.Frame(app)
hls_frame.pack()
tk.Label(hls_frame, text="HLS:").grid(row=0, column=0)
hls_entries = [tk.Entry(hls_frame, width=7) for _ in range(3)]
hls_sliders = [tk.Scale(hls_frame, from_=0, to_ = 360 if (_ == 0) else 100, orient = "horizontal") for _ in range(3)]
for i, entry in enumerate(hls_entries):
    entry.grid(row=i+1, column=0)
    entry.bind("<Return>", lambda _: update_from_hls())
for i, entry in enumerate(hls_sliders):
    entry.grid(row=i+1, column=1, ipady = 10)
    entry.bind("<ButtonRelease-1>", lambda _: update_from_slider_hls())

cmyk_frame = tk.Frame(app)
cmyk_frame.pack()
tk.Label(cmyk_frame, text="CMYK:").grid(row=0, column=0)
cmyk_entries = [tk.Entry(cmyk_frame, width=7) for _ in range(4)]
cmyk_sliders = [tk.Scale(cmyk_frame, from_=0, to_ = 100, orient = "horizontal") for _ in range(4)]
for i, entry in enumerate(cmyk_entries):
    entry.grid(row=i+1, column=0)
    entry.bind("<Return>", lambda _: update_from_cmyk())
for i, entry in enumerate(cmyk_sliders):
    entry.grid(row=i+1, column=1, ipady = 10)
    entry.bind("<ButtonRelease-1>", lambda _: update_from_slider_cmyk())

choose_color_button = tk.Button(app, text="Choose Color", command=choose_color)
choose_color_button.pack(pady=20)
update_labels((255,0,0))
app.mainloop()