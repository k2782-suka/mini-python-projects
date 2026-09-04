import tkinter as tk
import math
import ast
import operator as op


OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos
}


def safe_eval(expression):
    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    tree = ast.parse(expression, mode="eval")
    return calculate_node(tree.body)


def calculate_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError()

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        if type(node.op) not in OPERATORS:
            raise ValueError()

        left = calculate_node(node.left)
        right = calculate_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError()

        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in OPERATORS:
            raise ValueError()

        return OPERATORS[type(node.op)](
            calculate_node(node.operand)
        )

    raise ValueError()


class OldCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULATOR")
        self.root.geometry("460x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#101510")

        self.expression = ""
        self.memory = 0
        self.display_var = tk.StringVar(value="0")

        self.create_interface()
        self.bind_keys()

    def create_interface(self):
        top_frame = tk.Frame(
            self.root,
            bg="#101510",
            highlightbackground="#244d2a",
            highlightthickness=2
        )
        top_frame.pack(fill="x", padx=12, pady=(12, 5))

        title = tk.Label(
            top_frame,
            text="CALCULATOR",
            font=("Courier New", 11, "bold"),
            fg="#55ff66",
            bg="#101510"
        )
        title.pack(anchor="w", padx=8, pady=(5, 0))

        self.display = tk.Entry(
            top_frame,
            textvariable=self.display_var,
            font=("Courier New", 30, "bold"),
            justify="right",
            fg="#66ff66",
            bg="#000000",
            insertbackground="#66ff66",
            relief="sunken",
            bd=5
        )
        self.display.pack(fill="x", padx=7, pady=8, ipady=8)
        self.display.configure(state="readonly")

        buttons_frame = tk.Frame(
            self.root,
            bg="#101510"
        )
        buttons_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=8
        )

        buttons = [
            ["MC", "MR", "MS", "M+", "M-"],
            ["sin", "cos", "tan", "√", "x²"],
            ["(", ")", "%", "⌫", "C"],
            ["7", "8", "9", "÷", "±"],
            ["4", "5", "6", "×", "1/x"],
            ["1", "2", "3", "-", "="],
            ["0", ".", "00", "+", "π"]
        ]

        for row_index, row in enumerate(buttons):
            buttons_frame.rowconfigure(
                row_index,
                weight=1
            )

            for col_index in range(5):
                buttons_frame.columnconfigure(
                    col_index,
                    weight=1
                )

            for col_index, text in enumerate(row):
                button = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Courier New", 15, "bold"),
                    fg=self.get_foreground(text),
                    bg=self.get_background(text),
                    activeforeground="#ffffff",
                    activebackground="#2c913b",
                    relief="raised",
                    bd=3,
                    cursor="hand2",
                    command=lambda value=text: self.press(value)
                )

                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

        self.status = tk.Label(
            self.root,
            text="READY",
            anchor="w",
            font=("Courier New", 10),
            fg="#55ff66",
            bg="#101510"
        )
        self.status.pack(
            fill="x",
            padx=15,
            pady=(0, 8)
        )

    def get_background(self, text):
        if text == "C":
            return "#6c1111"

        if text == "=":
            return "#165d24"

        if text in [
            "+", "-", "×", "÷", "±",
            "%", "√", "x²", "1/x"
        ]:
            return "#193d20"

        if text in ["MC", "MR", "MS", "M+", "M-"]:
            return "#263329"

        return "#172119"

    def get_foreground(self, text):
        if text == "C":
            return "#ff7777"

        if text == "=":
            return "#8aff8a"

        return "#baffba"

    def update_display(self, value=None):
        if value is not None:
            self.display_var.set(str(value))
        else:
            if self.expression:
                self.display_var.set(self.expression)
            else:
                self.display_var.set("0")

    def press(self, value):
        try:
            if value == "C":
                self.expression = ""
                self.update_display()
                self.status.config(text="CLEARED")
                return

            if value == "⌫":
                self.expression = self.expression[:-1]
                self.update_display()
                return

            if value == "=":
                self.calculate()
                return

            if value == "±":
                self.toggle_sign()
                return

            if value == "√":
                self.add_function("sqrt")
                return

            if value == "x²":
                self.expression += "^2"
                self.update_display()
                return

            if value == "1/x":
                self.expression = f"1/({self.expression})"
                self.update_display()
                return

            if value == "π":
                self.expression += str(math.pi)
                self.update_display()
                return

            if value == "MC":
                self.memory = 0
                self.status.config(text="MEMORY CLEARED")
                return

            if value == "MR":
                self.expression += str(self.memory)
                self.update_display()
                return

            if value == "MS":
                self.memory = self.calculate_value()
                self.status.config(text="MEMORY SAVED")
                return

            if value == "M+":
                self.memory += self.calculate_value()
                self.status.config(text="ADDED TO MEMORY")
                return

            if value == "M-":
                self.memory -= self.calculate_value()
                self.status.config(text="SUBTRACTED FROM MEMORY")
                return

            if value in ["sin", "cos", "tan"]:
                self.add_function(value)
                return

            if value == ".":
                self.expression += "."
            elif value == "×":
                self.expression += "*"
            elif value == "÷":
                self.expression += "/"
            else:
                self.expression += value

            self.update_display()
            self.status.config(text="INPUT")

        except Exception:
            self.expression = ""
            self.display_var.set("ERROR")
            self.status.config(text="INVALID OPERATION")

    def add_function(self, function_name):
        if not self.expression:
            self.expression = f"{function_name}("
        else:
            self.expression = (
                f"{function_name}({self.expression})"
            )

        self.update_display()

    def toggle_sign(self):
        if self.expression:
            self.expression = f"-({self.expression})"
        else:
            self.expression = "-"

        self.update_display()

    def calculate_value(self):
        expression = self.expression

        expression = expression.replace(
            "sqrt(",
            "math.sqrt("
        )

        expression = expression.replace(
            "sin(",
            "math.sin(math.radians("
        )

        expression = expression.replace(
            "cos(",
            "math.cos(math.radians("
        )

        expression = expression.replace(
            "tan(",
            "math.tan(math.radians("
        )

        if "math.radians(" in expression:
            expression += ")"

        allowed = {
            "math": math,
            "abs": abs
        }

        return eval(
            expression
            .replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**"),
            {"__builtins__": {}},
            allowed
        )

    def calculate(self):
        try:
            result = self.calculate_value()

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.expression = str(result)
            self.update_display()
            self.status.config(text="RESULT")

        except ZeroDivisionError:
            self.expression = ""
            self.display_var.set("DIVISION BY ZERO")
            self.status.config(text="ERROR")

        except Exception:
            self.expression = ""
            self.display_var.set("ERROR")
            self.status.config(text="INVALID EXPRESSION")

    def bind_keys(self):
        self.root.bind("<Key>", self.keyboard_input)

    def keyboard_input(self, event):
        key = event.char

        if key in "0123456789.+-*/()":
            self.expression += key
            self.update_display()

        elif key == "\r":
            self.calculate()

        elif key == "\x08":
            self.expression = self.expression[:-1]
            self.update_display()

        elif key.lower() == "c":
            self.expression = ""
            self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = OldCalculator(root)
    root.mainloop()
