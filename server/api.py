from flask import Flask
from flask_restful import Api

from src.dependency_container import DEPENDENCY_CONTAINER
from src.resources.sensors_api import SensorAPI, SensorListAPI
from src.resources.test_resource import TestResource
from src.resources.users_api import UserListAPI, UserAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(TestResource, '/test')
api.add_resource(UserListAPI,
                 '/users',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(UserAPI,
                 '/users/<user_id>',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(SensorListAPI,
                 '/sensors',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(SensorAPI,
                 '/sensors/<sensor_id>',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)

if __name__ == '__main__':
    app.run(debug=True)