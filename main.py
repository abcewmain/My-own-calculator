import tkinter as tk


BG = "midnightblue"
CASE = "darkslategray"
PANEL = "darkslategray"
DISPLAY = "lemonchiffon"
INK = "darkslategray"
ACCENT = "coral"
KEY = "ivory"
KEY_ALT = "lightcyan"
KEY_ACTION = "gold"


class RetroCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Calculator")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.current = "0"
        self.stored = None
        self.operation = None
        self.replace_entry = False
        self.history = tk.StringVar(value="READY WHEN YOU ARE")
        self.display = tk.StringVar(value=self.current)

        body = tk.Frame(root, bg=CASE, padx=18, pady=18)
        body.pack(padx=18, pady=18)

        brand = tk.Label(
            body,
            text="POCKET  •  ELECTRIC",
            bg=CASE,
            fg="lemonchiffon",
            font=("Courier New", 11, "bold"),
        )
        brand.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        screen = tk.Frame(body, bg=DISPLAY, padx=12, pady=10, bd=3, relief="sunken")
        screen.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 16))

        history_label = tk.Label(
            screen,
            textvariable=self.history,
            bg=DISPLAY,
            fg="slategray",
            font=("Courier New", 9),
            anchor="e",
        )
        history_label.pack(fill="x")

        display_label = tk.Label(
            screen,
            textvariable=self.display,
            bg=DISPLAY,
            fg=INK,
            font=("Courier New", 30, "bold"),
            anchor="e",
            width=12,
        )
        display_label.pack(fill="x")

        keys = [
            ("C", "clear", KEY_ACTION),
            ("±", "sign", KEY_ALT),
            ("%", "percent", KEY_ALT),
            ("÷", "/", KEY_ACTION),
            ("7", "7", KEY),
            ("8", "8", KEY),
            ("9", "9", KEY),
            ("×", "*", KEY_ACTION),
            ("4", "4", KEY),
            ("5", "5", KEY),
            ("6", "6", KEY),
            ("−", "-", KEY_ACTION),
            ("1", "1", KEY),
            ("2", "2", KEY),
            ("3", "3", KEY),
            ("+", "+", KEY_ACTION),
            ("⌫", "backspace", KEY_ALT),
            ("0", "0", KEY),
            (".", ".", KEY),
            ("=", "equals", ACCENT),
        ]

        for index, (label, action, color) in enumerate(keys):
            row = index // 4 + 2
            column = index % 4
            button = tk.Button(
                body,
                text=label,
                command=lambda value=action: self.press(value),
                bg=color,
                fg=INK,
                activebackground="white",
                activeforeground=INK,
                font=("Courier New", 16, "bold"),
                relief="raised",
                bd=3,
                width=4,
                height=2,
                takefocus=False,
            )
            button.grid(row=row, column=column, padx=4, pady=4, sticky="nsew")

        footer = tk.Label(
            body,
            text="BATTERY-FREE • ALL THE RIGHT KEYS",
            bg=CASE,
            fg="lightcyan",
            font=("Courier New", 8),
        )
        footer.grid(row=7, column=0, columnspan=4, pady=(12, 0))

        self.root.bind("<Key>", self.handle_key)

    def press(self, action):
        if action.isdigit():
            self.enter_digit(action)
        elif action == ".":
            self.enter_decimal()
        elif action in ("+", "-", "*", "/"):
            self.choose_operation(action)
        elif action == "equals":
            self.calculate()
        elif action == "clear":
            self.clear()
        elif action == "sign":
            self.toggle_sign()
        elif action == "percent":
            self.apply_percent()
        elif action == "backspace":
            self.backspace()

    def enter_digit(self, digit):
        if self.replace_entry or self.current == "0" or self.current == "ERROR":
            self.current = digit
            self.replace_entry = False
        elif len(self.current) < 12:
            self.current += digit
        self.update_display()

    def enter_decimal(self):
        if self.replace_entry or self.current == "ERROR":
            self.current = "0."
            self.replace_entry = False
        elif "." not in self.current:
            self.current += "."
        self.update_display()

    def choose_operation(self, operation):
        if self.current == "ERROR":
            self.clear()
        value = float(self.current)
        if self.operation is not None and not self.replace_entry:
            if not self.perform_calculation(value):
                return
            value = float(self.current)
        self.stored = value
        self.operation = operation
        self.history.set(f"{self.format_number(value)} {self.operation_symbol(operation)}")
        self.replace_entry = True

    def calculate(self):
        if self.operation is None or self.stored is None:
            return
        left = self.stored
        right = float(self.current)
        symbol = self.operation_symbol(self.operation)
        if self.perform_calculation(right):
            self.history.set(f"{self.format_number(left)} {symbol} {self.format_number(right)} =")
            self.operation = None
            self.stored = None
            self.replace_entry = True

    def perform_calculation(self, right):
        left = self.stored
        if left is None or self.operation is None:
            return False
        if self.operation == "+":
            result = left + right
        elif self.operation == "-":
            result = left - right
        elif self.operation == "*":
            result = left * right
        elif self.operation == "/":
            if right == 0:
                self.current = "ERROR"
                self.history.set("CANNOT DIVIDE BY ZERO")
                self.operation = None
                self.stored = None
                self.replace_entry = True
                self.update_display()
                return False
            result = left / right
        else:
            return False
        self.current = self.format_number(result)
        self.stored = result
        self.replace_entry = True
        self.update_display()
        return True

    def toggle_sign(self):
        if self.current not in ("0", "ERROR"):
            self.current = self.format_number(-float(self.current))
            self.update_display()

    def apply_percent(self):
        if self.current != "ERROR":
            self.current = self.format_number(float(self.current) / 100)
            self.replace_entry = True
            self.update_display()

    def backspace(self):
        if self.replace_entry or self.current == "ERROR":
            self.current = "0"
            self.replace_entry = False
        else:
            self.current = self.current[:-1]
            if self.current in ("", "-"):
                self.current = "0"
        self.update_display()

    def clear(self):
        self.current = "0"
        self.stored = None
        self.operation = None
        self.replace_entry = False
        self.history.set("READY WHEN YOU ARE")
        self.update_display()

    def update_display(self):
        shown = self.current
        if len(shown) > 12:
            shown = f"{float(shown):.6g}"
        self.display.set(shown)

    @staticmethod
    def format_number(value):
        if value == 0:
            return "0"
        if abs(value) >= 1e12 or abs(value) < 1e-8:
            return f"{value:.6g}"
        return f"{value:.10f}".rstrip("0").rstrip(".")

    @staticmethod
    def operation_symbol(operation):
        return {"+": "+", "-": "−", "*": "×", "/": "÷"}[operation]

    def handle_key(self, event):
        if event.char.isdigit() or event.char == ".":
            self.press(event.char)
        elif event.char in ("+", "-", "*", "/"):
            self.press(event.char)
        elif event.char in ("=", "\r"):
            self.press("equals")
        elif event.keysym == "BackSpace":
            self.press("backspace")
        elif event.keysym == "Escape":
            self.press("clear")


def main():
    root = tk.Tk()
    RetroCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
