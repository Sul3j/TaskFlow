import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

BG_DARK = "#1e1e1e"
BG_FRAME = "#2d2d2d"
TEXT_LIGHT = "#ffffff"
ACCENT_BLUE = "#007acc"
ACCENT_GREEN = "#28a745"
ACCENT_RED = "#dc3545"
ENTRY_BG = "#3c3c3c"
ROW_BG_1 = "#252526"
ROW_BG_2 = "#2d2d30"

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

    def update_task(self, task_id, title, status, priority):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
                UPDATE tasks
                SET title = ?, status = ?, priority = ?
                WHERE id = ?
            """,
            (title, status, priority, task_id)
        )

        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

        conn.commit()
        conn.close()

class TaskFlowApp:

    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Aplikacja do zarządzania zadaniami")
        self.root.geometry("750x500")
        self.root.configure(bg=BG_DARK)

        self.db = Database()
        self.selected_task_id = None

        self.setup_styles()
        self.create_widgets()
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # styl ramek i etykiet
        style.configure(
            "Dark.TLabelframe", background=BG_FRAME, foreground=TEXT_LIGHT
        )

        style.configure(
            "Dark.TLabelframe.Label",
            background=BG_FRAME,
            foreground=TEXT_LIGHT,
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Dark.TLabel", background=BG_FRAME, foreground=TEXT_LIGHT, font=("Arial", 9)
        )

        # combobox (tło i kolor tekstu)
        style.configure(
            "Dark.TCombobox",
            fieldbackground=ENTRY_BG,
            background=BG_FRAME,
            foreground=TEXT_LIGHT,
            arrowcolor=TEXT_LIGHT
        )

        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", ENTRY_BG)],
            foreground=[("readonly", TEXT_LIGHT)]
        )

        # style tabeli
        style.configure(
            "Dark.Treeview",
            background=ROW_BG_1,
            foreground=TEXT_LIGHT,
            fieldbackground=BG_DARK,
            rowheight=32,
            font=("Arial", 9)
        )

        style.configure(
            "Dark.Treeview.Heading",
            background="#333333",
            foreground=TEXT_LIGHT,
            font=("Arial", 9, "bold"),
            relief="flat"
        )

        style.map(
            "Dark.Treeview",
            background=[("selected", ACCENT_BLUE)],
            foreground=[("selected", TEXT_LIGHT)]
        )

        style.configure("Dark.TFrame", background=BG_FRAME)

        style.configure(
            "Dark.TButton",
            background=ACCENT_BLUE,
            foreground=TEXT_LIGHT,
            relief="flat",
            padding=6
        )

        style.map(
            "Dark.TButton",
            background=[("active", "#005fa3")]
        )

        style.configure(
            "Green.TButton",
            background=ACCENT_GREEN,
            foreground=TEXT_LIGHT,
            relief="flat",
            padding=6
        )

        style.map(
            "Green.TButton",
            background=[("active", "#1e7e34")]
        )

        style.configure(
            "Red.TButton",
            background=ACCENT_RED,
            foreground=TEXT_LIGHT,
            relief="flat",
            padding=6
        )
        
        style.map(
            "Red.TButton",
            background=[("active", "#a71d2a")]
        )

        style.configure(
            "Gray.TButton",
            background=ENTRY_BG,
            foreground=TEXT_LIGHT,
            relief="flat",
            padding=6
        )
                
        style.map(
            "Grey.TButton",
            background=[("active", "#2a2a2a")]
        )

    def create_widgets(self):

        form_frame = ttk.LabelFrame(
            self.root, text=" Zarządzanie Zadaniami ", padding=15, style="Dark.TLabelframe"
        )

        form_frame.pack(
            fill="x", padx=15, pady=15
        )

        ttk.Label(form_frame, text="Tytuł zadania:", style="Dark.TLabel").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        self.title_entry = ttk.Entry(form_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Status:", style="Dark.TLabel").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )

        self.status_cb = ttk.Combobox(
            form_frame,
            values=["Do zrobienia", "W trakcie", "Zakończone"],
            width=15,
            state="readonly",
            style="Dark.TCombobox"
        )

        self.status_cb.grid(row=0, column=3, padx=5, pady=5)
        self.status_cb.current(0)

        ttk.Label(form_frame, text="Piorytet:", style="Dark.TLabel").grid(
            row=0, column=4, sticky="w", padx=5, pady=5
        )

        self.priority_cb = ttk.Combobox(
            form_frame,
            values=["Niski", "Średni", "Wysoki"],
            width=12,
            state="readonly",
            style="Dark.TCombobox"
        )

        self.priority_cb.grid(row=0, column=5, padx=5, pady=5)
        self.priority_cb.current(1)

        btn_frame = ttk.Frame(form_frame, style="Dark.TFrame")
        btn_frame.grid(row=1, column=0, columnspan=6, pady=10)

        self.add_btn = ttk.Button(
            btn_frame,
            text="Dodaj zadanie",
            command=self.handle_add_task,
            style="Dark.TButton",
        )

        self.add_btn.pack(side="left", padx=5)

        self.update_btn = ttk.Button(
            btn_frame, text="Aktaualizuj zaznaczone",
            command=self.handle_update,
            style="Green.TButton"
        )
        
        self.update_btn.pack(side="left", padx=5)

        self.delete_btn = ttk.Button(
            btn_frame, text="Usuń zaznaczone",
            command=self.handle_delete,
            style="Red.TButton"
        )
                
        self.delete_btn.pack(side="left", padx=5)

        self.clear_btn = ttk.Button(
            btn_frame, text="Wyczyść Formularz",
            command=self.clear_form,
            style="Grey.TButton"
        )
                
        self.clear_btn.pack(side="left", padx=5)


        table_frame = ttk.LabelFrame(
            self.root, 
            text=" Lista Zadań ", 
            padding=10, 
            style="Dark.TLabelframe"
            )

        table_frame.pack(
            fill="both", expand=True, padx=15, pady=(0, 15)
        )

        columns = ("ID", "Tytuł", "Status", "Piorytet")

        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings", 
            selectmode="browse", 
            style="Dark.Treeview"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.column(
            "Tytuł", width=250, anchor="w"
        )

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

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

    def handle_update(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "Ostrzeżenie", "Najpierw zaznacz zadaniez tabeli do edycji!"
            )
            return

        title = self.title_entry.get().strip()
        status = self.status_cb.get()
        priority = self.priority_cb.get()

        if not title:
            messagebox.showwarning("Ostrzeżenie", "Tytuł nie może być pusty!")
            return

        self.db.update_task(self.selected_task_id, title, status, priority)
        self.clear_form()
        self.load_data()
        messagebox.showinfo("Sukces", "Zadanie zostało zaktualizowane!")

    def handle_delete(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "Ostrzeżenie", "Najpierw zaznacz zadanie z tabeli do usunięcia!"
            )
            return

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chesz usunąć wybrane zadanie?"):
            self.db.delete_task(self.selected_task_id)
            self.clear_form()
            self.load_data()
            messagebox.showinfo("Sukces", "Zadanie zostało usunięte!")


    def on_row_select(self, event):

        selected_items = self.tree.selection()

        if not selected_items:
            return

        item = self.tree.item(selected_items)
        values = item["values"]

        if values:
            self.selected_task_id = values[0]

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[1])

            self.status_cb.set(values[2])
            self.priority_cb.set(values[3])

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.status_cb.current(0)
        self.priority_cb.current(1)
        self.selected_task_id = None

        for item in self.tree.selection():
            self.tree.selection_remove(item)





if __name__ == "__main__":

    root = tk.Tk()

    app = TaskFlowApp(root)

    root.mainloop()
    