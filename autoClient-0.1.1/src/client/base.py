from lib.async_thread_pool import AsyncThreadPool
from lib.log import Logger
from lib.response import BaseResponse
from lib.cunstomJson import Json
from config import settings
from src import asset
import traceback
import requests
import hashlib
import time
import json


class BaseClient(object):

    def __new__(cls, *args, **kwargs):
        if cls is not __class__:
            return super().__new__(cls)
        else:
            raise TypeError('基类不允许实例化')     # 因为基类中exec_shell_cmd未实现

    def __init__(self):
        self.logger = Logger()
        self.test_mode = getattr(settings, 'TEST_MODE', False)
        self.asset_api = settings.ASSET_API
        self.key = settings.KEY
        self.key_header_name = settings.AUTH_KEY_NAME
        self.key_header = self.auth_key()

    @classmethod
    def exec_shell_cmd(cls, cmd, hostname):
        raise NotImplementedError('请在子类中实现exec_shell_cmd方法：用于在待采集资产机器上执行该命令，返回结果')

    def process(self):
        raise NotImplementedError('请在子类中实现process方法：用于采集资产，并发送给API')

    def auth_key(self):
        """ 接口认证 """
        ha = hashlib.md5(self.key.encode('utf-8'))
        time_span = time.time()
        ha.update(bytes("{}|{}".format(self.key, time_span), encoding='utf-8'))
        encryption = ha.hexdigest()
        result = "{}|{}".format(encryption, time_span)
        return {self.key_header_name: result}

    def get_asset(self, hostname):
        response = BaseResponse()

        ret = {}
        entries = asset.get_asset_entries()
        for asset_name, method in entries.items():
            asset_resp = BaseResponse()
            cmds, parse_method = method
            lst = []
            try:
                for cmd in cmds:
                    lst.append(self.exec_shell_cmd(cmd, hostname))
                asset_resp.data = parse_method('\n'.join(lst))
            except Exception:
                print('------------------', asset_name)
                msg = '{} {} plugin error: {}'.format(hostname, asset_name, traceback.format_exc())
                self.logger.error(msg)
                asset_resp.status = False
                asset_resp.error = msg
            ret[asset_name] = asset_resp

        response.data = ret
        return response

    def post_asset(self, name, data, callback=None):    # TODO 发送数据前，数据中有response类实例需先处理
        """ 向API提交数据 """
        print('-------------------:', name, type(Json.dumps(data)), Json.dumps(data))
        try:
            response = requests.post(
                url=self.asset_api,
                headers=self.key_header,
                json=Json.dumps(data),
            )
            status = True
        except Exception as e:
            print(e)
            response = e
            status = False
        if callback:
            callback(status, response)

    def callback(self, status, response):
        """
            提交资产后的回调函数
        :param status:      请求是否成功
        :param response:    请求成功，返回的是响应报文； 请求失败，则是异常对象
        :return:
        """
        if not status:
            self.logger.error(str(response))
            return
        ret = json.loads(response.text)
        if ret['code'] == 1000:
            self.logger.info(ret['message'])
        else:
            self.logger.error(ret['message'])


class BaseMiddleClient(BaseClient):
    def __new__(cls, *args, **kwargs):
        if cls is not __class__:
            return super().__new__(cls)
        else:
            raise TypeError('基类不允许实例化')

    @classmethod
    def exec_shell_cmd(cls, cmd, hostname):
        raise NotImplementedError('you must implement "exec_shell_cmd(self, cmd)" method in sub class')

    def get_host(self):
        """
        使用requests.get()方式从api获取需要采集资产的主机列表
        :return: {'data': [{'hostname': '192.168.11.211'}], 'status': True, 'error': None, 'message': None}
        """
        try:
            # response = requests.get(
            #     url=self.asset_api,
            #     headers=self.key_header,
            # )
            # return response.json()
            return {'data': [{'hostname': '192.168.11.211'}], 'status': True, 'error': None, 'message': None}  # TODO测试
        except Exception as e:
            self.logger.error(str(e))

    def process(self, max_workers=6):
        """
        task = {'data': [{'hostname': 'c.com'}, {'hostname': 'c2.com'}], 'error': null, 'message': null, 'status': true}
        1. 获取需要采集资产的主机列表
        2. 根据列表依次采集资产数据
        3. 发送给API
        :max_workers: 启动多少个线程池来采集minion主机资产信息
        :return:
        """
        task = self.get_host()
        if task is None:
            return
        if not task['status']:
            self.logger.error(task['message'])
            return
        task_dic = {item['hostname']: [self.get_asset, item['hostname']] for item in task['data']}
        callback_dic = {item['hostname']: self.post_asset for item in task['data']}
        AsyncThreadPool(max_workers).execute_callback(task_dic, callback_dic)
