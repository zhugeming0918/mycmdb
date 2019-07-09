from .base import BaseClient


class AgentClient(BaseClient):
    @classmethod
    def exec_shell_cmd(cls, cmd, hostname):
        """ 要使用agent模式，需将当前代码部署在minion主机上执行 """
        import subprocess
        ret = subprocess.getoutput(cmd)
        return ret

    def process(self):
        """ agent模式仅采集自身主机的资产信息，所以不需要hostname参数 """
        data = self.get_asset(None)
        self.post_asset(None, data)
