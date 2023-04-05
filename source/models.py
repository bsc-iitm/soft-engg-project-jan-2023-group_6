from database import db



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False, unique=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, unique=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    admin = db.Column(db.Boolean(), unique=False, default=False)


class Faq(db.Model):
    __tablename__ = 'faq'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)

    @property
    def serialized(self):
        return {
            'title': self.title,
            'content': self.content
        }