from flask import Flask
from flask_restful import Api

from src.dependency_container import DependencyContainer
from src.resources.anchors_resources import AnchorListResource, AnchorResource
from src.resources.sensors_resources import SensorResource, SensorListResource
from src.resources.signal_emitters_resources import SignalEmitterResource, SignalEmitterListResource
from src.resources.users_resources import UserListResource, UserResource

USERS_ENDPOINT = "/users"
SENSORS_ENDPOINT = "/sensors"
ANCHORS_ENDPOINT = "/anchors"
SIGNAL_EMITTERS_ENDPOINT = "/signal_emitters"


def create_app():
    app = Flask(__name__)
    api = Api(app)

    #This is needed so thatt all providers are created before the application is started because resource classes are created lazily.
    DependencyContainer.init()

    api.add_resource(UserListResource,
                     USERS_ENDPOINT)
    api.add_resource(UserResource,
                     USERS_ENDPOINT + '/<user_id>')

    api.add_resource(SensorListResource,
                     SENSORS_ENDPOINT)
    api.add_resource(SensorResource,
                     SENSORS_ENDPOINT + '/<sensor_id>')

    api.add_resource(AnchorListResource,
                     ANCHORS_ENDPOINT)
    api.add_resource(AnchorResource,
                     ANCHORS_ENDPOINT + '/<anchor_id>')

    api.add_resource(SignalEmitterListResource,
                     SIGNAL_EMITTERS_ENDPOINT)
    api.add_resource(SignalEmitterResource,
                     SIGNAL_EMITTERS_ENDPOINT + '/<signal_emitter_id>')
    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", port=8082, debug=True)