import os
import tkinter as tk
from tkinter import ttk, filedialog


def create_file():
    text_area = tk.Text(notebook)
    text_area.pack(fill="both", expand=True)
    notebook.add(text_area, text="untitled")
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


root = tk.Tk()
root.title('notebook')
root.option_add("*tearOff", False)

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=(10, 10))

menubar = tk.Menu()
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="new", command=create_file)
file_menu.add_command(label="save", command=save_file)

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

create_file()

root.mainloop()
