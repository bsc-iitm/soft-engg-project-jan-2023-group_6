from database import db



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