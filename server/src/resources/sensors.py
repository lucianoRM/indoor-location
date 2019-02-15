from flask import Blueprint

'''
This file handles resources for creating, deleting, and updating information related to sensors.
'''

bp = Blueprint('sensors', __name__, url_prefix='/sensors')

@bp.route('/')
def all_sensors():
    return 'sensors'
