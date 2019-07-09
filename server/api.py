from flask import Flask
from flask_restful import Api

from src.dependency_container import DependencyContainer
from src.resources.anchors_resources import AnchorListResource, AnchorResource, SensingAnchorSensorListResource, \
    SensingAnchorSensorResource, SignalEmittingAnchorSEListResource, SignalEmittingAnchorSEResource
from src.resources.sensors_resources import SensorResource, SensorListResource
from src.resources.signal_emitters_resources import SignalEmitterResource, SignalEmitterListResource
from src.resources.users_resources import UserListResource, UserResource, SensingUserSensorListResource, \
    SensingUserSensorResource, SignalEmittingUserSEListResource, SignalEmittingUserSEResource

USERS_ENDPOINT = "/users"
SENSORS_ENDPOINT = "/sensors"
ANCHORS_ENDPOINT = "/anchors"
SIGNAL_EMITTERS_ENDPOINT = "/signal_emitters"

USER_ID_PLACEHOLDER = '/<user_id>'
SENSOR_ID_PLACEHOLDER = '/<sensor_id>'
ANCHOR_ID_PLACEHOLDER = '/<anchor_id>'
SIGNAL_EMITTER_ID_PLACEHOLDER = '/<signal_emitter_id>'
OWNER_ID_PLACEHOLDER = '/<owner_id>'

def create_app():
    app = Flask(__name__)
    api = Api(app)

    #This is needed so that all providers are created before the application is started because resource classes are created lazily.
    DependencyContainer.init()

    api.add_resource(UserListResource,
                     USERS_ENDPOINT)
    api.add_resource(UserResource,
                     USERS_ENDPOINT + USER_ID_PLACEHOLDER)
    api.add_resource(SensingUserSensorListResource,
                     USERS_ENDPOINT + OWNER_ID_PLACEHOLDER + SENSORS_ENDPOINT)
    api.add_resource(SensingUserSensorResource,
                     USERS_ENDPOINT + OWNER_ID_PLACEHOLDER + SENSORS_ENDPOINT + SENSOR_ID_PLACEHOLDER)
    api.add_resource(SignalEmittingUserSEListResource,
                     USERS_ENDPOINT + OWNER_ID_PLACEHOLDER + SIGNAL_EMITTERS_ENDPOINT)
    api.add_resource(SignalEmittingUserSEResource,
                     USERS_ENDPOINT + OWNER_ID_PLACEHOLDER + SIGNAL_EMITTERS_ENDPOINT + SIGNAL_EMITTER_ID_PLACEHOLDER)

    api.add_resource(SensorListResource,
                     SENSORS_ENDPOINT)
    api.add_resource(SensorResource,
                     SENSORS_ENDPOINT + SENSOR_ID_PLACEHOLDER)

    api.add_resource(AnchorListResource,
                     ANCHORS_ENDPOINT)
    api.add_resource(AnchorResource,
                     ANCHORS_ENDPOINT + ANCHOR_ID_PLACEHOLDER)
    api.add_resource(SensingAnchorSensorListResource,
                     ANCHORS_ENDPOINT + OWNER_ID_PLACEHOLDER + SENSORS_ENDPOINT)
    api.add_resource(SensingAnchorSensorResource,
                     ANCHORS_ENDPOINT + OWNER_ID_PLACEHOLDER + SENSORS_ENDPOINT + SENSOR_ID_PLACEHOLDER)
    api.add_resource(SignalEmittingAnchorSEListResource,
                     ANCHORS_ENDPOINT + OWNER_ID_PLACEHOLDER + SIGNAL_EMITTERS_ENDPOINT)
    api.add_resource(SignalEmittingAnchorSEResource,
                     ANCHORS_ENDPOINT + OWNER_ID_PLACEHOLDER + SIGNAL_EMITTERS_ENDPOINT + SIGNAL_EMITTER_ID_PLACEHOLDER)

    api.add_resource(SignalEmitterListResource,
                     SIGNAL_EMITTERS_ENDPOINT)
    api.add_resource(SignalEmitterResource,
                     SIGNAL_EMITTERS_ENDPOINT + SIGNAL_EMITTER_ID_PLACEHOLDER)
    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", port=8082, debug=True)