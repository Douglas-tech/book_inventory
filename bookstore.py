import sqlite3

# connect to the database
conn = sqlite3.connect('ebookstore.db')

# drop the books table if it exists
conn.execute("DROP TABLE IF EXISTS books")

# create the books table
conn.execute('''CREATE TABLE IF NOT EXISTS books
             (id INT PRIMARY KEY NOT NULL,
             title TEXT NOT NULL,
             author TEXT NOT NULL,
             qty INT NOT NULL);''')

# populate the table with data
conn.execute("INSERT INTO books (id, title, author, qty) \
              VALUES (3001, 'A Tale of Two Cities', 'Charles Dickens', 30)")

conn.execute("INSERT INTO books (id, title, author, qty) \
              VALUES (3002, 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 40)")

conn.execute("INSERT INTO books (id, title, author, qty) \
              VALUES (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25)")

conn.execute("INSERT INTO books (id, title, author, qty) \
              VALUES (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37)")

conn.execute("INSERT INTO books (id, title, author, qty) \
              VALUES (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)")

conn.commit()

# define functions for the bookstore clerk program
def add_book():
    id = int(input("Enter book ID: "))
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    qty = int(input("Enter book quantity: "))
    conn.execute("INSERT INTO books (id, title, author, qty) \
                  VALUES (?, ?, ?, ?)", (id, title, author, qty))
    conn.commit()
    print("Book added successfully.")

def update_book():
    id = int(input("Enter book ID: "))
    title = input("Enter new title (press enter to keep current): ")
    author = input("Enter new author (press enter to keep current): ")
    qty = input("Enter new quantity (press enter to keep current): ")
    update_query = "UPDATE books SET"
    update_params = []
    if title:
        update_query += " title=?,"
        update_params.append(title)
    if author:
        update_query += " author=?,"
        update_params.append(author)
    if qty:
        update_query += " qty=?,"
        update_params.append(int(qty))
    # remove trailing comma
    update_query = update_query[:-1]
    update_query += " WHERE id=?"
    update_params.append(id)
    conn.execute(update_query, tuple(update_params))
    conn.commit()
    print("Book updated successfully.")

def delete_book():
    id = int(input("Enter book ID: "))
    conn.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    print("Book deleted successfully.")

def search_books():
    search_term = input("Enter search term: ")
    results = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                           ('%'+search_term+'%', '%'+search_term+'%')).fetchall()
    if not results:
        print("No results found.")
    else:
        for row in results:
            print("ID: {}, Title: {}, Author: {}, Quantity: {}".format(*row))

# function to show all books
def show_all_books():
    # connect to the database
    conn = sqlite3.connect('ebookstore.db')

    # execute the select statement
    cursor = conn.execute("SELECT * FROM books")

    # loop through the rows and print each book
    for row in cursor:
        print(f"{row[0]} - {row[1]} by {row[2]} ({row[3]} copies)")

    # close the database connection
    conn.close()

# main loop for the program
while True:
    print("Welcome to the bookstore clerk program, jou lekker ding!")
    print("Please select an option:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. Show all books in inventory")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_books()
    elif choice == "5":
        show_all_books()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()
