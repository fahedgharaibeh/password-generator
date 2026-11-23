import secrets
import string
import tkinter as tk
from tkinter import messagebox

MIN_LENGTH = 8
DEFAULT_LENGTH = 10
SYMBOLS = "!@#$%^&*()-_=+[]{}"
SYS_RAND = secrets.SystemRandom()


def build_password(upper_count, lower_count, digits_count, symbols_count):
    pool = []

    for _ in range(upper_count):
        pool.append(secrets.choice(string.ascii_uppercase))

    for _ in range(lower_count):
        pool.append(secrets.choice(string.ascii_lowercase))

    for _ in range(digits_count):
        pool.append(secrets.choice(string.digits))

    for _ in range(symbols_count):
        pool.append(secrets.choice(SYMBOLS))

    SYS_RAND.shuffle(pool)
    return "".join(pool)


def parse_optional_int(raw_value, field_name):
    cleaned = raw_value.strip()
    if cleaned == "":
        return None
    try:
        val = int(cleaned)
    except ValueError:
        raise ValueError(f"'{field_name}' must be a valid whole number.")
    if val < 0:
        raise ValueError(f"'{field_name}' cannot be negative.")
    return val


def handle_generate():
    try:
        upper_in = parse_optional_int(upper_entry.get(), "Uppercase")
        lower_in = parse_optional_int(lower_entry.get(), "Lowercase")
        digits_in = parse_optional_int(digits_entry.get(), "Digits")
        symbols_in = parse_optional_int(symbols_entry.get(), "Symbols")
    except ValueError as err:
        messagebox.showerror("Invalid Input", str(err))
        return

    if upper_in is None and lower_in is None and digits_in is None and symbols_in is None:
        upper_count = 2
        lower_count = 4
        digits_count = 2
        symbols_count = 2
        total_len = upper_count + lower_count + digits_count + symbols_count

        password = build_password(upper_count, lower_count, digits_count, symbols_count)
        set_password_output(password)
        status_label.config(
            text=(
                f"Default password (len {total_len}): "
                f"{upper_count} uppercase, {lower_count} lowercase, {digits_count} digits, {symbols_count} symbols."
            ),
            fg="#38bdf8",
        )
        return

    upper_count = 0 if upper_in is None else upper_in
    lower_count = 0 if lower_in is None else lower_in
    digits_count = 0 if digits_in is None else digits_in
    symbols_count = 0 if symbols_in is None else symbols_in

    total_len = upper_count + lower_count + digits_count + symbols_count

    if total_len < MIN_LENGTH:
        messagebox.showwarning(
            "Length Too Short",
            f"Total length is {total_len}. Please increase the counts so the total length is at least {MIN_LENGTH}.",
        )
        status_label.config(
            text=f"Minimum total length is {MIN_LENGTH} (current total: {total_len}).",
            fg="#f87171",
        )
        return

    if upper_count < 1:
        messagebox.showwarning(
            "Uppercase Required",
            "Uppercase count must be at least 1.",
        )
        status_label.config(
            text="Please set Uppercase count to at least 1.",
            fg="#fbbf24",
        )
        return

    password = build_password(upper_count, lower_count, digits_count, symbols_count)
    set_password_output(password)
    status_label.config(
        text=(
            f"Generated password (len {total_len}): "
            f"{upper_count} uppercase, {lower_count} lowercase, {digits_count} digits, {symbols_count} symbols."
        ),
        fg="#4ade80",
    )


def set_password_output(password):
    output_entry.config(state="normal")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, password)
    output_entry.config(state="readonly")


def copy_password():
    pwd = output_entry.get()
    if not pwd:
        messagebox.showinfo("Nothing to Copy", "Generate a password first.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    status_label.config(text="Password copied to clipboard.", fg="#38bdf8")


def clear_fields():
    upper_entry.delete(0, tk.END)
    lower_entry.delete(0, tk.END)
    digits_entry.delete(0, tk.END)
    symbols_entry.delete(0, tk.END)
    output_entry.config(state="normal")
    output_entry.delete(0, tk.END)
    output_entry.config(state="readonly")
    status_label.config(
        text="Leave all fields blank for a default 10-character password (min length: 8).",
        fg="#94a3b8",
    )

root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("520x455")
root.resizable(False, False)
root.configure(bg="#0f172a")

header_frame = tk.Frame(root, bg="#0f172a")
header_frame.pack(fill="x", padx=24, pady=(20, 10))

tk.Label(
    header_frame,
    text="Password Generator",
    font=("Segoe UI", 20, "bold"),
    bg="#0f172a",
    fg="#f8fafc",
    anchor="w",
).pack(fill="x")

tk.Label(
    header_frame,
    text="Min total length: 8  |  Default (if blank): 10  |  At least 1 uppercase required",
    font=("Segoe UI", 9),
    bg="#0f172a",
    fg="#94a3b8",
    anchor="w",
).pack(fill="x", pady=(2, 0))

card = tk.Frame(
    root,
    bg="#1e293b",
    highlightbackground="#334155",
    highlightthickness=1,
    padx=18,
    pady=16,
)
card.pack(fill="x", padx=24, pady=10)

grid_frame = tk.Frame(card, bg="#1e293b")
grid_frame.pack(fill="x")

entry_style = {
    "width": 10,
    "font": ("Consolas", 12, "bold"),
    "justify": "center",
    "bg": "#0f172a",
    "fg": "#f8fafc",
    "insertbackground": "#38bdf8",
    "relief": "flat",
    "highlightbackground": "#475569",
    "highlightthickness": 1,
}

label_style = {
    "font": ("Segoe UI", 11),
    "bg": "#1e293b",
    "fg": "#e2e8f0",
    "anchor": "w",
}

hint_style = {
    "font": ("Segoe UI", 9),
    "bg": "#1e293b",
    "fg": "#94a3b8",
    "anchor": "w",
}

tk.Label(grid_frame, text="Uppercase Count", **label_style).grid(row=0, column=0, sticky="w", pady=5)
tk.Label(grid_frame, text="(A-Z, min 1 when set)", **hint_style).grid(row=0, column=1, sticky="w", padx=(8, 12))
upper_entry = tk.Entry(grid_frame, **entry_style)
upper_entry.grid(row=0, column=2, pady=5, ipady=3)

tk.Label(grid_frame, text="Lowercase Count", **label_style).grid(row=1, column=0, sticky="w", pady=5)
tk.Label(grid_frame, text="(a-z)", **hint_style).grid(row=1, column=1, sticky="w", padx=(8, 12))
lower_entry = tk.Entry(grid_frame, **entry_style)
lower_entry.grid(row=1, column=2, pady=5, ipady=3)

tk.Label(grid_frame, text="Digits Count", **label_style).grid(row=2, column=0, sticky="w", pady=5)
tk.Label(grid_frame, text="(0-9)", **hint_style).grid(row=2, column=1, sticky="w", padx=(8, 12))
digits_entry = tk.Entry(grid_frame, **entry_style)
digits_entry.grid(row=2, column=2, pady=5, ipady=3)
 
tk.Label(grid_frame, text="Symbols Count", **label_style).grid(row=3, column=0, sticky="w", pady=5)
tk.Label(grid_frame, text="(!@#$%^&*...)", **hint_style).grid(row=3, column=1, sticky="w", padx=(8, 12))
symbols_entry = tk.Entry(grid_frame, **entry_style)
symbols_entry.grid(row=3, column=2, pady=5, ipady=3)

actions_frame = tk.Frame(root, bg="#0f172a")
actions_frame.pack(fill="x", padx=24, pady=(8, 6))

tk.Button(
    actions_frame,
    text="Generate Password",
    font=("Segoe UI", 11, "bold"),
    bg="#2563eb",
    fg="#ffffff",
    activebackground="#1d4ed8",
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    padx=18,
    pady=8,
    command=handle_generate,
).pack(side="left")

tk.Button(
    actions_frame,
    text="Clear",
    font=("Segoe UI", 10, "bold"),
    bg="#334155",
    fg="#e2e8f0",
    activebackground="#475569",
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    padx=14,
    pady=8,
    command=clear_fields,
).pack(side="right")

output_frame = tk.Frame(root, bg="#0f172a")
output_frame.pack(fill="x", padx=24, pady=(10, 6))

output_entry = tk.Entry(
    output_frame,
    font=("Consolas", 13, "bold"),
    justify="center",
    state="readonly",
    readonlybackground="#1e293b",
    fg="#4ade80",
    relief="flat",
    highlightbackground="#334155",
    highlightthickness=1,
)
output_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))

tk.Button(
    output_frame,
    text="Copy",
    font=("Segoe UI", 10, "bold"),
    bg="#16a34a",
    fg="#ffffff",
    activebackground="#15803d",
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=7,
    command=copy_password,
).pack(side="right")

status_label = tk.Label(
    root,
    text="Leave all fields blank for a default 10-character password (min length: 8).",
    font=("Segoe UI", 9),
    bg="#0f172a",
    fg="#94a3b8",
    wraplength=472,
    justify="left",
)
status_label.pack(fill="x", padx=24, pady=(8, 0))

root.mainloop()