import json
from json.encoder import JSONEncoder
from lib.response import BaseResponse


class JsonCustomEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseResponse):
            return o.__dict__
        return JSONEncoder.default(self, o)


class Json(object):
    @staticmethod
    def dumps(obj, ensure_ascii=True):
        return json.dumps(obj, ensure_ascii=ensure_ascii, cls=JsonCustomEncoder)
