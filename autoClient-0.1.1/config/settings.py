#!/usr/bin/env python
import os

# 项目根目录
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 错误日志及运行日志
ERROR_LOG_PATH = os.path.join(BASEDIR, 'log', 'error.log')
RUN_LOG_PATH = os.path.join(BASEDIR, 'log', 'run.log')

# test_mode 仅供测试使用，表示资产数据冲files目录下的文件读取
TEST_MODE = True

# client运行的模式，允许的模式为 agent, ssh, salt
MODE = 'salt'

# salt模式下参数：salt-api
SALT_API_URL = 'https://192.168.11.126:8001'
SALT_API_PAM_USER = 'saltapi'
SALT_API_PAM_PASSWORD = 'salt20192019'

# ssh模式下参数：(使用root用户，将root用户的私钥拷贝到如下位置，修改权限，因为python用户无权限执行某些命令)
SSH_USER = 'root'
SSH_PRIVATE_KEY = '/home/python/.root_private_key/id_rsa'
SSH_PORT = '22'

# 资产采集项
PLUGINS = [
    'src.asset.mainboard.MainBoardPlugin',
    'src.asset.cpu.CpuPlugin',
    'src.asset.memory.MemoryPlugin',
    'src.asset.disk.DiskPlugin',
    'src.asset.nic.NicPlugin'
]


# 采集资产发送到哪个api上
ASSET_API = 'http://127.0.0.1:8000/api/asset'
# 用于API认证的KEY
KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
# 用于API认证KEY的请求头
AUTH_KEY_NAME = 'auth-key'

















