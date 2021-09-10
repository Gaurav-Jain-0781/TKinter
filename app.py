import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

contents = dict()


def create_file(content="", filename="Untitled"):
    text_area = tk.Text(notebook)
    text_area.insert("end", content)
    text_area.pack(fill="both", expand=True)

    notebook.add(text_area, text=filename)
    notebook.select(text_area)

    contents[str(text_area)] = hash(content)

    text_scroll = ttk.Scrollbar(text_area, orient="vertical", command=text_area.yview)
    text_scroll.pack(side="right", fill="y")
    text_area["yscrollcommand"] = text_scroll.set


def check_to_changes():
    current = root.nametowidget(notebook.select())
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")['text']

    if hash(content) != contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*")
    elif name[-1] == "*":
        notebook.tab("current", text=name[:-1])


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


def quit_tab():
    current = root.nametowidget(notebook.select())
    if current_tab_unsaved() and not confirm_close():
        return

    notebook.forget(current)

    if len(notebook.tabs()) == 0:
        create_file()


def current_tab_unsaved():
    text_widget = root.nametowidget(notebook.select())
    content = text_widget.get("1.0", "end-1c")

    return hash(content) != contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesno(
        title="confirm close ?",
        icon="question",
        message="Changes to your file has not been saved . Do you want to close ?",
    )


def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        current = root.nametowidget(tab)
        content = current.get("1.0", "end-1c")

        if hash(content) != contents[str(current)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
        return

    root.destroy()


def show_info():
    messagebox.showinfo(
        title="info",
        message="This is a simple text editor created using tkinter . Thank you for using it .",
        icon="info"
    )


root = tk.Tk()
root.title('notebook')
root.option_add("*tearOff", False)

main = ttk.Frame(root, height="250px", width="400px")
main.pack(fill="both", expand=True, padx=10, pady=(10, 10))
main.pack_propagate(0)

menubar = tk.Menu()
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Help", menu=help_menu)

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Quit", command=quit_tab, accelerator="Ctrl+Q")
file_menu.add_command(label="Exit", command=confirm_quit)

help_menu.add_command(label="About", command=show_info)

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

create_file()

root.bind("<KeyPress>", lambda event: check_to_changes())
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-q>", lambda event: quit_tab())

root.mainloop()
