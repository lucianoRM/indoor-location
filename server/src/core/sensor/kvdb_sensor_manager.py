from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBacked
from src.core.sensor.sensor_manager import SensorManager, SensorAlreadyExistsException, UnknownSensorException


class KVDBSensor(SensorManager, KVDBBacked):
    """Sensor manager that stores information in a key-value database"""

    __SENSORS_POSITION_KEY = "sensors"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about sensors
        """
        super(KVDBSensor, self).__init__(kv_database)

    def add_sensor(self, sensor_id, sensor):
        try:
            return self._database.insert(
                self._build_complex_key(self.__SENSORS_POSITION_KEY, sensor_id),
                sensor
            )
        except KeyAlreadyExistsException:
            raise SensorAlreadyExistsException("Sensor with id: " + sensor_id + " was already registered")

    def get_sensor(self, sensor_id):
        try:
            return self._database.retrieve(
                self._build_complex_key(self.__SENSORS_POSITION_KEY, sensor_id)
            )
        except KeyDoesNotExistException:
            raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def update_sensor(self, sensor_id, sensor):
        try:
            return self._database.update(
                self._build_complex_key(self.__SENSORS_POSITION_KEY, sensor_id),
                sensor
            )
        except KeyDoesNotExistException:
            raise UnknownSensorException("A sensor with id: " + sensor_id + " does not exist")

    def remove_sensor(self, sensor_id):
        try:
            return self._database.remove(
                self._build_complex_key(self.__SENSORS_POSITION_KEY, sensor_id)
            )
        except KeyDoesNotExistException:
            raise UnknownSensorException("Attempting to remove a sensor that does not exist. With ID: " + sensor_id)

    def get_all_sensors(self):
        try:
            return self._database.retrieve(self.__SENSORS_POSITION_KEY).values()
        except KeyDoesNotExistException:
            return []
