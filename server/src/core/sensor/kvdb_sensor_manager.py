from src.core.database.kv_database import KeyAlreadyExistsException, KeyDoesNotExistException
from src.core.manager.kvdb_backed_manager import KVDBBackedManager
from src.core.sensor.sensor_manager import SensorManager, SensorAlreadyExistsException, UnknownSensorException


class KVDBSensorManager(SensorManager, KVDBBackedManager):
    """Sensor manager that stores information in a key-value database"""

    __SENSORS_LOCATION_KEY = "sensors"

    def __init__(self, kv_database):
        """
        Constructor for Manager.
        :param kv_database: key-value database to store information about sensors
        """
        super(KVDBSensorManager, self).__init__(kv_database)

    def add_sensor(self, sensor):
        try:
            return self._database.insert(
                self._build_complex_key(self.__SENSORS_LOCATION_KEY, sensor.id),
                sensor
            )
        except KeyAlreadyExistsException:
            raise SensorAlreadyExistsException("Sensor with id: " + sensor.id + " was already registered")

    def get_sensor(self, sensorId):
        try:
            return self._database.retrieve(
                self._build_complex_key(self.__SENSORS_LOCATION_KEY, sensorId)
            )
        except KeyDoesNotExistException:
            raise UnknownSensorException("A sensor with id: " + sensorId + " does not exist")

    def remove_sensor(self, sensorId):
        try:
            return self._database.remove(
                self._build_complex_key(self.__SENSORS_LOCATION_KEY, sensorId)
            )
        except KeyDoesNotExistException:
            raise UnknownSensorException("Attempting to remove a sensor that does not exist. With ID: " + sensorId)

    def get_all_sensors(self):
        try:
            return self._database.retrieve(self.__SENSORS_LOCATION_KEY).values()
        except KeyDoesNotExistException:
            return []
