from src.core.object.moving_object import MovingObject

class SignalEmitter(MovingObject):
    """
    Class that models an object that emits a signal
    """

    def __init__(self,**kwargs):
        signal = kwargs.pop("signal", None)
        if not signal:
            signal = {}
        self.__signal = signal
        super().__init__(**kwargs)

    @property
    def signal(self):
        return self.__signal