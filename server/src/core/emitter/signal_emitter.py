from abc import ABCMeta, abstractmethod


class SignalEmitter:
    """
    Abstract class that models an object that emits a signal
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        signal = kwargs.pop("signal", None)
        if not signal:
            signal = {}
        self.__signal = signal
        super().__init__(**kwargs)

    @property
    def signal(self):
        return self.__signal