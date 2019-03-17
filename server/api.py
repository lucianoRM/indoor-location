from flask import Flask
from flask_restful import Api

from src.dependency_container import DEPENDENCY_CONTAINER
from src.resources.sensors_resources import SensorResource, SensorListResource
from src.resources.users_resources import UserListResource, UserResource

USERS_ENDPOINT = "/users"
SENSORS_ENDPOINT = "/sensors"


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(UserListResource,
                     USERS_ENDPOINT,
                     resource_class_kwargs=DEPENDENCY_CONTAINER)
    api.add_resource(UserResource,
                     USERS_ENDPOINT + '/<user_id>',
                     resource_class_kwargs=DEPENDENCY_CONTAINER)
    api.add_resource(SensorListResource,
                     SENSORS_ENDPOINT,
                     resource_class_kwargs=DEPENDENCY_CONTAINER)
    api.add_resource(SensorResource,
                     SENSORS_ENDPOINT + '/<sensor_id>',
                     resource_class_kwargs=DEPENDENCY_CONTAINER)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)