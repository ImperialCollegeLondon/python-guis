import tkinter as tk
from tkinter import ttk


def on_button_clicked():
    label["text"] = "Hello Pythoners!"


# Create the widgets. This includes adding them to a container.
root = tk.Tk()
button = ttk.Button(master=root, text="Click me")
label = ttk.Label(master=root, text="")

# Create their physical arrangement.
button.pack(side=tk.LEFT)
label.pack(side=tk.LEFT)

# Add the callback of the button.
button.configure(command=on_button_clicked)

# Run the main window loop, which starts the program.
root.mainloop()
