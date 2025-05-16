

# Import the tkinter library for creating graphical user interfaces (GUIs)
import tkinter as tk
# Import the messagebox module from tkinter for showing dialog boxes (e.g., alerts, confirmations) and ttk for using themed widgets
from tkinter import messagebox, ttk
# Import the re module for regular expression operations (e.g., pattern matching)
import re
# Import the Image and ImageTk modules from PIL (Pillow library) for image processing and displaying images in Tkinter
from PIL import Image, ImageTk
# Import the urllib.request module for handling URL requests (e.g., downloading resources from the web)
import urllib.request
# Import the os module for interacting with the operating system (e.g., file paths, directory operations)
import os
# Importing the MySQL connector library for connecting and interacting with MySQL database.
import mysql.connector
# Importing the Error class from mysql.connector to handle specific database connection errors.
from mysql.connector import Error

class LibraryManagementSystem:
    def __init__(self):
        self.current_user = None
        self.load_data()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="alice",  # Your MySQL password
                database="Library"
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def load_data(self):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT email FROM users WHERE email = 'admin@gmail.com'")
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO users (email, password, profile) VALUES (%s, %s, %s)",
                        ('admin@gmail.com', '12345', '{}')
                    )
                    conn.commit()
            except Error as e:
                print(f"Error loading data: {e}")
            finally:
                cursor.close()
                conn.close()

    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def register_user(self, email, password):
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Email is already registered.")
                    return
                cursor.execute(
                    "INSERT INTO users (email, password, profile) VALUES (%s, %s, %s)",
                    (email, password, '{}')
                )
                conn.commit()
                messagebox.showinfo("Success", f"User registered successfully with email: {email}")
            except Error as e:
                print(f"Error registering user: {e}")
                messagebox.showerror("Error", "Failed to register user.")
            finally:
                cursor.close()
                conn.close()

    def login_user(self, email, password):
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return False
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "Email is not registered.")
                    return False
                if result[0] == password:
                    self.current_user = email
                    messagebox.showinfo("Success", "User logged in successfully!")
                    return True
                else:
                    messagebox.showerror("Error", "Incorrect password.")
                    return False
            except Error as e:
                print(f"Error logging in: {e}")
                messagebox.showerror("Error", "Failed to log in.")
            finally:
                cursor.close()
                conn.close()
        return False

    def add_book(self, title, author, copies, genre):
        if self.current_user != "admin@gmail.com":
            messagebox.showerror("Error", "Only admin can add books.")
            return
        if not all([title, author, copies, genre]):
            messagebox.showerror("Error", "All fields (title, author, copies, genre) are required.")
            return
        try:
            copies = int(copies)
            if copies < 0:
                raise ValueError("Copies cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Invalid number of copies.")
            return
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                conn.start_transaction()
                # Handle Author
                cursor.execute("SELECT AuthorID FROM Authors WHERE AuthorName = %s", (author,))
                author_result = cursor.fetchone()
                if author_result:
                    author_id = author_result[0]
                else:
                    cursor.execute("INSERT INTO Authors (AuthorName) VALUES (%s)", (author,))
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    author_id = cursor.fetchone()[0]
                    if not author_id or author_id == 0:
                        raise Error("Failed to retrieve valid AuthorID after insertion")
                # Handle Genre
                cursor.execute("SELECT GenreID FROM Genres WHERE GenreName = %s", (genre,))
                genre_result = cursor.fetchone()
                if genre_result:
                    genre_id = genre_result[0]
                else:
                    cursor.execute("INSERT INTO Genres (GenreName) VALUES (%s)", (genre,))
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    genre_id = cursor.fetchone()[0]
                    if not genre_id or genre_id == 0:
                        raise Error("Failed to retrieve valid GenreID after insertion")
                # Insert book
                cursor.execute(
                    "INSERT INTO Books (Title, AuthorID, Copies, GenreID) VALUES (%s, %s, %s, %s)",
                    (title, author_id, copies, genre_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
            except Error as e:
                conn.rollback()
                print(f"Error adding book: {e}")
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def search_books(self, title, author):
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT b.BookID, b.Title, a.AuthorName, g.GenreName, b.Copies
                    FROM Books b
                    JOIN Authors a ON b.AuthorID = a.AuthorID
                    JOIN Genres g ON b.GenreID = g.GenreID
                    WHERE
                """
                params = []
                conditions = []
                if title:
                    conditions.append("LOWER(b.Title) LIKE %s")
                    params.append(f"%{title.lower()}%")
                if author:
                    conditions.append("LOWER(a.AuthorName) LIKE %s")
                    params.append(f"%{author.lower()}%")
                if not conditions:
                    query = query.replace("WHERE", "")
                else:
                    query += " OR ".join(conditions)
                cursor.execute(query, params)
                books = cursor.fetchall()
                if not books:
                    return "No books available for this search criteria."
                result = []
                for book in books:
                    result.append(f"Book-{book[0]}: Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Copies: {book[4]}")
                return "\n".join(result)
            except Error as e:
                print(f"Error searching books: {e}")
                return "Error searching books."
            finally:
                cursor.close()
                conn.close()
        return "Error connecting to database."

    def return_book(self, book_id, quantity):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            book_id_num = int(book_id.split('-')[1]) if book_id.startswith('Book-') else int(book_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid book ID or quantity.")
            return
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT borrowing_id, quantity FROM borrowings WHERE user_email = %s AND BookID = %s",
                    (self.current_user, book_id_num)
                )
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "Borrowing record not found.")
                    return
                borrowing_id, borrowed_quantity = result
                if borrowed_quantity < quantity:
                    messagebox.showerror("Error", "Cannot return more copies than borrowed.")
                    return
                cursor.execute(
                    "UPDATE Books SET Copies = Copies + %s WHERE BookID = %s",
                    (quantity, book_id_num)
                )
                if borrowed_quantity == quantity:
                    cursor.execute("DELETE FROM borrowings WHERE borrowing_id = %s", (borrowing_id,))
                else:
                    cursor.execute(
                        "UPDATE borrowings SET quantity = quantity - %s WHERE borrowing_id = %s",
                        (quantity, borrowing_id)
                    )
                conn.commit()
                messagebox.showinfo("Success", f"Successfully returned {quantity} copies of Book-{book_id_num}.")
            except Error as e:
                print(f"Error returning book: {e}")
                messagebox.showerror("Error", "Failed to return book.")
            finally:
                cursor.close()
                conn.close()

    def generate_report(self):
        if self.current_user != "admin@gmail.com":
            messagebox.showerror("Error", "Only admin can generate borrowing reports.")
            return "Access Denied."
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.BookID, b.Title, a.AuthorName, g.GenreName, br.quantity, br.user_email
                    FROM borrowings br
                    JOIN Books b ON br.BookID = b.BookID
                    JOIN Authors a ON b.AuthorID = a.AuthorID
                    JOIN Genres g ON b.GenreID = g.GenreID
                """)
                borrowings = cursor.fetchall()
                if not borrowings:
                    return "No borrowings found."
                report_lines = []
                for borrowing in borrowings:
                    report_lines.append(
                        f"Book ID: Book-{borrowing[0]}, Title: {borrowing[1]}, Author: {borrowing[2]}, "
                        f"Genre: {borrowing[3]}, Quantity Borrowed: {borrowing[4]}, Borrower: {borrowing[5]}"
                    )
                return "\n".join(report_lines)
            except Error as e:
                print(f"Error generating report: {e}")
                return "Error generating report."
            finally:
                cursor.close()
                conn.close()
        return "Error connecting to database."

class LibraryManagementGUI:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.load_background_image()
        self.setup_styles()
        self.main_menu(logged_in=False)
        self.root.bind("<Configure>", self.resize_background)

    def setup_styles(self):
        style = ttk.Style()
        style.configure("Rounded.TFrame", background="#f0f0f0", padding=10)
        style.configure("Large.TButton", font=("Helvetica", 14), padding=(5, 5))

    def load_background_image(self):
        url = "https://img.freepik.com/premium-photo/abstract-blur-library-blurred-book-shelves-hall-generative-ai_791316-6098.jpg?semt=ais_hybrid"
        image_path = "background.jpg"
        if not os.path.exists(image_path):
            try:
                urllib.request.urlretrieve(url, image_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load background image: {e}")
                self.bg_image = None
                return
        self.bg_image = Image.open(image_path)

    def resize_background(self, event=None):
        if hasattr(self, 'canvas') and self.canvas.winfo_exists() and self.bg_image:
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            resized_bg = self.bg_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_bg)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def setup_page_with_background(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.pack(fill="both", expand=True)
        self.resize_background()

    def main_menu(self, logged_in):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, style="Rounded.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)
        ttk.Label(frame, text="Library Management System", font=("Times New Roman", 28)).pack(pady=30)
        if not logged_in:
            ttk.Button(frame, text="Register", command=self.register, style="Large.TButton").pack(pady=30)
            ttk.Button(frame, text="Login", command=self.login, style="Large.TButton").pack(pady=30)
        else:
            ttk.Button(frame, text="Search Books", command=self.search_books, style="Large.TButton").pack(pady=5)
            if self.system.current_user != "admin@gmail.com":
                ttk.Button(frame, text="Borrow Book", command=self.borrow_book, style="Large.TButton").pack(pady=5)
            ttk.Button(frame, text="Return Book", command=self.return_book, style="Large.TButton").pack(pady=5)
            if self.system.current_user == "admin@gmail.com":
                ttk.Button(frame, text="View Borrowing Report", command=self.view_report, style="Large.TButton").pack(pady=5)
            ttk.Button(frame, text="View All Books", command=self.view_all_books, style="Large.TButton").pack(pady=5)
            if self.system.current_user == "admin@gmail.com":
                ttk.Button(frame, text="Add Book", command=self.add_book, style="Large.TButton").pack(pady=5)
            # Logout button for all users, including admin
            ttk.Button(frame, text="Logout", command=self.logout, style="Large.TButton").pack(pady=20)

    def register(self):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Register", font=("Times New Roman", 25)).pack(pady=5)
        ttk.Label(frame, text="Email:").pack(pady=(5, 2))
        email_entry = ttk.Entry(frame)
        email_entry.pack()
        ttk.Label(frame, text="Password:").pack(pady=(5, 2))
        password_entry = ttk.Entry(frame, show="*")
        password_entry.pack()
        show_password_var = tk.BooleanVar()
        show_password_checkbox = ttk.Checkbutton(frame, text="Show Password", variable=show_password_var,
            command=lambda: self.toggle_password_visibility(password_entry, show_password_var))
        show_password_checkbox.pack(pady=5)
        ttk.Button(frame, text="Register", command=lambda: self.register_user_action(email_entry.get(), password_entry.get())).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=False)).pack(pady=5)

    def register_user_action(self, email, password):
        self.system.register_user(email, password)
        self.main_menu(logged_in=False)

    def login(self):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Login", font=("Times New Roman", 25)).pack(pady=5)
        ttk.Label(frame, text="Email:").pack(pady=(5, 2))
        email_entry = ttk.Entry(frame)
        email_entry.pack()
        ttk.Label(frame, text="Password:").pack(pady=(5, 2))
        password_entry = ttk.Entry(frame, show="*")
        password_entry.pack()
        show_password_var = tk.BooleanVar()
        show_password_checkbox = ttk.Checkbutton(frame, text="Show Password", variable=show_password_var,
            command=lambda: self.toggle_password_visibility(password_entry, show_password_var))
        show_password_checkbox.pack(pady=5)
        ttk.Button(frame, text="Login", command=lambda: self.attempt_login(email_entry.get(), password_entry.get())).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=False)).pack(pady=5)

    def attempt_login(self, email, password):
        if self.system.login_user(email, password):
            self.main_menu(logged_in=True)

    def logout(self):
        self.system.current_user = None
        messagebox.showinfo("Logout", "You have been logged out successfully.")
        self.main_menu(logged_in=False)

    def toggle_password_visibility(self, entry, show_var):
        entry.config(show="" if show_var.get() else "*")

    def add_book(self):
        if self.system.current_user != "admin@gmail.com":
            messagebox.showerror("Error", "Only admin can add books.")
            return
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=400)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Add Book", font=("Times New Roman", 25)).pack(pady=5)
        ttk.Label(frame, text="Title:").pack(pady=(5, 2))
        title_entry = ttk.Entry(frame)
        title_entry.pack()
        ttk.Label(frame, text="Author:").pack(pady=(5, 2))
        author_entry = ttk.Entry(frame)
        author_entry.pack()
        ttk.Label(frame, text="Copies:").pack(pady=(5, 2))
        copies_entry = ttk.Entry(frame)
        copies_entry.pack()
        ttk.Label(frame, text="Genre:").pack(pady=(5, 2))
        genre_entry = ttk.Entry(frame)
        genre_entry.pack()
        ttk.Button(frame, text="Add Book", command=lambda: self.add_book_action(
            title_entry.get(), author_entry.get(), copies_entry.get(), genre_entry.get()
        )).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=True)).pack(pady=5)

    def add_book_action(self, title, author, copies, genre):
        self.system.add_book(title, author, copies, genre)
        self.main_menu(logged_in=True)

    def show_search_results(self, title, author):
        results = self.system.search_books(title, author)
        result_window = tk.Toplevel(self.root)
        result_window.title("Search Results")
        result_window.geometry("400x300")
        ttk.Label(result_window, text="Search Results", font=("Times New Roman", 20)).pack(pady=10)
        result_text = tk.Text(result_window, wrap="word", height=10, width=40)
        result_text.pack(pady=10)
        result_text.insert("end", results)
        result_text.config(state="disabled")
        ttk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=5)

    def search_books(self):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Search Books", font=("Times New Roman", 25)).pack(pady=25)
        ttk.Label(frame, text="Title:").pack(pady=(10, 5))
        title_entry = ttk.Entry(frame)
        title_entry.pack()
        ttk.Label(frame, text="Author:").pack(pady=(10, 5))
        author_entry = ttk.Entry(frame)
        author_entry.pack()
        ttk.Button(frame, text="Search", command=lambda: self.show_search_results(title_entry.get(), author_entry.get())).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=True)).pack(pady=5)

    def view_all_books(self):
        self.setup_page_with_background()
        all_books_window = tk.Toplevel(self.root)
        all_books_window.title("All Books")
        all_books_window.geometry("500x400")
        ttk.Label(all_books_window, text="All Books", font=("Times New Roman", 25)).pack(pady=10)
        canvas = tk.Canvas(all_books_window)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(all_books_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        books_text = tk.Text(frame, wrap="word", height=15, width=50)
        books_text.pack(pady=10)
        conn = self.system.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.BookID, b.Title, a.AuthorName, g.GenreName, b.Copies
                    FROM Books b
                    JOIN Authors a ON b.AuthorID = a.AuthorID
                    JOIN Genres g ON b.GenreID = g.GenreID
                """)
                books = cursor.fetchall()
                all_books_info = ""
                for book in books:
                    all_books_info += f"Book ID: Book-{book[0]}\n"
                    all_books_info += f"Title: {book[1]}\n"
                    all_books_info += f"Author: {book[2]}\n"
                    all_books_info += f"Genre: {book[3]}\n"
                    all_books_info += f"Copies Available: {book[4]}\n\n"
                books_text.insert("end", all_books_info)
                books_text.config(state="disabled")
            except Error as e:
                print(f"Error fetching books: {e}")
                books_text.insert("end", "Error fetching books.")
                books_text.config(state="disabled")
            finally:
                cursor.close()
                conn.close()
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        # Move Close button beneath the text
        close_button = ttk.Button(frame, text="Close", command=lambda: self.close_books_window(all_books_window))
        close_button.pack(pady=5)

    def close_books_window(self, all_books_window):
        all_books_window.destroy()
        self.main_menu(logged_in=True)

    def borrow_book(self):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Borrow Book", font=("Times New Roman", 25)).pack(pady=10)
        ttk.Label(frame, text="Book ID (e.g., Book-1):").pack(pady=(10, 5))
        book_id_entry = ttk.Entry(frame)
        book_id_entry.pack()
        ttk.Label(frame, text="Quantity:").pack(pady=(10, 5))
        quantity_entry = ttk.Entry(frame)
        quantity_entry.pack()
        ttk.Button(frame, text="Borrow", command=lambda: self.borrow_book_action(book_id_entry.get(), quantity_entry.get())).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=True)).pack(pady=5)

    def borrow_book_action(self, book_id, quantity):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            book_id_num = int(book_id.split('-')[1]) if book_id.startswith('Book-') else int(book_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid book ID or quantity.")
            return
        conn = self.system.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Copies FROM Books WHERE BookID = %s", (book_id_num,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "Invalid book ID.")
                    return
                available_copies = result[0]
                if available_copies < quantity:
                    messagebox.showerror("Error", "Not enough copies available.")
                    return
                cursor.execute(
                    "UPDATE Books SET Copies = Copies - %s WHERE BookID = %s",
                    (quantity, book_id_num)
                )
                cursor.execute(
                    "INSERT INTO borrowings (user_email, BookID, quantity) VALUES (%s, %s, %s)",
                    (self.system.current_user, book_id_num, quantity)
                )
                conn.commit()
                messagebox.showinfo("Success", f"Successfully borrowed {quantity} copies of Book-{book_id_num}.")
            except Error as e:
                print(f"Error borrowing book: {e}")
                messagebox.showerror("Error", "Failed to borrow book.")
            finally:
                cursor.close()
                conn.close()
        self.main_menu(logged_in=True)

    def return_book(self):
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=400, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Return Book", font=("Times New Roman", 25)).pack(pady=5)
        ttk.Label(frame, text="Book ID (e.g., Book-1):").pack(pady=(5, 2))
        book_id_entry = ttk.Entry(frame)
        book_id_entry.pack()
        ttk.Label(frame, text="Quantity:").pack(pady=(5, 2))
        quantity_entry = ttk.Entry(frame)
        quantity_entry.pack()
        ttk.Button(frame, text="Return", command=lambda: self.return_book_action(book_id_entry.get(), quantity_entry.get())).pack(pady=10)
        ttk.Button(frame, text="Back", command=lambda: self.main_menu(logged_in=True)).pack(pady=5)

    def return_book_action(self, book_id, quantity):
        self.system.return_book(book_id, quantity)
        self.main_menu(logged_in=True)

    def view_report(self):
        if self.system.current_user != "admin@gmail.com":
            messagebox.showerror("Error", "Only admin can view borrowing reports.")
            return
        self.setup_page_with_background()
        frame = ttk.Frame(self.root, width=570, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.pack_propagate(False)
        ttk.Label(frame, text="Borrowing Report", font=("Times New Roman", 25)).pack(pady=10)
        canvas = tk.Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        text_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=text_frame, anchor="nw")
        report_text = tk.Text(text_frame, wrap="word", height=20, width=55)
        report_text.pack(pady=5)
        borrowings_info = self.system.generate_report()
        report_text.insert("end", borrowings_info)
        report_text.config(state="disabled")
        text_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        # Move Back button beneath the text
        back_button = ttk.Button(text_frame, text="Back", command=lambda: self.main_menu(logged_in=True))
        back_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    system = LibraryManagementSystem()
    gui = LibraryManagementGUI(root, system)
    root.mainloop()
