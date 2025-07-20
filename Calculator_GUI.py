import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculator")
        self.root.geometry("480x500")
        self.root.resizable(False, False)

        self.expression = ""

        self.entry = tk.Entry(root, font=("Arial", 20), borderwidth=3, relief="ridge", justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=15, padx=10, pady=10)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0, 4)
        ]

        for (text, row, col, *span) in buttons:
            colspan = span[0] if span else 1
            btn = tk.Button(root, text=text, font=("Arial", 16), width=8 if text != "=" else 35,
                            height=2, command=lambda t=text: self.on_click(t))
            btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5)

    def on_click(self, char):
        if char == "=":
            try:
                result = str(eval(self.expression))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
                self.expression = result
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
                self.expression = ""
        elif char == "C":
            self.expression = ""
            self.entry.delete(0, tk.END)
        else:
            self.expression += str(char)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)

# Run the calculator GUI
if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
