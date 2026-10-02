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