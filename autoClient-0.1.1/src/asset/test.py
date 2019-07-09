# ------------------------- 测试BasicPlugin插件 ------------------------- #
# from src.asset.basic import BasicPlugin
# obj = BasicPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# for k, v in data.data.items():
#     print('{}: {}'.format(k, v))


# # ------------------------- 测试DiskPlugin插件 ------------------------- #
# from src.asset.disk import DiskPlugin
# obj = DiskPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# for k, v in data.data.items():
#     print("{}: {}".format(k, v))


# # ------------------------- 测试CpuPlugin插件 ------------------------- #
# from src.asset.cpu import CpuPlugin
# obj = CpuPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# print(data.data)


# # ------------------------- 测试MemoryPlugin插件 ------------------------- #
# from src.asset.memory import MemoryPlugin
# obj = MemoryPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# for k, v in data.data.items():
#     print('{}:{}'.format(k, v))


# # ------------------------- 测试MainBoardPlugin插件 ------------------------- #
# from src.asset.main_board import MainBoardPlugin
# obj = MainBoardPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# print(data.data)
# for k, v in data.data.items():
#     print('{}:{}'.format(k, v))


# # ------------------------- 测试MemoryPlugin插件 ------------------------- #
# from src.asset.nic import NicPlugin
# obj = NicPlugin('192.168.11.211')
# data = obj.execute()
# print(data.status, data.message, data.error)
# for k, v in data.data.items():
#     print('{}:{}'.format(k, v))


# import re
# with open('files/nic.out', 'r') as f:
#     ret = f.read()
# print(ret.encode())
# groups = re.compile('\r?\n(?=\d)').split(ret)
# print(len(groups))
# for item in groups:
#     print(item)
#
# regex = re.compile(r'^\d+:\s*([\w\-]+)(?:@)?([\w\-])?:\s*<([^]]+)>')
# s = "1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN"
# matcher = regex.match(s)
# print(matcher.group())
# print(matcher.groups())
#
# cols = 'link/ether 52:54:00:a3:74:29 brd ff:ff:ff:ff:ff:ff'.split()
# print(cols[-1:])
#
#
# def _cidr2ipv4_netmask(cidr: int):
#     """ cidr: 24  --->  子网掩码: 255.255.255.0"""
#     nm_all = 0xffffffff
#     right_shift = 32 - cidr
#     nm_p = nm_all << right_shift
#     nm = nm_all & nm_p
#     nm_bytes = nm.to_bytes(4, 'big')
#     print(hex(nm_all))
#     print(hex(nm_p))
#     print(hex(nm))
#     print(nm_bytes)
#     print('.'.join(map(lambda x: str(x), nm_bytes)))
#
#
# _cidr2ipv4_netmask(27)


from src.asset import pack
ret = pack('192.168.11.211')
for k, v in ret.items():
    print(k, v)
    print()
