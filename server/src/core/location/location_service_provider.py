from src.core.location.location_service import LocationService


class LocationServiceProvider:
    '''
    Class that provides LocationService implementation according to the given key
    '''

    def __init__(self, **kwargs):
        self.__location_services = {}
        for key,value in kwargs.items():
            if isinstance(value, LocationService):
                self.__location_services[key] = value

    def get_location_service(self, key=None):
        if not key:
            key = 'simple'
        location_service = self.__location_services.get(key)
        if location_service:
            return location_service
        raise UnknownLocationServiceException("Location service with key: " + key + " does not exist")


class UnknownLocationServiceException(Exception):
    '''
    Exception thrown when the location service requested does not exist
    '''
    pass