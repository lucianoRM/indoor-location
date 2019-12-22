from src.dependency_container import DependencyContainer
from src.resources.abstract_resource import AbstractResource
from src.resources.schemas.log_schema import LogSchema


class LogResource(AbstractResource):

    def __init__(self, custom_error_mappings=None, **kwargs):
        super().__init__(custom_error_mappings, **kwargs)
        self.__log_schema = LogSchema(strict=True)
        self.__logger = DependencyContainer.logger()

    def _do_post(self, **kwargs):
        log_data = self.__log_schema.load(self._get_post_data_as_json()).data

        self.__logger.info('%s - ' + log_data['message'], log_data['tag'])
        return "You should not be using this, it's experimental!"


