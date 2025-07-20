import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILENAME = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List")
        self.root.geometry("400x500")
        self.tasks = self.load_tasks()

        self.task_var = tk.StringVar()

        # Entry + Add Button
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=10)

        self.entry = tk.Entry(entry_frame, textvariable=self.task_var, width=25, font=("Arial", 14))
        self.entry.pack(side=tk.LEFT, padx=(10, 5))

        add_button = tk.Button(entry_frame, text="Add this Task", command=self.add_task)
        add_button.pack(side=tk.LEFT)

        # Task listbox + scrollbar
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, width=40, height=15, yscrollcommand=self.scrollbar.set,
                                  selectmode=tk.SINGLE, font=("Arial", 12))
        self.listbox.pack()

        self.scrollbar.config(command=self.listbox.yview)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        complete_button = tk.Button(button_frame, text="Mark as Completed", command=self.mark_completed)
        complete_button.grid(row=0, column=0, padx=5)

        delete_button = tk.Button(button_frame, text="Delete this Task", command=self.delete_task)
        delete_button.grid(row=0, column=1, padx=5)

        save_button = tk.Button(button_frame, text="Save this Tasks", command=self.save_tasks)
        save_button.grid(row=0, column=2, padx=5)

        self.refresh_tasks()

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_var.set("")
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            del self.tasks[selected[0]]
            self.refresh_tasks()
        else:
            messagebox.showinfo("Info", "Please select a task to delete.")

    def mark_completed(self):
        selected = self.listbox.curselection()
        if selected:
            self.tasks[selected[0]]["completed"] = not self.tasks[selected[0]]["completed"]
            self.refresh_tasks()
        else:
            messagebox.showinfo("Info", "Select a task to mark complete.")

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔️ " if task["completed"] else "❌ "
            self.listbox.insert(tk.END, status + task["task"])

    def save_tasks(self):
        with open(FILENAME, "w") as f:
            json.dump(self.tasks, f, indent=4)
        messagebox.showinfo("Saved", "Tasks saved successfully! 😊")

    def load_tasks(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, "r") as f:
                return json.load(f)
        return []

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
