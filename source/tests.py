import pytest
import json
from flask import Flask, request
from config import SECRET_KEY, TEST_SQLALCHEMY_DATABASE_URI
from database import db
from models import User, Faq, Ticket
from helpers import generate_password_hash, authenticate_user, token_required

@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=TEST_SQLALCHEMY_DATABASE_URI
    )
    app.app_context().push()
    db.init_app(app)
    Ticket.query.delete()
    db.session.commit()
    return app
    


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_ticket(app):    
    tickets = Ticket.query.all()
    print(len(tickets))
    assert len(tickets)==5