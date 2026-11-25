import math
import os
import random
import sys
import tkinter as tk
import tkinter.font as tkfont

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # crisp rendering on high DPI screens
except Exception:
    pass

BASE_W, BASE_H = 620, 930
FONT = "Tahoma"

# (wood stripe 1, wood stripe 2, shape color, price text color, title color)
PALETTES = [
    ("#c98f52", "#b47838", "#14164f", "#e0262d", "#b3141b"),  # classic wood
    ("#a9b57a", "#8d9a5e", "#12402f", "#e0262d", "#0f3d2a"),  # forest
    ("#7fb7d9", "#5f9cc2", "#0b2f57", "#e0262d", "#0b2f57"),  # ocean
    ("#b99ad6", "#9d7cc0", "#2c1450", "#c4161c", "#3a1a66"),  # purple
    ("#e3a1a8", "#cf838c", "#5a1230", "#d3202a", "#7a1236"),  # rose
    ("#8a5a33", "#6e4524", "#0e1b3d", "#e0262d", "#3b1f0a"),  # dark oak
    ("#e8a24a", "#d18a32", "#1b2a6b", "#d3202a", "#7a2a00"),  # orange
    ("#4a4a4a", "#3a3a3a", "#101010", "#e0262d", "#1a1a1a"),  # dark
]


def pick_palette():
    """Pick a different palette on every launch (remembers the last one)."""
    store_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "AlansarPrices")
    store = os.path.join(store_dir, "last_palette.txt")
    last = -1
    try:
        with open(store, encoding="utf-8") as fh:
            last = int(fh.read().strip())
    except Exception:
        pass
    choices = [i for i in range(len(PALETTES)) if i != last]
    index = random.choice(choices)
    try:
        os.makedirs(store_dir, exist_ok=True)
        with open(store, "w", encoding="utf-8") as fh:
            fh.write(str(index))
    except Exception:
        pass
    return PALETTES[index]


WOOD1, WOOD2, NAVY, RED, TITLE = pick_palette()

root = tk.Tk()
root.title("Alansar - Digital Print Prices")
try:
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    root.iconbitmap(os.path.join(base_dir, "icon.ico"))
except tk.TclError:
    pass
root.geometry("620x930")
root.minsize(340, 520)

cv = tk.Canvas(root, highlightthickness=0, bg=WOOD1)
cv.pack(fill="both", expand=True)

probe = tkfont.Font(family=FONT, size=-100, weight="bold")
st = {"sx": 1.0, "sy": 1.0, "job": None, "toast": None}
hits = []  # clickable areas: (kind, cx, cy, half_w, half_h, text)


def fit(s, w_px, h_px, w_frac, h_frac):
    """Largest font size (in pixels) so the text fits inside the given area."""
    lines = s.split("\n")
    w100 = max(probe.measure(line) for line in lines) or 1
    h100 = probe.metrics("linespace") * len(lines)
    return min(w_frac * w_px / w100, h_frac * h_px / h100) * 100


def build_items():
    items = []

    def add(kind, cx, cy, w, h, s, group, fill=RED, stroke="white", icon=None, mode="center"):
        items.append(dict(kind=kind, cx=cx, cy=cy, w=w, h=h, s=s, group=group, fill=fill, stroke=stroke, icon=icon, mode=mode))

    add("free", 310, 45, 420, 62, "الأنصار", "title", TITLE)
    add("free", 310, 100, 420, 36, "أسعار الطباعة الديجيتال", "subtitle", TITLE)

    label_x = 535
    cols = [415, 305, 195, 85]
    add("oval", (cols[0] + cols[1]) / 2, 165, 230, 58, "ربع 33 × 48,7", "size")
    add("oval", (cols[2] + cols[3]) / 2, 165, 230, 58, "ربع جاير 33 × 44", "size")
    for i, t in enumerate(["وجه (1)", "وجهين", "وجه (1)", "وجهين"]):
        add("oval", cols[i], 232, 100, 42, t, "sub")

    rows = [
        ("٣٠٠ جرام", ["١٠", "١٢,٥٠", "١٠", "١٢"]),
        ("٢٥٠ جرام", ["٩,٤٥", "١١,٩٥", "٩,٣٠", "١١,٧٠"]),
        ("٢٠٠ جرام", ["٩,٢٠", "١١,٤٠", "٨,٩٠", "١١,١٥"]),
        ("١٥٠ جرام", ["٧,٤٠", "٩,٧٠", "٧,١٠", "٩,١٠"]),
    ]
    y = 300
    for label, prices in rows:
        add("oval", label_x, y, 112, 52, label, "label")
        for cx, p in zip(cols, prices):
            add("oval", cx, y, 100, 50, p, "price")
        y += 66

    add("rect", 535, 575, 112, 54, "استيكر", "sticker")
    add("rect", 245, 575, 440, 54, "من ١:١٠ سعر الورقة ١٠ ج\nأكثر من ١٠ الورقة ٩,٢٥ ج", "banner")

    add("rect", 512, 650, 196, 60, "الكروت الشخصية\nشاملة ( قص + سلوفان )", "info")
    add("rect", 310, 650, 196, 60, "السلوفان\nلامع – مط", "info")
    add("rect", 512, 740, 196, 84, "١٠٠ كارت وجه ٦٠ ج\n١٠٠ كارت وجهين ٧٥ ج", "info")
    add("rect", 310, 740, 196, 84, "من ١:١٠ ورقة ثابت ١٠ جنية\nوما بعد ذلك ١,٢٥ ج للوجه", "info")
    add("rect", 108, 740, 196, 84, "وش ١٠ جنية\nوش وضهر ١٥ جنيه", "info")

    # contact rows: left group touches the left margin, right group the right margin, mail is centered
    add("free", 30, 830, 265, 34, "01227348588 - 01282133300", "contact", "white", "black", "whatsapp", "left")
    add("free", 590, 830, 120, 34, "27790695", "contact", "white", "black", "phone", "right")
    add("free", 310, 880, 260, 34, "Accploting@gmail.com", "contact", "white", "black", "mail", "center")
    return items


def draw_icon(kind, ix, cy, px):
    d = px * 1.35
    sym_font = ("Segoe UI Symbol", -int(d * 0.62), "bold")
    bw = max(2, round(px * 0.09))
    if kind == "whatsapp":
        cv.create_oval(ix - d / 2, cy - d / 2, ix + d / 2, cy + d / 2, fill="#25D366", outline="white", width=bw)
        cv.create_text(ix, cy, text="\u2706", font=sym_font, fill="white")
    elif kind == "mail":
        cv.create_rectangle(ix - d / 2, cy - d / 2, ix + d / 2, cy + d / 2, fill="#d32f2f", outline="white", width=bw)
        cv.create_text(ix, cy, text="\u2709", font=sym_font, fill="white")
    elif kind == "phone":
        r = max(1, round(px * 0.05))
        for k in range(8):
            a = 2 * math.pi * k / 8
            cv.create_text(ix + r * math.cos(a), cy + r * math.sin(a), text="\u260E",
                           font=("Segoe UI Symbol", -int(d * 0.95), "bold"), fill="black")
        cv.create_text(ix, cy, text="\u260E", font=("Segoe UI Symbol", -int(d * 0.95), "bold"), fill="white")


def draw():
    cw, ch = max(cv.winfo_width(), 1), max(cv.winfo_height(), 1)
    sx, sy = cw / BASE_W, ch / BASE_H
    cv.delete("all")
    hits.clear()

    # wood background fills the whole window
    step = max(14, 46 * sx)
    x = 0.0
    while x < cw:
        cv.create_rectangle(x, 0, x + step * 0.87, ch, fill=WOOD1, outline="")
        cv.create_rectangle(x + step * 0.87, 0, x + step, ch, fill=WOOD2, outline="")
        x += step

    items = build_items()

    # font size per item, then the smallest size inside each group so similar items match
    group_size = {}
    for it in items:
        w_px, h_px = it["w"] * sx, it["h"] * sy
        if it["kind"] == "oval":
            size = fit(it["s"], w_px, h_px, 0.72, 0.52)
        elif it["kind"] == "rect":
            size = fit(it["s"], w_px, h_px, 0.88, 0.70)
        else:
            size = fit(it["s"], w_px, h_px, 0.98, 0.85)
        it["size"] = size
        group_size[it["group"]] = min(group_size.get(it["group"], 1e9), size)

    border = max(2, round(3 * min(sx, sy)))
    for it in items:
        cx, cy = it["cx"] * sx, it["cy"] * sy
        hw, hh = it["w"] * sx / 2, it["h"] * sy / 2
        if it["kind"] == "oval":
            cv.create_oval(cx - hw, cy - hh, cx + hw, cy + hh, fill=NAVY, outline="white", width=border)
            if it["group"] == "price":
                hits.append(("oval", cx, cy, hw, hh, it["s"]))
        elif it["kind"] == "rect":
            cv.create_rectangle(cx - hw, cy - hh, cx + hw, cy + hh, fill=NAVY, outline="white", width=border)

    for it in items:
        px = max(8, int(group_size[it["group"]]))
        font = (FONT, -px, "bold")
        cx, cy = it["cx"] * sx, it["cy"] * sy
        icon_x = None
        if it["icon"]:
            tw = probe.measure(it["s"]) * px / 100
            d = px * 1.35
            gap = px * 0.35
            group_w = d + gap + tw
            if it["mode"] == "left":
                x0 = cx
            elif it["mode"] == "right":
                x0 = cx - group_w
            else:
                x0 = cx - group_w / 2
            icon_x = x0 + d / 2
            text_left = x0 + d + gap
            idx = 0
            for part in it["s"].split(" - "):
                pos = it["s"].find(part, idx)
                part_x = text_left + probe.measure(it["s"][:pos]) * px / 100
                part_w = probe.measure(part) * px / 100
                hits.append(("rect", part_x + part_w / 2, cy, part_w / 2 + 2, px * 0.9, part))
                idx = pos + len(part)
            cx = x0 + d + gap + tw / 2
        r = max(1, round(px * 0.06))
        for k in range(12):
            a = 2 * math.pi * k / 12
            cv.create_text(cx + r * math.cos(a), cy + r * math.sin(a), text=it["s"], font=font,
                           fill=it["stroke"], justify="center")
        cv.create_text(cx, cy, text=it["s"], font=font, fill=it["fill"], justify="center")
        if icon_x is not None:
            draw_icon(it["icon"], icon_x, cy, px)


def find_hit(x, y):
    for kind, cx, cy, hw, hh, value in reversed(hits):
        if kind == "oval":
            if hw and hh and ((x - cx) / hw) ** 2 + ((y - cy) / hh) ** 2 <= 1:
                return value
        elif abs(x - cx) <= hw and abs(y - cy) <= hh:
            return value
    return None


def show_toast():
    if st["toast"]:
        root.after_cancel(st["toast"])
    cv.delete("toast")
    cw, ch = cv.winfo_width(), cv.winfo_height()
    px = max(14, int(min(st["sx"], st["sy"]) * 20))
    cv.create_rectangle(cw / 2 - px * 4, ch - px * 3, cw / 2 + px * 4, ch - px * 1.2,
                        fill="black", outline="white", width=2, tags="toast")
    cv.create_text(cw / 2, ch - px * 2.1, text="تم النسخ", fill="white",
                   font=(FONT, -px, "bold"), tags="toast")
    st["toast"] = root.after(1200, lambda: cv.delete("toast"))


def on_click(event):
    value = find_hit(event.x, event.y)
    if value is None:
        return
    root.clipboard_clear()
    root.clipboard_append(value.replace("\n", " - "))
    root.update()  # keeps the clipboard content after the app closes
    show_toast()


def on_motion(event):
    cv.configure(cursor="hand2" if find_hit(event.x, event.y) is not None else "")


def schedule(_event=None):
    if st["job"]:
        root.after_cancel(st["job"])
    st["job"] = root.after(30, draw)


cv.bind("<Configure>", schedule)
cv.bind("<Button-1>", on_click)
cv.bind("<Motion>", on_motion)
root.mainloop()
