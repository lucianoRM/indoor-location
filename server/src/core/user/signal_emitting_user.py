from src.core.emitter.signal_emitter import SignalEmitter
from src.core.user.user import User


class SignalEmittingUser(User, SignalEmitter):
    """
    An user that is also a signal emitter
    """

    def __init__(self, id: str, position: str, **kwargs):
        super().__init__(id=id, position=position, **kwargs)
