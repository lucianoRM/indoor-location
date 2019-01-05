from flask import Blueprint

'''
This file handles endpoints for creating, deleting, and updating information related to users.
'''

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def all_users():
    return 'users'
