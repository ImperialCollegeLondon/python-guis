import tkinter as tk
from tkinter import ttk


def on_button_clicked():
    return "Hello Pythoners!"


class MySimpleGUI(tk.Tk):
    def __init__(self):
        super(MySimpleGUI, self).__init__()

        button = ttk.Button(master=self, text="Click me")
        self.label = ttk.Label(master=self, text="")

        button.pack(side=tk.LEFT)
        self.label.pack(side=tk.LEFT)

        # Add the callback of the button.
        button.configure(command=self._on_button_clicked)

    def _on_button_clicked(self):
        self.label["text"] = on_button_clicked()


if __name__ == "__main__":
    root = MySimpleGUI()
    root.mainloop()
