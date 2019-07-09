from .base import BasePlugin


class CpuPlugin(BasePlugin):

    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'cpu': [['cat /proc/cpuinfo'], self.parse]
            }

        else:
            return {}

    @classmethod
    def parse(cls, content):
        ret = {'cpu_count': 0, 'cpu_physical_count': 0, 'cpu_model': ''}
        flag = False
        cpu_physical_set = set()
        for item in content.strip().split('\n\n'):
            for row in item.split('\n'):
                if not row.strip():
                    continue
                rs = row.split(':')
                if len(rs) != 2:
                    continue
                key, value = map(lambda x: x.strip(), rs)
                if key == 'processor':
                    ret['cpu_count'] += 1
                elif key == 'physical id':
                    cpu_physical_set.add(value)
                elif flag is False and key == 'model name':
                    ret['cpu_model'] = value
                    flag = True
        ret['cpu_physical_count'] = len(cpu_physical_set)
        return ret
