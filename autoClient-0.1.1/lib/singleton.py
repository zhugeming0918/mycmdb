#!/usr/bin/env python
from functools import wraps


def singleton(cls):
    instance = None

    @wraps(cls)
    def _wrap(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return _wrap
