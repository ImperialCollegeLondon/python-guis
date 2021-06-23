"""
This example has been adapted from:
https://stackoverflow.com/a/29729649/3778792

All credit to its authors.
"""
from threading import Thread
from time import sleep
import tkinter as tk
from tkinter import ttk


def on_loading(widget, status):
    status("Loading...")
    widget.start(150)
    sleep(15)
    widget.stop()
    status("Now ready to work...")


def main():
    root = tk.Tk()
    root.geometry("640x120")

    ft = ttk.Frame()
    ft.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    label = ttk.Label(ft, text="")
    label.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    def status(text):
        label["text"] = text  # the lambda to capture value

    pb_hd = ttk.Progressbar(
        ft, orient="horizontal", mode="determinate", max=100, variable=0
    )
    pb_hd.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

    # Creates a thread that call on_loading
    Thread(target=on_loading, args=(pb_hd, status)).start()
    root.mainloop()


if __name__ == "__main__":
    main()
