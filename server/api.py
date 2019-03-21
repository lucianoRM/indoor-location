from flask import Flask
from flask_restful import Api

from src.resources.sensors_resources import SensorResource, SensorListResource
from src.resources.users_resources import UserListResource, UserResource

USERS_ENDPOINT = "/users"
SENSORS_ENDPOINT = "/sensors"


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(UserListResource,
                     USERS_ENDPOINT)
    api.add_resource(UserResource,
                     USERS_ENDPOINT + '/<user_id>')
    api.add_resource(SensorListResource,
                     SENSORS_ENDPOINT)
    api.add_resource(SensorResource,
                     SENSORS_ENDPOINT + '/<sensor_id>')
    return app


if __name__ == '__main__':
    create_app().run(debug=True)