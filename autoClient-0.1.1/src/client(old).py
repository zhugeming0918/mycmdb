# ----------- client功能简介 ----------- #
# agent模式
# 采集资产
# 将采集的资产数据发送到API
#
# ssh模式
# 从API处获取未采集主机列表
# 根据主机列表依次采集资产数据
# 将采集的资产数据发送到API
#
# salt模式
# 从API处获取未采集主机列表
# 根据主机列表依次采集资产数据
# 将采集的资产数据发送到API


class BaseClient(object):
    def collect(self):
        pass

    def send_data(self):
        pass


class GetHostMixin(object):
    def get_host(self):
        pass


class AgentClient(BaseClient):
    def collect(self):
        pass


class SshClient(GetHostMixin, BaseClient):
    def collect(self):
        pass


class SaltClient(GetHostMixin, BaseClient):
    def collect(self):
        pass










































