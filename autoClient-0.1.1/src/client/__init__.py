from config import settings
from .base import BaseClient
from lib.response import BaseResponse
from lib.log import Logger
from src import asset
import importlib
import os


class AutoClient:
    MODE = {
        'agent': 'src.client.agent.AgentClient',
        'salt': 'src.client.salt.SaltClient',
        'ssh': 'src.client.ssh.SshClient'
    }

    def __init__(self):
        self.mode, self.client = self.check_mode()
        self.logger = Logger()
        self.test_mode = getattr(settings, 'TEST_MODE', False)

    def check_mode(self):
        mode = getattr(settings, 'MODE', 'agent')       # 没有设置默认采用agent模式
        if mode not in self.MODE:
            raise SystemError("模式设置错误，仅支持： agent, salt, ssh模式")
        model_path, cls_name = self.MODE[mode].rsplit('.', maxsplit=1)
        cls = getattr(importlib.import_module(model_path), cls_name)
        if not issubclass(cls, BaseClient):
            raise SystemError("客户端类异常: {}应当继承自BaseClient类".format(cls.__name__))
        client = cls()
        return mode, client

    @classmethod
    def test(cls):
        """ 仅供测试使用： 读取files目录下文件的内容（该内容等效于在minion主机上执行命令返回的结果）， 测试parse函数是否正确 """
        fp = {
            'basic': 'basic.out',
            'mainboard': 'mainboard.out',
            'cpu': 'cpu.out',
            'memory': 'memory.out',
            'disk': 'disk.out',
            'nic': 'nic.out'
        }
        response = BaseResponse()
        ret = {}
        entries = asset.get_asset_entries()
        for asset_name, method in entries.items():
            if asset_name in fp:
                asset_resp = BaseResponse()
                cmds, parse_method = method
                with open(os.path.join(settings.BASEDIR, 'files', fp[asset_name]), 'r') as f:
                    content = f.read()
                asset_resp.data = parse_method(content)
                ret[asset_name] = asset_resp
        response.data = ret
        return response

    def get_asset(self, hostname):
        if self.test_mode:
            return self.test()
        else:
            return self.client.get_asset(hostname)

    def run(self):
        self.client.process()
