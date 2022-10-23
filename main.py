import json
from tkinter import (
    Tk,
    Button,
    Label,
    Entry,
    Radiobutton,
    IntVar,
    BooleanVar,
    Checkbutton,
    END,
)
from tkinter.scrolledtext import ScrolledText

from tkcalendar import DateEntry


def clear_view(tk):
    for el in tk.grid_slaves():
        el.destroy()


def list_tasks_view(tk):
    pass


def save_task(title, due_date, description, priority, is_completed):
    task = {
        "title": title,
        "due_date": due_date,
        "description": description,
        "priority": priority,
        "is_completed": is_completed,
    }
    with open("db.txt", "a+") as file:
        file.write(json.dumps(task) + "\n")
    main_view()


def create_task_view(tk):
    clear_view(tk)
    Label(tk, text="Enter your task name: ").grid(row=0, column=0, padx=20, pady=20)
    name = Entry(tk)
    name.grid(row=0, column=1, padx=20, pady=20)
    Label(tk, text="Due date: ").grid(row=1, column=0, padx=20, pady=20)
    date = DateEntry(tk)
    date.grid(row=1, column=1, padx=20, pady=20)
    Label(tk, text="Description: ").grid(row=2, column=0, padx=20, pady=20)
    description = ScrolledText(tk, width=20, height=10)
    description.grid(row=2, column=1, padx=20, pady=20)
    Label(tk, text="Select priority: ").grid(row=3, column=0, padx=20, pady=20)
    selected = IntVar()
    rad1 = Radiobutton(tk, text="Low", value=1, variable=selected)
    rad2 = Radiobutton(tk, text="Medium", value=2, variable=selected)
    rad3 = Radiobutton(tk, text="High", value=3, variable=selected)
    rad1.grid(column=1, row=3)
    rad2.grid(column=2, row=3)
    rad3.grid(column=3, row=3)
    Label(tk, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    chk_state = BooleanVar()
    chk_state.set(False)  # set check state
    chk = Checkbutton(tk, text="Choose", var=chk_state)
    chk.grid(column=1, row=4)
    Button(tk, text="Save task", bg="green", fg="white", command=lambda: save_task(name.get(), date.get(), description.get("1.0", END), selected.get(), chk_state.get())).grid(row=5, column=0)
    Button(tk, text="Cancel", bg="black", fg="white", command=lambda: main_view(tk)).grid(row=5, column=1, padx=100,
                                                                                          pady=100)


def main_view(tk):
    clear_view(tk)
    list_button = Button(
        tk,
        text="List all tasks",
        bg="blue",
        fg="white",
        command=lambda: list_tasks_view(tk),
    )
    list_button.grid(row=1, column=0, padx=100, pady=100)
    create_button = Button(
        tk,
        text="Create new task",
        bg="green",
        fg="white",
        command=lambda: create_task_view(tk),
    )
    create_button.grid(row=1, column=1, padx=100, pady=100)


tk = Tk()
tk.geometry("700x600")
main_view(tk)
tk.mainloop()
