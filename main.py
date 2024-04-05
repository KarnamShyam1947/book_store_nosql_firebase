from app.home import home
from app.auth import auth
from app.book import book
from flask import Flask

app = Flask(__name__)
app.config.from_prefixed_env()

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(book)
