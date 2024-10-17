from actions import add_book, search_books, update_book_by_isbn_number, delete_book_by_isbn_number
from db_connect import connectDB
from models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from colorama import Fore, init

from view import displayTasks, get_top_5_books, display_search_results, add_book_input, update_book_input, delete_book_input

# Define the connection parameters
host = 'localhost'
database = "test"
user = "root"
password = "root"
port = 3306

# Create the SQLAlchemy engine
engine = create_engine(connectDB(host, database, user, password, port))

# Create the tables in the database if they don't exist
Base.metadata.create_all(engine, checkfirst=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

while True:
    # Display all tasks
    choice = displayTasks()

    if choice == 1:
        # Shows top 5 books
        get_top_5_books(session)
    elif choice == 2:
        keyword = input("Enter the keyword to search: ")
        search_results = search_books(session, keyword)

        # This shows the books based on the search keywords
        display_search_results(search_results)
    elif choice == 3:

        # This function will take the input from the user
        title, author, isbn, publication_year, quantity, categories, tags = add_book_input()

        # This function will add a new book into the databse
        add_book(session=session, title=title, author=author, isbn=isbn,
                 publication_year=publication_year, quantity=quantity, categories=categories, tags=tags)
    elif choice == 4:
        # This function will take the input from the user
        isbn, title, author, publication_year, quantity, categories, tags = update_book_input()

        # This function will update the book based on the ISBN number
        update_book_by_isbn_number(
            session, isbn, title, author, publication_year, quantity, categories, tags)
    elif choice == 5:

        # This function will take the input from the user
        isbn = delete_book_input()

        if isbn:
            # This function will delete the book based on the ISBN number
            delete_book_by_isbn_number(session, isbn)

    elif choice == 6:
        init(autoreset=True)

        # clear screen
        print("\033[H\033[J")
        print(f"{Fore.GREEN}Exiting the library management system")
        break

try:
    # Commit the transaction
    session.commit()
except Exception as e:
    print(f"An error occurred: {e}")
    session.rollback()

finally:
    # Close the session
    session.close()
