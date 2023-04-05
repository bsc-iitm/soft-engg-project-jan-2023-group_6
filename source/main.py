import os

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy



curr_dir = os.path.abspath(os.path.dirname(__name__))
config = {
    "SECRET_KEY": "mySuperDuperOmegaGigaChadSecretKey",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///" + os.path.join(curr_dir, 'database.sqlite3'),
}

app = Flask(__name__)
app.config.from_mapping(config)

db = SQLAlchemy()
db.init_app(app)



@app.route('/', methods=['GET'])
def home():
    return "You have found this API. Badhai ho"


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )