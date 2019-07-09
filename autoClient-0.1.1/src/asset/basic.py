from .base import BasePlugin


class BasicPlugin(BasePlugin):

    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'basic': [['uname', 'cat /etc/system-release', 'hostname'], self.parse]
            }

        else:
            return {}

    @classmethod
    def parse(cls, content: str):
        name = ['os_platform', 'version', 'hostname']
        lst = content.splitlines()
        if lst:
            return dict(zip(name, lst))
        else:
            raise ValueError('采集不')
