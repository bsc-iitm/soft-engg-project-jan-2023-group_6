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


# home page route
@appc.route('/user/tickets', methods=['GET'])
@token_required
def user_home(current_user): 
    try:
        if(current_user.admin == 1):
            _tickets = Ticket.query.filter_by(status='Open').all()
        else:
            _tickets = Ticket.query.filter_by(user_id=current_user.id).all()
        
        print(_tickets)
        ticket_list = {}
        for ticket_ in _tickets:
            ticket_list[ticket_.id]={
            'id': ticket_.id,
            'title':ticket_.title,
            'content':ticket_.content,
            'date':ticket_.date,
            'likes':ticket_.likes,
            'status': ticket_.status
            }
        return json.dumps(ticket_list, sort_keys=True, default=str)
    except:
        return 'Bad Request',400

# get all public tickets (need to add private/public flag to tickets)
@appc.route('/user/publictickets', methods=['GET'])
@token_required
def public_tickets(): 
    try:
        user_tickets = Ticket.query.filter_by.all()
        ticket_list = {}
        for ticket_ in user_tickets:
            ticket_list[ticket_.id]={
            'id': ticket_.id,
            'title':ticket_.title,
            'content':ticket_.content,
            'date':ticket_.date,
            'likes':ticket_.likes,
            'status': ticket_.status
            }
        return json.dumps(ticket_list, sort_keys=True, default=str)
    except:
        return 'Bad Request',400
    
# mark as solved
@appc.route('/ticket/mark_solved', methods=['POST'])
@token_required
def mark_solved(current_user): 
    try:
        if(current_user.admin == 1): ## also check for user id
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
@appc.route('/ticket/reopen', methods=['POST'])
@token_required
def ticket_reopen(current_user): 
    try:
        if(current_user.admin == 1 and current_user.id != json.loads(request.data)['user_id']): 
            return "Forbidden",403
        else:
            ticket_id = json.loads(request.data)['ticket_id']
            try:
                Ticket.query.filter_by(id=ticket_id ).update(dict(status = 'Open'))
                db.session.commit()
            except:
                db.session.rollback()
            return 'sucessfully marked as solved', 201
    except:
        return 'Bad Request',400

# markDuplicate
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
@appc.route('/ticket/reverse_duplicate', methods=['POST'])
@token_required
def reverse_duplicate(current_user): 
    try:
        if(current_user.admin == 0): 
            return "Forbidden",403
        else:
            data = json.loads(request.data)
            ticket_id = data['ticket_id']
            try:
                Ticket.query.filter_by(id=ticket_id ).update(dict(duplicate = None))
                db.session.commit()
            except:
                db.session.rollback()
                return 'Bad Request', 401
            return 'sucessfully marked as solved', 201
    except:
        return 'Bad Request',400
    

#like ticket route
@appc.route('/ticket/like', methods=['POST'])
@token_required
def like_ticket(current_user): 
    try:
        if(current_user.admin == 1): ## Add check for user id
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
@appc.route('/ticket/unlike', methods=['POST'])
@token_required
def unlike_ticket(current_user): 
    try:
        if(current_user.admin == 1): 
            return "Forbidden",403
        else:
            data = json.loads(request.data)
            ticket_id = data['ticket_id']
            user_id = data['user_id']
            try:
                ticket = db.session.query(Ticket).filter(Ticket.id==ticket_id ).first()
                if str(ticket.user_id) != user_id:
                    return "Forbidden",405
                else:
                    likes = loads(ticket.likes)
                    if user_id in likes:
                        likes.remove(user_id)
                        Ticket.query.filter_by(id=ticket_id ).update(dict(likes = dumps(likes)))
                        db.session.commit()
                        return {'sucessfully removed like': 201}
                    else:
                        return {'user has not liked': 402}
            except:
                db.session.rollback()
                return 'error occurred while adding', 401       
    except Exception as e:
        return 'Bad Request',400

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
    except:
        return 'Bad Request',400

#create tickets
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
        )
        print(new_ticket)
        db.session.add(new_ticket)
        db.session.commit()
        return {'success': True}
    except:
        return 'Bad Request',400

# update tickets
@appc.route('/ticket/update', methods=['PUT'])
@token_required
def update_ticket(current_user):
    try:
        if(current_user.admin == 1):
            return "Forbidden",403
        else:
            ticket_data = json.loads(request.data)
            ticket_id = ticket_data['ticket_id']
            user_id = ticket_data['user_id']
            try:
                ticket = db.session.query(Ticket).filter(Ticket.id==ticket_id ).first()
                if str(ticket.user_id) != user_id:
                    return "Forbidden",405
                else:
                    if 'title' in ticket_data:
                        ticket.title = ticket_data['title']
                    if 'content' in ticket_data:
                        ticket.content = ticket_data['content']
                    db.session.commit()
                    return {'sucessfully updated ticket': 201}
            except:
                db.session.rollback()
                return 'error ocurred while retrieving ticket', 401 
    except:
        return 'Bad Request',400
#delete tickets
@appc.route('/ticket/delete', methods=['DELETE'])
@token_required
def delete_ticket(current_user):
    try:
        if(current_user.admin == 1):
            return "Forbidden",403
        else:
            ticket_data = json.loads(request.data)
            ticket_id = ticket_data['ticket_id']
            user_id = ticket_data['user_id']
            try:
                ticket = db.session.query(Ticket).filter(Ticket.id==ticket_id ).first()
                if str(ticket.user_id) != user_id:
                    return "Forbidden",405
                else:
                    db.session.delete(ticket)
                    db.session.commit()
                    return {'sucessfully deleted ticket': 201}
            except:
                db.session.rollback()
                return 'error ocurred while retrieving ticket', 401 
    except:
        return 'Bad Request',400

@appc.route('/faq', methods=['GET'])
def all_faqs():
    faqs = Faq.query.all()
    faqs = [faq.serialized for faq in faqs]
    return {
        'faqs': faqs
    }


@appc.route('/faq/create', methods=['POST'])
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


@appc.route('/faq/update', methods=['PUT'])
@token_required
def update_faq(current_user):
    try:
        if(current_user.admin == 0):
            return "Forbidden", 403
        faq_data = json.loads(request.data)
        faq = Faq.query.filter_by(id = faq_data['id']).first()
        if faq_data['title']:
            faq.title = faq_data['title']
        if faq_data['content']:
            faq.content = faq_data['content']
        db.session.commit()
        return {'success': True}
    except:
        return 'Bad Request', 400

   
@appc.route('/faq/delete/<faq_id>', methods=['DELETE'])
@token_required
def delete_faq(current_user, faq_id):
    try:
        if(current_user.admin == 0):
            return "Forbidden", 403
        faq_to_delete = Faq.query.filter_by(id = faq_id).first()
        db.session.delete(faq_to_delete)
        db.session.commit()
        return {'success': True}
    except:
        return 'Bad Request', 400