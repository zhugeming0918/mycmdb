from .base import BaseMiddleClient
from config import settings
import paramiko


class SshClient(BaseMiddleClient):

    @classmethod
    def exec_shell_cmd(cls, cmd, hostname):
        """ 要使用ssh模式，将当前代码部署在master主机上，程序会自动ssh连接minion """
        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result
