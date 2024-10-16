from sqlalchemy import func, select, or_
from sqlalchemy.orm import aliased
from models import Book, Category, Tag

from colorama import init, Fore


def add_book(session, title, author, isbn, publication_year, quantity=1, categories=None, tags=None):
    init(autoreset=True)

    # Check if the book already exists
    existing_book = session.execute(
        select(Book).filter_by(isbn=isbn)).scalar_one_or_none()
    if existing_book:
        print(f"{Fore.YELLOW}Book with ISBN {isbn} already exists.")
        return existing_book

    new_book = Book(title=title, author=author, isbn=isbn,
                    publication_year=publication_year, quantity=quantity)
    session.add(new_book)

    if categories:
        for category_name in categories:
            category = session.execute(select(Category).filter_by(
                name=category_name)).scalar_one_or_none()
            if not category:
                category = Category(name=category_name)
                session.add(category)
            new_book.categories.append(category)

    if tags:
        for tag_name in tags:
            tag = session.execute(select(Tag).filter_by(
                name=tag_name)).scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            new_book.tags.append(tag)

    session.commit()
    print(f"{Fore.GREEN}Book '{title}' has been added successfully.")
    return new_book


def update_book_by_isbn_number(session, isbn, title=None, author=None, publication_year=None, quantity=None, categories=None, tags=None):
    init(autoreset=True)

    # Check if the book already exists
    book = session.execute(select(Book).filter_by(
        isbn=isbn)).scalar_one_or_none()

    if not book:
        print(f"{Fore.YELLOW}Book with ISBN {isbn} does not exist.")
        return None

    # Update book details if provided
    if title is not None:
        book.title = title

    if author is not None:
        book.author = author

    if publication_year is not None:
        book.publication_year = publication_year

    if quantity is not None:
        book.quantity = quantity

    # Update categories
    if categories is not None:
        book.categories.clear()
        for category_name in categories:
            category = session.execute(select(Category).filter_by(
                name=category_name)).scalar_one_or_none()
            if not category:
                category = Category(name=category_name)
                session.add(category)
            book.categories.append(category)

    # Update tags
    if tags is not None:
        book.tags.clear()
        for tag_name in tags:
            tag = session.execute(select(Tag).filter_by(
                name=tag_name)).scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            book.tags.append(tag)

    try:
        session.commit()
        print(f"{Fore.GREEN}Book with ISBN {
              isbn} has been updated successfully.")
        return book
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        session.rollback()
        return None


def search_books(session, keyword):
    BookCategory = aliased(Book.categories.property.secondary)
    BookTag = aliased(Book.tags.property.secondary)

    query = (
        select(Book)
        .distinct()
        .outerjoin(BookCategory)
        .outerjoin(Category, Category.id == BookCategory.c.category_id)
        .outerjoin(BookTag)
        .outerjoin(Tag, Tag.id == BookTag.c.tag_id)
        .where(
            or_(
                Book.title.ilike(f"%{keyword}%"),
                Book.author.ilike(f"%{keyword}%"),
                Book.isbn.ilike(f"%{keyword}%"),
                Category.name.ilike(f"%{keyword}%"),
                Tag.name.ilike(f"%{keyword}%")
            )
        )
    )

    # execute the query
    search_results = session.execute(query).scalars().all()

    return search_results


def delete_book_by_isbn_number(session, isbn):
    init(autoreset=True)

    # Check if the book already exists
    book = session.execute(select(Book).filter_by(
        isbn=isbn)).scalar_one_or_none()

    if not book:
        print(f"{Fore.YELLOW}Book with ISBN {isbn} does not exist.")
        return None

    session.delete(book)
    session.commit()
    print(f"{Fore.GREEN}Book with ISBN {isbn} has been deleted successfully.")
    return book
