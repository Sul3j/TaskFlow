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

        db = Database()

        style = ttk.Style()
        style.theme_use("clam")

        self.create_widgets()

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



if __name__ == "__main__":

    root = tk.Tk()

    app = TaskFlowApp(root)

    root.mainloop()
    