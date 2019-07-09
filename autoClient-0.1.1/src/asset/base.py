#!/usr/bin/env python
from lib.log import Logger
import platform


class BasePlugin(object):
    def __init__(self):
        self.logger = Logger()
        self.os_system = 'linux'            # TODO 测试用
        # self.os_system = self.check_os()

    @classmethod
    def check_os(cls):
        valid_system = {'linux', 'windows'}
        system = platform.system().lower()
        if system in valid_system:
            return system
        raise SystemError('当前系统不支持（支持linux和windows系统）')

    @property
    def asset(self):
        """
        返回值是一个字典
            key: 资产名称。
            value是一个列表：
                索引为0元素是一个列表，获取该资产信息需要执行的命令shell命令列表
                索引为1元素是函数对象，会对命令执行的结果进行处理，返回需要提取的数据。
        """
        raise NotImplementedError('请在子类中实现该方法，返回一个字典，标识如何获取该资产以及解析的方法')
