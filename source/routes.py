import json
from models import User, Faq, Ticket
from database import db
from flask import  request, Blueprint
from helpers import generate_password_hash, authenticate_user, token_required
from json import dumps, loads

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
    auth_details = json.loads(request.data)
    auth_data = authenticate_user(auth_details)
    return auth_data


# Student home page route
@appc.route('/user/tickets', methods=['GET'])
@token_required
def user_home(current_user): 
    try:
        if(current_user.admin == 1):
            return "Forbidden",403
        else:
            # user_id = json.loads(request.data)['user_id']
            user_tickets = Ticket.query.filter_by(id=current_user.id).all()
            ticket_list = {}
            for ticket_ in user_tickets:
                ticket_list[ticket_.id]={
                'title':ticket_.title,
                'content':ticket_.content,
                'date':ticket_.date,
                'likes':ticket_.likes}
            return json.dumps(ticket_list, sort_keys=True, default=str)
    except:
        return 'Bad Request',400
    
#mark as solve
@appc.route('/ticket/mark_solved', methods=['POST'])
@token_required
def mark_solved(current_user): 
    try:
        if(current_user.admin == 1): 
            return "Forbidden",403
        else:
            ticket_id = json.loads(request.data)['ticket_id']
            try:
                Ticket.query.filter_by(id=ticket_id ).update(dict(status = 'Solved'))
                db.session.commit()
            except:
                db.session.rollback()
            return 'sucessfully marked as solved', 201
    except:
        return 'Bad Request',400

# Ticket status reopen

#markDuplicate
@appc.route('/ticket/mark_duplicate', methods=['POST'])
@token_required
def mark_duplicate(current_user): 
    try:
        if(current_user.admin == 0): 
            return "Forbidden",403
        else:
            data = json.loads(request.data)
            ticket_id = data['ticket_id']
            duplicate_id = data['duplicate_id']
            try:
                Ticket.query.filter_by(id=ticket_id ).update(dict(duplicate = duplicate_id))
                db.session.commit()
            except:
                db.session.rollback()
                return 'Bad Request', 401
            return 'sucessfully marked as solved', 201
    except:
        return 'Bad Request',400

# unduplicate route

#like ticket route
@appc.route('/ticket/like', methods=['POST'])
@token_required
def like_ticket(current_user): 
    try:
        if(current_user.admin == 1): 
            return "Forbidden",403
        else:
            data = json.loads(request.data)
            ticket_id = data['ticket_id']
            user_id = data['user_id']
            try:
                likes = loads(db.session.query(Ticket).filter(Ticket.id==ticket_id ).first().likes)
                if user_id not in likes:
                    likes.append(user_id)
                    Ticket.query.filter_by(id=ticket_id ).update(dict(likes = dumps(likes)))
                    db.session.commit()
                    return {'sucessfully added like': 201}
                else:
                    return {'user already liked': 402}
            except:
                db.session.rollback()
                return 'error occurred while adding', 401
            
    except Exception as e:
        print(e)
        return 'Bad Request',400

# Unlike route

#replies
@appc.route('/ticket/reply', methods=['POST'])
@token_required
def reply_to_ticket(current_user): 
    try:
        if(current_user.admin == 1): 
            return "Forbidden",403
        else:
            data = json.loads(request.data)
            ticket_id = data['ticket_id']
            user_id = data['user_id']
            content = data['content']
            try:
                replies = loads(db.session.query(Ticket).filter(Ticket.id==ticket_id ).first().replies)
                replies.append((user_id, content))
                Ticket.query.filter_by(id=ticket_id ).update(dict(replies = dumps(replies)))
                db.session.commit()
            except:
                db.session.rollback()
                return 'error occurred while additin', 401
            return {'sucessfully added reply': 201}
    except Exception as e:
        print(e)
        return 'Bad Request',400


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
#remaning rud


@appc.route('/faq', methods=['POST'])
@token_required
def create_faq(current_user):
    try:
        if(current_user.admin == 0):
            return "Forbidden", 403
        
        faq_data = json.loads(request.data)
        new_faq = Faq(
            title=faq_data['title'],
            content=faq_data['content']
        )
        db.session.add(new_faq)
        db.session.commit()
        return {'success': True}
    except:
        return 'Bad Request', 400