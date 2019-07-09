import re
from .base import BasePlugin


class NicPlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.regex_split = re.compile(r'\r?\n(?=\d)')
        self.regex_ifc_info = re.compile(r'^\d+:\s*([\w\-]+)(?:@)?([\w\-])?:\s*<([^]]+)>')

    @property
    def asset(self):
        if self.os_system == 'linux':
            return {
                'nic': [['sudo ip link show', 'sudo ip addr show'], self.parse]
            }
        else:
            return {}

    @classmethod
    def _cidr2ipv4_netmask(cls, cidr: int):
        """ cidr: 24  --->  子网掩码: 255.255.255.0"""
        if cidr > 32:
            raise ValueError('无类域间路由(cidr): 不能大于32')
        nm_all = 0xffffffff
        right_shift = 32 - cidr
        nm_p = nm_all << right_shift
        nm = nm_all & nm_p
        nm_bytes = nm.to_bytes(4, 'big')
        return '.'.join(map(lambda x: str(x), nm_bytes))

    @classmethod
    def _parse_network(cls, cols: list):
        """
        如果当前行是 inet 10.211.55.4/24 brd 10.211.55.255 scope global eth0
        那么cols是按空格切割后的列表
        返回值： ip, netmask, broadcast （即从字符串中解析出ip地址，子网掩码，网关返回）
        """
        lst = cols[1].split('/')
        if len(lst) == 1:
            ip = lst[0]
            cidr = 32
        else:
            ip, cidr = lst[0], int(lst[1])
        net_mask = ''
        broadcast = ''
        if cols[0] == 'inet':
            net_mask = cls._cidr2ipv4_netmask(cidr)
            if 'brd' in cols:
                broadcast = cols[cols.index('brd')+1]
        return ip, net_mask, broadcast

    def parse(self, content):
        ret = {}
        valid_keys = ['name', 'hwaddr', 'up', 'netmask', 'ipaddrs']
        interfaces = self.regex_split.split(content)       # 零宽断言，返回一个列表，列表元素是一个接口项
        for interface in interfaces:
            ifc_name = ''
            ifc = {}
            for line in interface.splitlines():
                if not line.strip():
                    continue
                matcher = self.regex_ifc_info.match(line)
                if matcher:
                    ifc_name, parent, attrs = matcher.groups()
                    if not ifc_name:
                        break
                    ifc['up'] = True if 'UP' in attrs.split(',') else False
                    if parent and parent in valid_keys:
                        ifc[parent] = parent
                    continue
                cols = line.split()
                if len(cols) >= 2:
                    type_, value = cols[0:2]
                    if type_ == 'inet':
                        ip, net_mask, broadcast = self._parse_network(cols)
                        if 'secondary' not in cols:
                            if 'inet' not in ifc:
                                ifc['inet'] = []
                            ifc['inet'].append({
                                'address': ip, 'netmask': net_mask, 'broadcast': broadcast
                            })
                        else:
                            if 'secondary' not in ifc:
                                ifc['secondary'] = []
                            ifc['secondary'].append({
                                'type': type_, 'address': ip, 'netmask': net_mask, 'broadcast': broadcast
                            })
                    elif type_.startswith('link'):
                        ifc['hwaddr'] = value
            if ifc_name:
                ret[ifc_name] = ifc
        return ret
