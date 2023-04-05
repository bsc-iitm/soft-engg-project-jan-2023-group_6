import os

curr_dir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(curr_dir, 'database.sqlite3')

SECRET_KEY = "gigaChadSecretKey"
ALGORITHM = "HS256"