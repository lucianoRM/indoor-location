from flask import Flask
from flask_restful import Api

from src.dependency_container import DEPENDENCY_CONTAINER
from src.resources.sensors_resources import SensorResource, SensorListResource
from src.resources.test_resource import TestResource
from src.resources.users_resources import UserListResource, UserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(TestResource, '/test')
api.add_resource(UserListResource,
                 '/users',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(UserResource,
                 '/users/<user_id>',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(SensorListResource,
                 '/sensors',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)
api.add_resource(SensorResource,
                 '/sensors/<sensor_id>',
                 resource_class_kwargs=DEPENDENCY_CONTAINER)

if __name__ == '__main__':
    app.run(debug=True)