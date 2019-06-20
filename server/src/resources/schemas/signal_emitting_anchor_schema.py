from marshmallow import post_load

from src.core.anchor.signal_emitting_anchor import SignalEmittingAnchor
from src.resources.schemas.anchor_schema import AnchorSchema
from src.resources.schemas.signal_emitter_schema import SignalEmitterSchema


class SignalEmittingAnchorSchema(SignalEmitterSchema, AnchorSchema):

    @post_load
    def make_object(self, kwargs):
        return SignalEmittingAnchor(**kwargs)