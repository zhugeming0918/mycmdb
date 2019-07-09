#!/usr/bin/env python
import json


class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None

    def __repr__(self):
        return json.dumps(self.__dict__).__repr__()
