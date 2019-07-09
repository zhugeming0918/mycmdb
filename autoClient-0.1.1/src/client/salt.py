from .base import BaseMiddleClient
from lib.salt_api import SaltAPI


class SaltClient(BaseMiddleClient):

    @classmethod
    def exec_shell_cmd(cls, cmd, hostname=''):
        """ 要使用salt模式，将当前代码部署在master主机上，程序会向salt-api发送请求，有salt-master向minion发送命令 """
        # 使用subprocess方式在本地执行salt命令
        # import subprocess
        # ret = subprocess.getoutput("salt '*' cmd.run {}".format(cmd))
        # print(ret)
        sa = SaltAPI()
        result = sa.remote_execution(tgt=hostname, fun='cmd.run', arg=cmd)
        return result[hostname]
