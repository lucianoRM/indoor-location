from abc import ABCMeta, abstractmethod


class SignalEmitter:
    """
    Abstract class that models an object that emits a signal
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, **kwargs):
        super().__init__(**kwargs)