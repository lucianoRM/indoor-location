import requests

from api import ANCHORS_ENDPOINT, USERS_ENDPOINT
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.user_schema import UserSchema


class Client:
    '''
    Talks with the server and gets updated values
    '''
    
    def __init__(self):
        self.__anchors = []
        self.__users = []
        self.__users_serializer = UserSchema(many=True, strict=True)
        self.__anchors_serializer = AnchorSchema(many=True, strict=True)

    def update(self):
        self.__anchors = self.__get_anchors()
        self.__users = self.__get_users()

    def get_anchors(self):
        return self.__anchors

    def get_users(self):
        return self.__users

    def __build_url(self, endpoint):
        return "http://localhost:8082" + endpoint

    def __get_anchors(self):
        return self.__anchors_serializer.load(requests.get(self.__build_url(ANCHORS_ENDPOINT)).json()).data

    def __get_users(self):
        return self.__users_serializer.load(requests.get(self.__build_url(USERS_ENDPOINT)).json()).data