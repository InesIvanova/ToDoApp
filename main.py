import ast
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
    END, INSERT,
)
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from tkcalendar import DateEntry


mapper = {1: "Minor", 2: "Medium", 3: "High"}


def clear_view(tk):
    for el in tk.grid_slaves():
        el.destroy()


def delete_task_from_file(task):
    if isinstance(task, str):
        task = ast.literal_eval(task)
    with open("db.txt", "r") as file:
        lines = file.readlines()
    with open("db.txt", "w") as file:
        for line in lines:
            if json.loads(line.strip("\n")) != task:
                file.write(line)


def delete_task(task):
    delete_task_from_file(task)
    main_view(tk)


def save_changes(task, tk, title, due_date, description, priority, is_completed):
    delete_task_from_file(task)
    changed_task = {"title": title, "due_date": due_date, "description": description, "priority": priority, "is_completed": is_completed}
    with open("db.txt", "a") as file:
        file.write(json.dumps(changed_task) + '\n')
    main_view(tk)


def edit_task(task, tk):
    task = ast.literal_eval(task)
    clear_view(tk)
    Label(tk, text="Enter your task name: ").grid(row=0, column=0, padx=20, pady=20)
    name = Entry(tk)
    name.delete(0, END)
    name.insert(0, task['title'])
    name.grid(row=0, column=1, padx=20, pady=20)
    Label(tk, text="Due date: ").grid(row=1, column=0, padx=20, pady=20)
    date = DateEntry(tk)
    date.delete(0, END)
    date.insert(0, task['due_date'])
    date.grid(row=1, column=1, padx=20, pady=20)
    Label(tk, text="Description: ").grid(row=2, column=0, padx=20, pady=20)
    description = ScrolledText(tk, width=20, height=10)
    description.insert(INSERT, task['description'])
    description.insert(END, "")
    description.grid(row=2, column=1, padx=20, pady=20)
    Label(tk, text=f"Select priority, current is {mapper[task['priority']] if task['priority'] else None}").grid(row=3, column=0, padx=20, pady=20)
    s = IntVar()
    rad1 = Radiobutton(tk, text='Low', value=1, variable=s)
    rad2 = Radiobutton(tk, text='Medium', value=2, variable=s)
    rad3 = Radiobutton(tk, text='High', value=3, variable=s)

    rad1.grid(column=1, row=3)
    rad2.grid(column=2, row=3)
    rad3.grid(column=3, row=3)
    Label(tk, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    Label(tk, text="Check if completed: ").grid(row=4, column=0, padx=20, pady=20)
    chk_state = BooleanVar()
    chk_state.set(task["is_completed"])  # set check state
    chk = Checkbutton(tk, text='Choose', variable=chk_state, onvalue=True, offvalue=False)
    chk.grid(column=1, row=4)

    Button(tk, text="Edit task", bg="yellow", fg="black", command=lambda: save_changes(task, tk, name.get(), date.get(), description.get("1.0", END), s.get(), chk_state.get())).grid(row=5, column=0)
    Button(tk, text="Cancel", bg="black", fg="white", command=lambda: main_view(tk)).grid(row=5, column=1, padx=100, pady=100)


def list_tasks_view(tk):
    clear_view(tk)
    dd = Combobox(tk, width=100)
    all_tasks = []
    with open("db.txt", "r") as file:
        for line in file.readlines():
            all_tasks.append(json.loads(line))

    dd["values"] = all_tasks
    dd.grid(row=0, column=0)

    Button(
        tk,
        text="Edit task",
        bg="yellow",
        fg="black",
        command=lambda: edit_task(dd.get(), tk),
    ).grid(row=2, column=0)
    Button(
        tk,
        text="Delete task",
        bg="red",
        fg="white",
        command=lambda: delete_task(dd.get()),
    ).grid(row=2, column=1)
    Button(
        tk, text="Cancel", bg="black", fg="white", command=lambda: main_view(tk)
    ).grid(row=3, column=0, padx=100, pady=100)


def save_task(title, due_date, description, priority, is_completed, tk):
    task = {
        "title": title,
        "due_date": due_date,
        "description": description,
        "priority": priority,
        "is_completed": is_completed,
    }
    with open("db.txt", "a+") as file:
        file.write(json.dumps(task) + "\n")
    main_view(tk)


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
    Button(
        tk,
        text="Save task",
        bg="green",
        fg="white",
        command=lambda: save_task(
            name.get(),
            date.get(),
            description.get("1.0", END),
            selected.get(),
            chk_state.get(),
            tk,
        ),
    ).grid(row=5, column=0)
    Button(
        tk, text="Cancel", bg="black", fg="white", command=lambda: main_view(tk)
    ).grid(row=5, column=1, padx=100, pady=100)


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
