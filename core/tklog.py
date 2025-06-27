# core/tklog.py
import tkinter as tk
import threading

class LogWindow:
    def __init__(self, title="Log"):
        self.root = tk.Tk()
        self.root.title(title)
        self.text = tk.Text(self.root, height=15, width=60)
        self.text.pack()
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def write(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
