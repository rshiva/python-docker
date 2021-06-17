from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


@app.route('/')
def hello():
    return {"hello": "world"}


if __name__ == '__main__':
    app.run(debug=True)
