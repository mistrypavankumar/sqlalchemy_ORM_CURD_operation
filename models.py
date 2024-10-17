from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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

# This Book class define the books table which contains
# the details of the books like title, author, isbn, publication year


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_year = Column(Integer)
    quantity = Column(Integer, default=1)

    categories = relationship(
        "Category", secondary=book_category, back_populates="books")
    tags = relationship("Tag", secondary=book_tag, back_populates="books")


# This Category class define the categories table which contains
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", secondary=book_category,
                         back_populates="categories")


# This Tag class define the tags table which contains
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", secondary=book_tag, back_populates="tags")
