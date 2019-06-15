from typing import Dict

from src.core.anchor.anchor import Anchor
from src.core.emitter.signal_emitter import SignalEmitter


class SignalEmittingAnchor(Anchor, SignalEmitter):
    """
    An anchor that is also a signal emitter
    """

    def __init__(self, id: str, position: str, **kwargs):
        super().__init__(id=id, position=position, **kwargs)