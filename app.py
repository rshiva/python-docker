from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nbt040:password@books-psql:5432/books_api"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BooksModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    read = db.Column(db.Boolean(), default=False)

    def __init__(self, name, author, read):
        self.name = name
        self.author = author
        self.read = read

    def __repr__(self):
        return f"<Book {self.name}>"


@app.route('/')
def hello():
    return {"hello": "world"}


@app.route("/books", methods=['POST', 'GET'])
def books():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            new_book = BooksModel(
                name=data['name'], author=data['author'], read=data['read'])
            db.session.add(new_book)
            db.session.commit()
            return {"message": f"Book {new_book.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == "GET":
        books = BooksModel.query.all()
        results = [
            {
                "name": book.name,
                "author": book.author,
                "read": book.read
            }
            for book in books]
        return {"count": len(results), "books": results}


if __name__ == '__main__':
    app.run(debug=True)
