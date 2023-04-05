from flask import Flask, request, make_response, jsonify

from config import config_mapping
from database import db
from models import Faq



app = Flask(__name__)
app.config.from_mapping(config_mapping)
db.init_app(app)



@app.route('/', methods=['GET'])
def home():
    return "You have found this API. Badhai ho"

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