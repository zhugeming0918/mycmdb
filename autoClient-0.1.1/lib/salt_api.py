import requests
from config import settings


class SaltAPI(object):
    def __init__(self):
        self.__user = settings.SALT_API_PAM_USER
        self.__pwd = settings.SALT_API_PAM_PASSWORD
        self.url = settings.SALT_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.__base_data = {
            'username': self.__user,
            'password': self.__pwd,
            'eauth': 'pam'
        }
        self.__token = self.get_token()

    def get_token(self):
        """ login salt-api and get token_id """
        params = self.__base_data
        requests.packages.urllib3.disable_warnings()  # close ssl warning,
        response = requests.post(
            url="{}{}".format(self.url, '/login'),
            json=params,
            verify=False,
            headers=self.headers,
        )
        # print('response:', response)                # TODO 测试用
        response_json = response.json()
        # print('response_json:', response_json)      # TODO 测试用
        token = response_json["return"][0]["token"]
        return token

    def __post(self, **kwargs):
        """ custom post interface, headers contains X-Auth-Token """
        headers_token = {'X-Auth-Token': self.__token}
        headers_token.update(self.headers)
        requests.packages.urllib3.disable_warnings()  # close ssl warning,
        response = requests.post(
            url=self.url,
            verify=False,
            headers=headers_token,
            **kwargs
        )
        # print('response:', response)                # TODO 测试用
        response_code, response_data = response.status_code, response.json()
        # print('response_code:', response_code)      # TODO 测试用
        # print('response_data:', response_data)      # TODO 测试用
        return response_code, response_data

    def list_all_keys(self):
        """ show all keys, minions have been certified, minions_pre not certification """
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        res_code, res_data = self.__post(json=params)
        minions = res_data['return'][0]['data']['return']['minions']
        minions_pre = res_data['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def delete_key(self, tgt):
        """ delete a key (删除一个minion) """
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': tgt}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]['data']['success']

    def accept_key(self, tgt):
        """ accept a key (接受一个minion) """
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': tgt}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]['data']['success']

    def lookup_jid_ret(self, jid):
        """ depend on job_id to find result """
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        res_code, res_data = self.__pwd(json=params)
        return res_data['return'][0]

    def list_running_jobs(self):
        """ show all running jobs """
        params = {'client': 'runner', 'fun': 'jobs.active'}
        res_code, res_data = self.__pwd(json=params)
        return res_data['return'][0]

    def run(self, params):
        """ remote common interface, you need to custom data dict
            for example
            params = {
                'client': 'local',
                'fun': 'grains.item',
                'tgt': '*',
                'arg': ('os', 'id', 'host'),
                'kwargs': {},
                'expr_form': 'glob',
                'timeout': 60
            }
        """
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]

    def remote_execution(self, tgt, fun, arg, expr_form='glob'):
        """ remote execution, command will wait result
            arg: must be a tuple, such as : arg=(a, b)
            expr_form: tgt m
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]

    def async_remote_execution(self, tgt, fun, arg, expr_form='glob'):
        """ async remote execution, it will return a job id
            tgt: a string like 'minion1, minion2, minion3',  多个minion使用逗号分隔
        """
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]['jid']

    def salt_state(self, tgt, arg, expr_form='list'):
        """ salt state.sls """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]

    def salt_alive(self, tgt, expr_form='glob'):
        """ salt test.ping """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping', 'expr_form': expr_form}
        res_code, res_data = self.__post(json=params)
        return res_data['return'][0]


if __name__ == '__main__':
    obj = SaltAPI()
    # obj.list_all_keys()
    # print(obj.remote_execution('*', 'cmd.run', 'uname -a'))























