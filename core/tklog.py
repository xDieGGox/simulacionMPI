# core/tklog.py
import tkinter as tk

class LogWindow:
    def __init__(self, title="Log"):
        self.root = tk.Tk()
        self.root.title(title)
        self.text = tk.Text(self.root, height=15, width=60)
        self.text.pack()

    def write(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)

    def start(self):
        self.root.mainloop()
