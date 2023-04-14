from flask import Flask
from flask_cors import CORS

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from database import db
from routes import appc



app = Flask(__name__)
CORS(app)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
)
db.init_app(app)
app.register_blueprint(appc)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )