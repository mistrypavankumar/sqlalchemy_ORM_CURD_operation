import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Float, Boolean, select, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()

# Many-to-many relationship table for books and categories
book_category = Table('book_category', Base.metadata,
                      Column('book_id', Integer, ForeignKey('books.id')),
                      Column('category_id', Integer,
                             ForeignKey('categories.id'))
                      )

# Many-to-many relationship table for books and tags
book_tag = Table('book_tag', Base.metadata,
                 Column('book_id', Integer, ForeignKey('books.id')),
                 Column('tag_id', Integer, ForeignKey('tags.id'))
                 )


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_year = Column(Integer)
    quantity = Column(Integer, default=1)

    borrowings = relationship("Borrowing", back_populates="book")
    categories = relationship(
        "Category", secondary=book_category, back_populates="books")
    tags = relationship("Tag", secondary=book_tag, back_populates="books")

    @hybrid_property
    def is_available(self):
        return self.quantity > len([b for b in self.borrowings if b.return_date is None])

    @is_available.expression
    def is_available(cls):
        return cls.quantity > (
            select([func.count(Borrowing.id)])
            .where(Borrowing.book_id == cls.id)
            .where(Borrowing.return_date.is_(None))
            .as_scalar()
        )


class Patron(Base):
    __tablename__ = 'patrons'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    membership_date = Column(Date, default=func.current_date())

    borrowings = relationship("Borrowing", back_populates="patron")
    fines = relationship("Fine", back_populates="patron")

    @hybrid_property
    def total_fines(self):
        return sum(fine.amount for fine in self.fines if not fine.paid)


class Borrowing(Base):
    __tablename__ = 'borrowings'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    patron_id = Column(Integer, ForeignKey('patrons.id'), nullable=False)
    borrow_date = Column(Date, nullable=False, default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)

    book = relationship("Book", back_populates="borrowings")
    patron = relationship("Patron", back_populates="borrowings")

    @hybrid_property
    def is_overdue(self):
        return self.return_date is None and self.due_date < datetime.date.today()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", secondary=book_category,
                         back_populates="categories")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", secondary=book_tag, back_populates="tags")


class Fine(Base):
    __tablename__ = 'fines'

    id = Column(Integer, primary_key=True)
    patron_id = Column(Integer, ForeignKey('patrons.id'), nullable=False)
    amount = Column(Float, nullable=False)
    reason = Column(String(200))
    date = Column(Date, default=func.current_date())
    paid = Column(Boolean, default=False)

    patron = relationship("Patron", back_populates="fines")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
