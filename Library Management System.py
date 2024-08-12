import sqlite3

def initialize_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create admin table
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL)''')

    # Create books table
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 year INTEGER NOT NULL,
                 isbn TEXT NOT NULL)''')

    # Create issued books table
    c.execute('''CREATE TABLE IF NOT EXISTS issued_books (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 book_id INTEGER,
                 student_name TEXT NOT NULL,
                 issue_date TEXT NOT NULL,
                 return_date TEXT,
                 FOREIGN KEY (book_id) REFERENCES books(id))''')

    # Add a default admin if no admin exists
    c.execute("SELECT * FROM admins")
    if not c.fetchone():
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('admin', 'admin'))

    conn.commit()
    conn.close()

initialize_database()

import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime


# Function to create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Library Management System")
    window.geometry("800x600")
    return window


# Function to check admin credentials
def admin_login(username, password):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result


# Function for login screen
def login_screen():
    window = create_main_window()

    tk.Label(window, text="Admin Login", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Username").pack(pady=5)
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Password").pack(pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if admin_login(username, password):
            window.destroy()
            dashboard_screen(username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(window, text="Login", command=attempt_login).pack(pady=20)

    window.mainloop()


# Function for dashboard screen
def dashboard_screen(admin_name):
    window = create_main_window()
    tk.Label(window, text=f"Welcome, {admin_name}", font=("Arial", 14)).pack(pady=10)

    tk.Label(window, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}").pack(pady=5)
    tk.Label(window, text=f"Time: {datetime.now().strftime('%H:%M:%S')}").pack(pady=5)

    # Add buttons for the 8 functionalities
    functionalities = [
        ("Add Books", add_books_screen),
        ("Issue Books", issue_books_screen),
        ("Edit Books", edit_books_screen),
        ("Return Books", return_books_screen),
        ("Delete Books", delete_books_screen),
        ("Search Books", search_books_screen),
        ("Show Books", show_books_screen),
        ("Log out", lambda: window.destroy())
    ]

    for func_name, func_command in functionalities:
        tk.Button(window, text=func_name, width=20, command=func_command).pack(pady=5)

    window.mainloop()


# Function to add books
def add_books_screen():
    window = create_main_window()

    tk.Label(window, text="Add a New Book", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Title").pack(pady=5)
    title_entry = tk.Entry(window)
    title_entry.pack(pady=5)

    tk.Label(window, text="Author").pack(pady=5)
    author_entry = tk.Entry(window)
    author_entry.pack(pady=5)

    tk.Label(window, text="Year").pack(pady=5)
    year_entry = tk.Entry(window)
    year_entry.pack(pady=5)

    tk.Label(window, text="ISBN").pack(pady=5)
    isbn_entry = tk.Entry(window)
    isbn_entry.pack(pady=5)

    def add_book():
        title = title_entry.get()
        author = author_entry.get()
        year = int(year_entry.get())
        isbn = isbn_entry.get()
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                  (title, author, year, isbn))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book added successfully")
        window.destroy()

    tk.Button(window, text="Add Book", command=add_book).pack(pady=20)

    window.mainloop()


# Function to issue books
def issue_books_screen():
    window = create_main_window()

    tk.Label(window, text="Issue a Book", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Book ID").pack(pady=5)
    book_id_entry = tk.Entry(window)
    book_id_entry.pack(pady=5)

    tk.Label(window, text="Student Name").pack(pady=5)
    student_name_entry = tk.Entry(window)
    student_name_entry.pack(pady=5)

    def issue_book():
        book_id = int(book_id_entry.get())
        student_name = student_name_entry.get()
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM issued_books WHERE student_name=?", (student_name,))
        count = c.fetchone()[0]
        if count >= 3:
            messagebox.showerror("Error", "Cannot issue more than 3 books to a single student.")
        else:
            issue_date = datetime.now().strftime('%Y-%m-%d')
            c.execute("INSERT INTO issued_books (book_id, student_name, issue_date) VALUES (?, ?, ?)",
                      (book_id, student_name, issue_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Book issued successfully")
            window.destroy()

    tk.Button(window, text="Issue Book", command=issue_book).pack(pady=20)

    window.mainloop()


# Function to edit books
def edit_books_screen():
    window = create_main_window()

    tk.Label(window, text="Edit a Book", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Book ID").pack(pady=5)
    book_id_entry = tk.Entry(window)
    book_id_entry.pack(pady=5)

    tk.Label(window, text="New Title").pack(pady=5)
    title_entry = tk.Entry(window)
    title_entry.pack(pady=5)

    tk.Label(window, text="New Author").pack(pady=5)
    author_entry = tk.Entry(window)
    author_entry.pack(pady=5)

    tk.Label(window, text="New Year").pack(pady=5)
    year_entry = tk.Entry(window)
    year_entry.pack(pady=5)

    tk.Label(window, text="New ISBN").pack(pady=5)
    isbn_entry = tk.Entry(window)
    isbn_entry.pack(pady=5)

    def edit_book():
        book_id = int(book_id_entry.get())
        title = title_entry.get()
        author = author_entry.get()
        year = int(year_entry.get())
        isbn = isbn_entry.get()
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
                  (title, author, year, isbn, book_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book updated successfully")
        window.destroy()

    tk.Button(window, text="Edit Book", command=edit_book).pack(pady=20)

    window.mainloop()


# Function to return books
def return_books_screen():
    window = create_main_window()

    tk.Label(window, text="Return a Book", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Book ID").pack(pady=5)
    book_id_entry = tk.Entry(window)
    book_id_entry.pack(pady=5)

    tk.Label(window, text="Student Name").pack(pady=5)
    student_name_entry = tk.Entry(window)
    student_name_entry.pack(pady=5)

    def return_book():
        book_id = int(book_id_entry.get())
        student_name = student_name_entry.get()
        return_date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE issued_books SET return_date=? WHERE book_id=? AND student_name=? AND return_date IS NULL",
                  (return_date, book_id, student_name))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book returned successfully")
        window.destroy()

    tk.Button(window, text="Return Book", command=return_book).pack(pady=20)

    window.mainloop()


# Function to delete books
def delete_books_screen():
    window = create_main_window()

    tk.Label(window, text="Delete a Book", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Book ID").pack(pady=5)
    book_id_entry = tk.Entry(window)
    book_id_entry.pack(pady=5)

    def delete_book():
        book_id = int(book_id_entry.get())
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Book deleted successfully")
        window.destroy()

    tk.Button(window, text="Delete Book", command=delete_book).pack(pady=20)

    window.mainloop()


# Function to search books
def search_books_screen():
    window = create_main_window()

    tk.Label(window, text="Search Books", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Search by Title").pack(pady=5)
    title_entry = tk.Entry(window)
    title_entry.pack(pady=5)

    tk.Label(window, text="Search by Author").pack(pady=5)
    author_entry = tk.Entry(window)
    author_entry.pack(pady=5)

    tk.Label(window, text="Search by Year").pack(pady=5)
    year_entry = tk.Entry(window)
    year_entry.pack(pady=5)

    def search_books():
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ?"
        c.execute(query, ('%' + title + '%', '%' + author + '%', '%' + year + '%'))
        results = c.fetchall()
        conn.close()
        if results:
            for book in results:
                messagebox.showinfo("Book Found",
                                    f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, ISBN: {book[4]}")
        else:
            messagebox.showinfo("No Results", "No books found.")
        window.destroy()

    tk.Button(window, text="Search", command=search_books).pack(pady=20)

    window.mainloop()


# Function to show all books
def show_books_screen():
    window = create_main_window()

    tk.Label(window, text="All Books", font=("Arial", 16)).pack(pady=10)

    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()

    if books:
        tree = ttk.Treeview(window, columns=("ID", "Title", "Author", "Year", "ISBN"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Year", text="Year")
        tree.heading("ISBN", text="ISBN")
        tree.pack(fill=tk.BOTH, expand=True)

        for book in books:
            tree.insert("", tk.END, values=book)
    else:
        tk.Label(window, text="No books available in the library.").pack(pady=20)

    window.mainloop()


# Start the application with the login screen
login_screen()

##write admin/admin as user name and password.