from .base import BasePlugin
import re


class DiskPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.regex_num = re.compile('\d+\.\d+')

    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'disk': [['sudo MegaCli -PDList -aALL'], self.parse]
            }

        else:
            return {}

    def parse(self, content: str):
        """
        解析shell命令返回的结果，从返回的字符串中提取有用信息
        :param content:     sudo MegaCli -PDList -aALL命令执行返回的字符串
        :return:            解析后返回的结果
        """
        ret = {}
        for item in content.split("\n\n\n\n"):
            tmp = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
                rs = row.split(":")
                if len(rs) != 2:
                    continue
                key, value = rs
                name = self.mega_pattern_match(key)
                if name:
                    if key == 'Raw Size':
                        matcher = self.regex_num.match(value.strip())
                        if matcher:
                            tmp[name] = matcher.group()
                        else:
                            tmp[name] = '0'
                    else:
                        tmp[name] = value.strip()
            if tmp:
                ret[tmp['slot']] = tmp
        return ret

    @classmethod
    def mega_pattern_match(cls, needle: str):
        dic = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in dic.items():
            if needle.startswith(key):
                return value
