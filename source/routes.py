import json
from models import User, Faq, Ticket
from database import db
from flask import  request, Blueprint
from helpers import generate_password_hash, authenticate_user, token_required

appc = Blueprint("appc", __name__)

@appc.route('/', methods=['GET'])
def home():
    return "You have found this API. Badhai ho"

@appc.route('/register', methods=['POST'])
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

@appc.route('/login', methods=['POST'])
def login():
    auth_details = dict(request.authorization)
    auth_data = authenticate_user(auth_details)
    return auth_data
 
@appc.route('/ticket', methods=['POST'])
@token_required
def create_ticket(current_user):
    try:
        if(current_user.admin == 1):
            return "Forbidden",403
        
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
    except:
        return 'Bad Request',400


@appc.route('/faq', methods=['GET'])
def all_faqs():
    faqs = Faq.query.all()
    faqs = [faq.serialized for faq in faqs]
    return {
        'faqs': faqs
    }