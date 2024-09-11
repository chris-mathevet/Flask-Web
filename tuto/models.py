from .app import db


class Author(db.Model):
    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True)
        self.name = db.Column(db.String(100))
class Book(db.Model ):
    def __init__(self):
        self.id = db.Column(db.Integer , primary_key =True)
        self.price = db.Column(db.Float)
        self.title = db.Column(db.String(100))
        self.url = db.Column(db.String(100))
        self.img = db.Column(db.String(100))
        self.author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
        self.author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))
        
def get_sample():
    return Book.query.limit(10).all()