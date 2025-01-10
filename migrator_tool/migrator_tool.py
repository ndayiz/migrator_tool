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

        # Adding buttons and labels for UI interaction with customtkinter
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
    
    def update_status(self, message, text_color="green"):
        self.status_label.configure(text=f"Status: {message}", text_color=text_color)
        self.root.update_idletasks()

    def select_file(self):
        # File selection dialog to choose the .csdb file
        file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.csdb")])
        if file_path:
            # Get the relative path from the selected file path
            relative_path = os.path.basename(file_path)
            self.selected_file = file_path
            self.update_status(f"Selected file: {relative_path}")
            self.migrate_button.configure(state=ctk.NORMAL)

    def migrate(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a case file first.")
            return

        # Get the database name from the entry field
        mysql_database = self.database_entry.get().strip()

        if not mysql_database:
            messagebox.showerror("Error", "Please enter a MySQL database name.")
            return

        self.update_status("Migrating...")

        # Database configureurations
        mysql_host = "localhost"
        mysql_user = "root"
        mysql_password = ""
        auth_plugin="caching_sha2_password"
        try:
            # Connect to MySQL Server and Create Database
            mysql_conn = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                auth_plugin=auth_plugin
            )
            mysql_cursor = mysql_conn.cursor()

            mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mysql_database};")
            self.update_status(f"Database '{mysql_database}' is ready.")

            # Connect to the newly created database
            mysql_conn = mysql.connector.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                database=mysql_database,
            )
            mysql_cursor = mysql_conn.cursor()

            # Connect to SQLite using the selected file
            sqlite_conn = sqlite3.connect(self.selected_file)
            sqlite_cursor = sqlite_conn.cursor()

            # Function to get primary and foreign key info
            def get_table_constraints(table_name):
                sqlite_cursor.execute(f"PRAGMA table_info(`{table_name}`);")
                schema = sqlite_cursor.fetchall()

                primary_keys = [column[1] for column in schema if column[5] == 1]
                sqlite_cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`);")
                foreign_keys = sqlite_cursor.fetchall()

                return primary_keys, foreign_keys

            # Function to migrate a table
            def migrate_table(table_name):
                primary_keys, foreign_keys = get_table_constraints(table_name)

                # Get table schema
                sqlite_cursor.execute(f"PRAGMA table_info(`{table_name}`);")
                schema = sqlite_cursor.fetchall()

                # Create table in MySQL
                create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
                column_definitions = []
                for column in schema:
                    column_name = column[1]
                    column_type = column[2]
                    column_nullable = "" if column[3] else "NOT NULL"
                    column_default = f"DEFAULT {column[4]}" if column[4] else ""
                    column_definitions.append(
                        f"`{column_name}` {column_type} {column_nullable} {column_default}"
                    )

                if primary_keys:
                    column_definitions.append(f"PRIMARY KEY ({', '.join([f'`{key}`' for key in primary_keys])})")

                for fk in foreign_keys:
                    column_name = fk[3]
                    ref_table = fk[2]
                    ref_column = fk[4]
                    column_definitions.append(
                        f"FOREIGN KEY (`{column_name}`) REFERENCES `{ref_table}`(`{ref_column}`)"
                    )

                create_table_query += ", ".join(column_definitions) + ");"

                try:
                    mysql_cursor.execute(create_table_query)
                    self.update_status(f"Table '{table_name}' created in MySQL.")
                except mysql.connector.Error as err:
                    self.update_status(f"Error creating table '{table_name}': {err}", text_color="red")
                    return

                # Migrate data
                sqlite_cursor.execute(f"SELECT * FROM `{table_name}`")
                rows = sqlite_cursor.fetchall()
                if rows:
                    columns = [f"`{desc[0]}`" for desc in sqlite_cursor.description]
                    placeholders = ", ".join(["%s"] * len(columns))
                    insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders})"

                    try:
                        for i in range(0, len(rows), 1000):
                            batch = rows[i:i + 1000]
                            mysql_cursor.executemany(insert_query, batch)
                            mysql_conn.commit()
                        self.update_status(f"Data migrated for table '{table_name}'.")
                    except mysql.connector.Error as err:
                        self.update_status(f"Error inserting data into table '{table_name}': {err}", text_color="red")

            # Migrate 'level-1' table first
            self.update_status("Migrating 'level-1' table...")
            migrate_table("level-1")

            # Migrate tables referencing 'level-1'
            sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            all_tables = [table[0] for table in sqlite_cursor.fetchall()]
            for table_name in all_tables:
                primary_keys, foreign_keys = get_table_constraints(table_name)
                for fk in foreign_keys:
                    if fk[2] == "level-1":
                        self.update_status(f"Migrating table '{table_name}' (references 'level-1')...")
                        migrate_table(table_name)

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

if __name__ == "__main__":
    main()
