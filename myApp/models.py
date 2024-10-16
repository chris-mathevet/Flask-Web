from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import Mapped

fav_books = db.Table("fav_books",
        db.Column("username",db.String(50),db.ForeignKey("user.username"), primary_key =True),
        db.Column("id_book",db.Integer, db.ForeignKey("book.id"), primary_key =True),
    )

# fav_books = db.Table("fav_books",
#         db.metadata,
#         db.Column("username",db.ForeignKey("user.username"), primary_key =True),
#         db.Column("id_book", db.ForeignKey("book.id"), primary_key =True),
#     )

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self ):
        return self.name

class Book(db.Model):
    id = db.Column(db.Integer , primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))
    favorites_book = db.relationship("User",secondary=fav_books,back_populates="favorites")

    def __repr__(self ):
        return self.title
    
# class fav_books(db.Model):
#     user = db.Column("username",db.String(50),db.ForeignKey("user.username"), primary_key =True)
#     book = db.Column("id_book",db.Integer, db.ForeignKey("book.id"), primary_key =True)

class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    favorites = db.relationship("Book", secondary=fav_books,back_populates="favorites_book")

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self.username

def get_sample():
    return Book.query.limit(10).all()

def get_book_by_id(id:int):
    return Book.query.get_or_404(id)

def get_author_by_id(id:int):
    return Author.query.get_or_404(id)

def get_books_by_author(id:int):
    return Author.query.get_or_404(id).books.all()

def get_user_by_username(username:str):
    return User.query.get_or_404(username)

def get_fav_books(username:str):
    return User.query.get_or_404(username).favorites

def add_favorites(username:str,id_book:int):
    user = get_user_by_username(username)
    book = get_book_by_id(id_book)
    if book not in user.favorites:
        user.favorites.append(book)
        db.session.commit()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)