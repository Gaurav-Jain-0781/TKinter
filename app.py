import os
import tkinter as tk
from tkinter import ttk, filedialog


def create_file(content="", filename="Untitled"):
    text_area = tk.Text(notebook)
    text_area.insert("end", content)
    text_area.pack(fill="both", expand=True)
    notebook.add(text_area, text=filename)
    notebook.select(text_area)


def save_file():
    file = filedialog.asksaveasfilename()
    try:
        file_name = os.path.basename(file)
        text_widget = root.nametowidget(notebook.select())
        content = text_widget.get("1.0", "end-1c")

        with open(file, 'w') as file:
            file.write(content)

    except(AttributeError, FileNotFoundError):
        print("save command cancelled")
        return

    notebook.tab("current", text=file_name)


def open_file():
    file_path = filedialog.askopenfilename()
    try:
        file_name = os.path.basename(file_path)

        with open(file_path, "r") as file:
            content = file.read()
    except(AttributeError, FileNotFoundError):
        print("Open operation cancelled . ")
        return
    create_file(content, file_name)


root = tk.Tk()
root.title('notebook')
root.option_add("*tearOff", False)

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=(10, 10))

menubar = tk.Menu()
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

create_file()

root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-o>", lambda event: open_file())

root.mainloop()
