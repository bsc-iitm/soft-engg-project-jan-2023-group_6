import json

from flask import Flask, request

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from database import db
from models import User, Faq, Ticket
from helpers import generate_password_hash, authenticate_user, token_required



app = Flask(__name__)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
)
db.init_app(app)



@app.route('/', methods=['GET'])
def home():
    return "You have found this API. Badhai ho"

@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        name=data['name'],
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        admin=data['admin']
    )
    db.session.add(new_user)
    db.session.commit()
    return {'success': True}

@app.route('/login', methods=['POST'])
def login():
    auth_details = dict(request.authorization)
    auth_data = authenticate_user(auth_details)
    return auth_data

@app.route('/ticket', methods=['POST'])
@token_required
def create_ticket(current_user):
    ticket_data = json.loads(request.data)
    new_ticket = Ticket(
        title=ticket_data['title'],
        content=ticket_data['content'],
        date=ticket_data['date'],
        status='Open',
        user_id=current_user.id,
        likes=0
    )
    db.session.add(new_ticket)
    db.session.commit()
    return {'success': True}


@app.route('/faq', methods=['GET'])
def all_faqs():
    faqs = Faq.query.all()
    faqs = [faq.serialized for faq in faqs]
    return {
        'faqs': faqs
    }





if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )