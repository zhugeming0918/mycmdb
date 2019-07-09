from .base import BasePlugin
from lib import convert


class MemoryPlugin(BasePlugin):

    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'memory': [['sudo dmidecode -q -t 17 2>/dev/null'], self.parse]
            }

        else:
            return {}

    @classmethod
    def parse(cls, content: str):
        key_map = {
            'Size': 'capacity', 'Locator': 'slot', 'Type': 'model',
            'Speed': 'speed', 'Manufacturer': 'manufacturer', 'Serial Number': 'sn'
        }
        ret = {}
        for item in content.split("\n\n"):
            if not item.strip() or item.startswith('#'):
                continue
            segment = {}
            for row in item.split("\n\t"):
                rs = row.split(":")
                if len(rs) != 2:
                    continue
                key, value = map(lambda x: x.strip(), rs)
                if key in key_map:
                    if key == 'Size':
                        segment['size'] = convert.convert_mb2gb(value, 0)
                    else:
                        segment[key_map[key]] = value
            ret[segment['slot']] = segment
        return ret
