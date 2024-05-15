import sqlite3
import datetime

# Conexión a la base de datos 
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Creación de las tablas 
cursor.execute('''CREATE TABLE books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                )''')

cursor.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE loans (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    book_id INTEGER NOT NULL,
                    loan_date TEXT NOT NULL,
                    return_date TEXT
                )''')

def add_book(title, author, quantity):
    cursor.execute('INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)', (title, author, quantity))
    conn.commit()
    print("Libro agregado correctamente.")

def add_user(name):
    cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()
    print("Usuario agregado correctamente.")

def borrow_book(user_id, book_id):
    loan_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute('INSERT INTO loans (user_id, book_id, loan_date) VALUES (?, ?, ?)', (user_id, book_id, loan_date))
    cursor.execute('UPDATE books SET quantity = quantity - 1 WHERE id = ?', (book_id,))
    conn.commit()
    print("Libro prestado correctamente.")

def return_book(user_id, book_id):
    return_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute('UPDATE loans SET return_date = ? WHERE user_id = ? AND book_id = ? AND return_date IS NULL',
                   (return_date, user_id, book_id))
    cursor.execute('UPDATE books SET quantity = quantity + 1 WHERE id = ?', (book_id,))
    conn.commit()
    print("Libro devuelto correctamente.")

def display_books():
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    if books:
        print("\nLista de libros:")
        for book in books:
            print(f"ID: {book[0]}, Título: {book[1]}, Autor: {book[2]}, Cantidad disponible: {book[3]}")
    else:
        print("No hay libros disponibles.")

def display_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    if users:
        print("\nLista de usuarios:")
        for user in users:
            print(f"ID: {user[0]}, Nombre: {user[1]}")
    else:
        print("No hay usuarios registrados.")

def edit_book(book_id, title=None, author=None, quantity=None):
    # Obtener los datos actuales del libro
    cursor.execute('SELECT title, author, quantity FROM books WHERE id = ?', (book_id,))
    current_data = cursor.fetchone()
    current_title, current_author, current_quantity = current_data

    # Verificar si se proporcionaron nuevos datos
    new_title = title if title else current_title
    new_author = author if author else current_author
    new_quantity = quantity if quantity else current_quantity

    cursor.execute('UPDATE books SET title=?, author=?, quantity=? WHERE id=?', (new_title, new_author, new_quantity, book_id))
    conn.commit()
    print("Libro editado correctamente.")

# Menu
while True:
    print("\n1. Agregar libro")
    print("2. Editar libro")
    print("3. Agregar usuario")
    print("4. Prestar libro")
    print("5. Devolver libro")
    print("6. Mostrar libros")
    print("7. Mostrar usuarios")
    print("8. Salir")

    choice = input("Ingrese el número de la opción que desea realizar: ")

    if choice == '1':
        title = input("Ingrese el título del libro: ")
        author = input("Ingrese el autor del libro: ")
        quantity = int(input("Ingrese la cantidad disponible del libro: "))
        add_book(title, author, quantity)
    elif choice == '2':
        display_books()
        book_id = int(input("Ingrese el ID del libro que desea editar: "))
        title = input("Ingrese el nuevo título del libro (deje en blanco para mantener el mismo): ")
        author = input("Ingrese el nuevo autor del libro (deje en blanco para mantener el mismo): ")
        quantity = int(input("Ingrese la nueva cantidad disponible del libro (deje en blanco para mantener la misma): "))
        edit_book(book_id, title, author, quantity)
    elif choice == '3':
        name = input("Ingrese el nombre del usuario: ")
        add_user(name)
    elif choice == '4':
        display_users()
        user_id = int(input("Ingrese el ID del usuario que va a pedir prestado el libro: "))
        display_books()
        book_id = int(input("Ingrese el ID del libro que va a ser prestado: "))
        borrow_book(user_id, book_id)
    elif choice == '5':
        display_users()
        user_id = int(input("Ingrese el ID del usuario que va a devolver el libro: "))
        display_books()
        book_id = int(input("Ingrese el ID del libro que va a ser devuelto: "))
        return_book(user_id, book_id)
    elif choice == '6':
        display_books()
    elif choice == '7':
        display_users()
    elif choice == '8':
        break
    else:
        print("Opción no válida. Por favor, ingrese un número válido.")
