from sqlalchemy import select
from colorama import Fore, init


from models import Book

def displayTasks():
    init(autoreset=True)

    print(f"{Fore.GREEN}*********** Library Mangement System ***********")
    print(f"{Fore.GREEN}1. View top 5 books.")
    print(f"{Fore.GREEN}2. Search book")
    print(f"{Fore.GREEN}3. Add book")
    print(f"{Fore.GREEN}4. Update book")
    print(f"{Fore.GREEN}5. Delete book")
    print(f"{Fore.RED}6. Exit")
    print("************************************************")

    choice = int(input("Enter your choice: "))

    return choice


def get_top_5_books(session):
    init(autoreset=True) 

     # clear screen
    print("\033[H\033[J")
    
    print(f"\n{Fore.GREEN}********* Top 5 Books ************")

    # Query to get the top 10 books
    query = select(Book).limit(5)

    # Execute the query
    top_books = session.execute(query).fetchall()

    if not top_books:
        print(f"{Fore.YELLOW}No books found in the database.")
    else:
        for i, (book,) in enumerate(top_books, 1):
            print(f"{Fore.GREEN}{i}. {Fore.WHITE}{book.title}")
            print(f"   {Fore.CYAN}Author: {Fore.WHITE}{book.author}")
            print(f"   {Fore.CYAN}ISBN: {Fore.WHITE}{book.isbn}")
            print(f"   {Fore.CYAN}Publication Year: {Fore.WHITE}{book.publication_year}")
            print(f"   {Fore.CYAN}Quantity: {Fore.WHITE}{book.quantity}")
            print()

    print(f"{Fore.GREEN}************************************************")


def display_search_results(results):
    init(autoreset=True)
    
    # clear screen
    print("\033[H\033[J")

    print(f"\n{Fore.GREEN}********* Search Results ************")
    if not results:
        print(f"{Fore.YELLOW}No books found matching the search keyword")
    else:
        print(f"\n{Fore.GREEN}Found {len(results)} book(s):")
        for i, book in enumerate(results, 1):
            print(f"{Fore.GREEN}{i}. Title: {book.title}")
            print(f"   {Fore.CYAN}Author: {Fore.WHITE}{book.author}")
            print(f"   {Fore.CYAN}ISBN: {Fore.WHITE}{book.isbn}")
            print(f"   {Fore.CYAN}Publication Year: {Fore.WHITE}{book.publication_year}")
            print(f"   {Fore.CYAN}Quantity: {Fore.WHITE}{book.quantity}")
            print(f"   {Fore.CYAN}Categories: {Fore.WHITE}{', '.join(category.name for category in book.categories)}")
            print(f"   {Fore.CYAN}Tags: {Fore.WHITE}{', '.join(tag.name for tag in book.tags)}")
            print()
            print(f"{Fore.GREEN}--------------------------------------------------")
        


def add_book_input():
    print("\n*********** Add Book ***********")
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    publication_year = int(input("Enter the publication year of the book: "))
    quantity = int(input("Enter the quantity of the book: "))
    categories = input("Enter the categories of the book (comma-separated): ").split(",")
    tags = input("Enter the tags of the book (comma-separated): ").split(",")

    return title, author, isbn, publication_year, quantity, categories, tags


def update_book_input():
    init(autoreset=True)
      # clear screen
    print("\033[H\033[J")
    
    print(f"\n {Fore.GREEN}*********** Update Book **************")

    isbn = input("Enter the ISBN of the book to update: ")
    title = input("Enter the new title (press Enter to skip): ") or None
    author = input("Enter the new author (press Enter to skip): ") or None
    
    publication_year = None
    year_input = input("Enter the new publication year (press Enter to skip): ")
    if year_input:
        try:
            publication_year = int(year_input)
        except ValueError:
            print("Invalid year. Skipping publication year update.")

    quantity = None
    quantity_input = input("Enter the new quantity (press Enter to skip): ")

    if quantity_input:
        try:
            quantity = int(quantity_input)
        except ValueError:
            print("Invalid quantity. Skipping quantity update.")

    categories_input = input("Enter the new categories (comma-separated, press Enter to skip): ")
    categories = [cat.strip() for cat in categories_input.split(",")] if categories_input else None

    tags_input = input("Enter the new tags (comma-separated, press Enter to skip): ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else None

    return isbn, title, author, publication_year, quantity, categories, tags


def delete_book_input():
        init(autoreset=True)

        # clear screen
        print("\033[H\033[J")

        isbn = input(f"Enter the ISBN of the book to delete: ")

        while True:
            confirmation = input(f"{Fore.YELLOW}Do you want to delete this book? [yes/no]: ").lower()
            if confirmation in ['yes', 'y']:
                return isbn
            elif confirmation in ['no', 'n']:
                print(f"{Fore.RED}Deletion cancelled.")
                return None
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'yes' or 'no'.")