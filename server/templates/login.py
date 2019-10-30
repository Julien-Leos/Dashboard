from flask import Blueprint

login_page = Blueprint('login_page', __name__, template_folder='templates')

@login_page.route('/hello')
def hello():
    return 'Hello World!'