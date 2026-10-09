import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class Database:

    def __init__(self, db_name="taskflow.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL
                )
            """)

        conn.commit()
        conn.close()

    def get_tasks(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, status, priority FROM tasks")
        rows = cursor.fetchall()

        conn.close()
        return rows

    def add_task(self, title, status, priority):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (title, status, priority) VALUES (?, ?, ?)",
            (title, status, priority),
        )

        conn.commit()
        conn.close()

class TaskFlowApp:

    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Aplikacja do zarządzania zadaniami")
        self.root.geometry("750x500")

        self.db = Database()

        style = ttk.Style()
        style.theme_use("clam")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):

        form_frame = ttk.LabelFrame(
            self.root, text=" Zarządzanie Zadaniami ", padding=15
        )

        form_frame.pack(
            fill="x", padx=15, pady=15
        )

        ttk.Label(form_frame, text="Tytuł zadania:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        self.title_entry = ttk.Entry(form_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Status:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )

        self.status_cb = ttk.Combobox(
            form_frame,
            values=["Do zrobienia", "W trakcie", "Zakończone"],
            width=15,
            state="readonly"
        )

        self.status_cb.grid(row=0, column=3, padx=5, pady=5)
        self.status_cb.current(0)

        ttk.Label(form_frame, text="Piorytet:").grid(
            row=0, column=4, sticky="w", padx=5, pady=5
        )

        self.priority_cb = ttk.Combobox(
            form_frame,
            values=["Niski", "Średni", "Wysoki"],
            width=12,
            state="readonly"
        )

        self.priority_cb.grid(row=0, column=5, padx=5, pady=5)
        self.priority_cb.current(1)

        add_btn = ttk.Button(
            form_frame, text="Dodaj zadanie", command=self.handle_add_task
        )

        add_btn.grid(row=0, column=6, padx=15, pady=5)

        table_frame = ttk.LabelFrame(self.root, text=" Lista Zadań ", padding=10)

        table_frame.pack(
            fill="both", expand=True, padx=15, pady=(0, 15)
        )

        columns = ("ID", "Tytuł", "Status", "Piorytet")

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.column(
            "Tytuł", width=250, anchor="w"
        )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.get_tasks()

        for row in rows:
            self.tree.insert(
                "", "end", values=row
            )

    def handle_add_task(self):

        title = self.title_entry.get().strip()
        status = self.status_cb.get()
        priority = self.priority_cb.get()

        if not title:
            messagebox.showwarning(
                "Ostrzeżenie", "Tytuł nie może być pusty!"
            )
            return

        self.db.add_task(title, status, priority)

        self.title_entry.delete(0, tk.END)

        self.load_data()

        messagebox.showinfo("Sukces", "Zadanie zostało dodane do bazy")   


if __name__ == "__main__":

    root = tk.Tk()

    app = TaskFlowApp(root)

    root.mainloop()
    