from .base import BasePlugin


class MainBoardPlugin(BasePlugin):
    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'mainboard': [['sudo dmidecode -t1'], self.parse]
            }

        else:
            return {}

    @classmethod
    def parse(cls, content: str):
        ret = {}
        key_map = {
            'Manufacturer': 'manufacturer', 'Product Name': 'model', 'Serial Number': 'sn'
        }
        for row in content.split('\n'):
            rs = row.strip().split(":")
            if len(rs) != 2:
                continue
            key, value = map(lambda x: x.strip(), rs)
            if key in key_map:
                ret[key_map[key]] = value
        return ret


