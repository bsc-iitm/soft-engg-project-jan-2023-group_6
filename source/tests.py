import pytest
import json
from flask import Flask, request
from config import SECRET_KEY, TEST_SQLALCHEMY_DATABASE_URI
from database import db
from models import User, Faq, Ticket
from helpers import generate_password_hash, authenticate_user, token_required
from routes import appc

@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=TEST_SQLALCHEMY_DATABASE_URI
    )
    app.register_blueprint(appc)
    app.app_context().push()
    db.init_app(app)
    Ticket.query.delete()
    db.session.commit()
    return app
    


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_ticket_without_auth(client):    
    response = client.post('/ticket', json={
        "date": "123123123", 
        "title": "test test1", 
        "content": "test_create_ticket_without_auth"
    })
    tickets = Ticket.query.all()
    assert response.status_code == 401
    assert b"Unauthorized request" in response.data
    assert(len(tickets)) == 0

def test_create_ticket_admin(client):
    access_token = authenticate_user({"username": "admin", "password": "admin123"})["access_token"]
    response = client.post('/ticket', json={
        "date": "123123123", 
        "title": "test test1", 
        "content": "test_create_ticket_without_auth"
    }, headers={
        "authorization": "bearer "+access_token
    })

    tickets = Ticket.query.all()
    assert response.status_code == 403
    assert b"Forbidden" in response.data
    assert(len(tickets)) == 0


    
