from measurement.measures import Distance
"""
Normalizes unit related values received into unit-less information used in the system.
"""

DEFAULT_LENGTH_UNIT = 'm'

def normalize_length(value, unit):
    used_unit = unit if unit else DEFAULT_LENGTH_UNIT
    return Distance(**{used_unit:value}).m

