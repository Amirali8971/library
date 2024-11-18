import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


conn = sqlite3.connect('books.db')
c = conn.cursor()


c.execute('''
CREATE TABLE IF NOT EXISTS books 
             (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)
             ''')

conn.commit()


def is_duplicate(title, author, year):
    c.execute("SELECT * FROM books WHERE title = ? AND author = ? AND year = ?", (title, author, year))
    return c.fetchone() is not None


def add_book():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()

    if title and author and year:

        if is_duplicate(title, author, year):
            messagebox.showwarning("کتاب تکراری", "این کتاب از قبل در کتابخانه موجود است.")
        else:
            c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
            conn.commit()
            load_books()
            messagebox.showinfo("موفقیت", "کتاب با موفقیت اضافه شد.")
    else:
        messagebox.showerror("خطا", "لطفاً همه فیلدها را پر کنید.")


def delete_book():
    selected_item = treeview.selection()
    if selected_item:
        book_id = treeview.item(selected_item)['values'][0]
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        renumber_ids()
        load_books()
        messagebox.showinfo("موفقیت", "کتاب با موفقیت حذف شد.")
    else:
        messagebox.showerror("خطا", "لطفاً یک کتاب را انتخاب کنید.")


def renumber_ids():
    c.execute("SELECT * FROM books ORDER BY id")
    books = c.fetchall()
    new_id = 1
    for book in books:
        old_id = book[0]
        c.execute("UPDATE books SET id = ? WHERE id = ?", (new_id, old_id))
        new_id += 1
    conn.commit()


def edit_book():
    selected_item = treeview.selection()
    if selected_item:
        book_id = treeview.item(selected_item)['values'][0]
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        if title and author and year:
            c.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, book_id))
            conn.commit()
            load_books()
            messagebox.showinfo("موفقیت", "کتاب با موفقیت ویرایش شد.")
        else:
            messagebox.showerror("خطا", "لطفاً همه فیلدها را پر کنید.")
    else:
        messagebox.showerror("خطا", "لطفاً یک کتاب را انتخاب کنید.")


def load_books():
    for item in treeview.get_children():
        treeview.delete(item)
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    for book in books:
        treeview.insert('', 'end', values=book)


root = tk.Tk()
root.title("مدیریت کتابخانه")
root.geometry("700x700")

tk.Label(root, text="عنوان").place(x=20, y=20)
entry_title = tk.Entry(root)
entry_title.place(x=100, y=20)

tk.Label(root, text="نویسنده").place(x=20, y=60)
entry_author = tk.Entry(root)
entry_author.place(x=100, y=60)

tk.Label(root, text="سال انتشار").place(x=20, y=100)
entry_year = tk.Entry(root)
entry_year.place(x=100, y=100)

tk.Button(root, text="افزودن کتاب", command=add_book).place(x=20, y=150)
tk.Button(root, text="حذف کتاب", command=delete_book).place(x=100, y=150)
tk.Button(root, text="ویرایش کتاب", command=edit_book).place(x=200, y=150)


treeview = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year"), show='headings', height=15)
treeview.heading("ID", text="شناسه")
treeview.heading("Title", text="عنوان")
treeview.heading("Author", text="نویسنده")
treeview.heading("Year", text="سال انتشار")
treeview.column("ID", width=70)
treeview.column("Title", width=200)
treeview.column("Author", width=150)
treeview.column("Year", width=100)
treeview.place(x=20, y=200, width=550, height=350)

load_books()

root.mainloop()




