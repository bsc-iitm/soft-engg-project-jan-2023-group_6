from database import db



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False, unique=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    admin = db.Column(db.Boolean(), unique=False, default=False)
    
    tickets = db.relationship("Ticket", backref="user", cascade="all, delete-orphan")
    # categories
    # comments (optional)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False, unique=False)
    content = db.Column(db.String(), nullable=False, unique=False)
    date = db.Column(db.String(), nullable=False, unique=False)
    status = db.Column(db.String(), nullable=False, unique=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False, unique=False)
    likes = db.Column(db.Integer(), nullable=False, unique=False, default=0)
    
    # comments

    @property
    def serialized(self):
        return {
            'title': self.title,
            'content': self.content,
            'date': self.date,
            'status': self.status,
            'user_id': self.user_id,
            'likes': self.likes
        }


class Faq(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)

    # categories

    @property
    def serialized(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }