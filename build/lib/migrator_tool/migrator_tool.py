import os
import sqlite3
import mysql.connector
import customtkinter as ctk
from tkinter import filedialog, messagebox


class DatabaseMigratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Migrator")
        self.root.geometry("800x350")

        # Adding buttons and labels for UI interaction
        self.label = ctk.CTkLabel(root, text="Database Migration Tool", font=("Helvetica", 17))
        self.label.pack(pady=20)

        self.select_file_button = ctk.CTkButton(root, text="Select Case File", font=("Helvetica", 13), command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.database_label = ctk.CTkLabel(root, text="Enter MySQL Database Name:", font=("Helvetica", 12))
        self.database_label.pack(pady=10)

        self.database_entry = ctk.CTkEntry(root, placeholder_text="Enter db name", font=("Helvetica", 12))
        self.database_entry.pack(pady=10)

        self.migrate_button = ctk.CTkButton(root, text="Migrate Data", font=("Helvetica", 13), command=self.migrate, state=ctk.DISABLED)
        self.migrate_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(root, text="Status: Ready", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # Footer text
        self.footer_label = ctk.CTkLabel(root, text="Developed by NISR IT TEAM", font=("Helvetica", 11, "italic"), text_color="gray")
        self.footer_label.pack(pady=10)

        self.selected_file = None

    def update_status(self, message, text_color="white"):
        self.status_label.configure(text=f"Status: {message}", text_color=text_color)
        self.root.update_idletasks()

    def select_file(self):
        # File selection dialog to choose the .csdb file
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.csdb")])
        if file_path:
            relative_path = os.path.basename(file_path)
            self.selected_file = file_path
            self.update_status(f"Selected file: {relative_path}")
            self.migrate_button.configure(state=ctk.NORMAL)

    def migrate(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a case file first.")
            return

        mysql_database = self.database_entry.get().strip()
        if not mysql_database:
            messagebox.showerror("Error", "Please enter a MySQL database name.")
            return

        self.update_status("Migrating...")

        # Database configurations
        mysql_host = "localhost"
        mysql_user = "root"
        mysql_password = ""

        try:
            # Connect to MySQL Server and Create Database
            mysql_conn = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password)
            mysql_cursor = mysql_conn.cursor()

            mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database};")
            self.update_status(f"Database '{mysql_database}' is ready.")

            # Connect to the newly created database
            mysql_conn = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)
            mysql_cursor = mysql_conn.cursor()

            # Connect to SQLite
            sqlite_conn = sqlite3.connect(self.selected_file)
            sqlite_cursor = sqlite_conn.cursor()

            def migrate_table(table_name):
                # Example migration logic: Add table schema and data handling
                pass

            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in sqlite_cursor.fetchall()]
            for table in tables:
                self.update_status(f"Migrating table '{table}'...")
                migrate_table(table)

            sqlite_conn.close()
            mysql_conn.close()

            self.update_status("Migration Completed!", text_color="green")
            messagebox.showinfo("Success", "Database Migration Completed Successfully!")

        except Exception as e:
            self.update_status("Migration Failed.", text_color="red")
            messagebox.showerror("Error", f"Error during migration: {e}")


def main():
    root = ctk.CTk()
    app = DatabaseMigratorApp(root)
    root.mainloop()
