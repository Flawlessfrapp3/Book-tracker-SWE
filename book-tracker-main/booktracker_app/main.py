import tkinter as tk
from tkinter import messagebox
import json

class BookCollection:
    def __init__(self, filename="books.json"):
        self._filename = filename  # encapsulation: private attribute
        self._my_books = []        # encapsulation: private attribute
        self._wishlist = []        # encapsulation: private attribute
        self.load_data()

    @property #<-- keeps the underlying data private
    def my_books(self):
        return self._my_books

    @property
    def wishlist(self):
        return self._wishlist

    def save_data(self):
        with open(self._filename, "w") as file:
            json.dump({"my_books": self._my_books, "wishlist": self._wishlist}, file)

    def load_data(self):
        try:
            with open(self._filename, "r") as file:
                data = json.load(file)
                self._my_books = data.get("my_books", [])
                self._wishlist = data.get("wishlist", [])
        except FileNotFoundError:
            pass

    def add_book(self, collection, book):
        if collection == "my_books":
            book["status"] = "To Read"
            self._my_books.append(book)
        elif collection == "wishlist":
            self._wishlist.append(book)
        self.save_data()

    def delete_book(self, collection, index):
        if collection == "my_books":
            self._my_books.pop(index)
        else:
            self._wishlist.pop(index)
        self.save_data()

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy Book Tracker")
        self.root.minsize(600, 400)
        self.collection = BookCollection()
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.show_home()

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(6):
            self.main_frame.grid_rowconfigure(i, weight=1)
        title_label = tk.Label(self.main_frame, text="Welcome to Cozy Book Tracker",
                               font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, pady=20)
        button_style = {"font": ("Helvetica", 12), "padx": 20, "pady": 10, "width": 20}
        tk.Button(self.main_frame, text="Add Book to My Books",
                  command=lambda: self.add_book_gui("my_books"),
                  bg="#2196F3", fg="white", **button_style).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="Add Book to Wishlist",
                  command=lambda: self.add_book_gui("wishlist"),
                  bg="#2196F3", fg="white", **button_style).grid(row=2, column=0, pady=5)
        tk.Button(self.main_frame, text="View My Books",
                  command=lambda: self.view_books_gui("my_books"),
                  bg="#4CAF50", fg="white", **button_style).grid(row=3, column=0, pady=5)
        tk.Button(self.main_frame, text="View Wishlist",
                  command=lambda: self.view_books_gui("wishlist"),
                  bg="#4CAF50", fg="white", **button_style).grid(row=4, column=0, pady=5)
        tk.Button(self.main_frame, text="Exit", command=self.root.quit,
                  bg="#f44336", fg="white", **button_style).grid(row=5, column=0, pady=5)

    def add_book_gui(self, collection):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        container = tk.Frame(self.main_frame, bg="#f0f0f0", padx=20, pady=20)
        container.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        for i in range(5):
            container.grid_rowconfigure(i, weight=1)
        tk.Label(container, text="Title:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, sticky="w")
        title_entry = tk.Entry(container, font=("Helvetica", 12))
        title_entry.grid(row=1, column=0, pady=5, sticky="ew")
        tk.Label(container, text="Author:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=2, column=0, pady=10, sticky="w")
        author_entry = tk.Entry(container, font=("Helvetica", 12))
        author_entry.grid(row=3, column=0, pady=5, sticky="ew")
        button_frame = tk.Frame(container, bg="#f0f0f0")
        button_frame.grid(row=4, column=0, pady=20)
        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            if not title or not author:
                messagebox.showerror("Error", "Both title and author are required!")
                return
            book = {"title": title, "author": author}
            self.collection.add_book(collection, book)
            messagebox.showinfo("Success", f"Book '{title}' added to {'My Books' if collection == 'my_books' else 'Wishlist'}!")
            self.show_home()
        tk.Button(button_frame, text="Save", command=save_book,
                  font=("Helvetica", 12), bg="#4CAF50", fg="white",
                  padx=20, pady=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back", command=self.show_home,
                  font=("Helvetica", 12), bg="#f44336", fg="white",
                  padx=20, pady=10).pack(side="left", padx=5)

    def view_books_gui(self, collection):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        container = tk.Frame(self.main_frame, bg="#f0f0f0", padx=20, pady=20)
        container.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        canvas = tk.Canvas(container, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        books = self.collection.my_books if collection == "my_books" else self.collection.wishlist
        if not books:
            tk.Label(scrollable_frame, text="No books found.",
                     font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        else:
            for index, book in enumerate(books, start=1):
                status = book.get("status", "N/A")
                book_frame = tk.Frame(scrollable_frame, bg="#f0f0f0", pady=5)
                book_frame.pack(fill="x", padx=5)
                info_frame = tk.Frame(book_frame, bg="#f0f0f0")
                info_frame.pack(fill="x", expand=True)
                tk.Label(info_frame,
                         text=f"{index}. {book['title']} by {book['author']} (Status: {status})",
                         font=("Helvetica", 12), bg="#f0f0f0").pack(side="left", anchor="w")
                def delete_callback(idx=index-1):
                    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{books[idx]['title']}'?"):
                        self.collection.delete_book(collection, idx)
                        self.view_books_gui(collection)
                tk.Button(info_frame, text="Delete",
                          command=lambda idx=index-1: delete_callback(idx),
                          font=("Helvetica", 10), bg="#f44336", fg="white",
                          padx=10, pady=5).pack(side="right", padx=5)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        tk.Button(container, text="Back", command=self.show_home,
                  font=("Helvetica", 12), bg="#f44336", fg="white",
                  padx=20, pady=10).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()





