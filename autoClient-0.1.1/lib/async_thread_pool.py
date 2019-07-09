from concurrent.futures import as_completed, ThreadPoolExecutor
import threading


class AsyncThreadPool(object):
    def __init__(self, max_workers=10):
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)
        self.__futures = {}
        self.__event = threading.Event()

    def _submit(self, task_dict: dict):
        """
        :param task_dict: 字典，key是任务名，value是列表，列表第一个元素是函数对象，其余是该函数的实参，如{'add': [add, 1, 2]}
        :return: 字典，key是future类实例，value是该future类实例的任务名
        """
        for name, item in task_dict.items():
            future = self.__executor.submit(*item)
            self.__futures[future] = name

    def _callback(self, callback_dict: dict=None):
        """
        :param callback_dict:
        :return:
        """
        cbk_dict = {k: v for k, v in callback_dict.items()}     # 深拷贝,确保函数中操作不会影响到原实参
        while not self.__event.is_set():
            del_future_lst = []
            new_future_dic = {}
            for future in as_completed(self.__futures):
                name = self.__futures.get(future, None)
                del_future_lst.append(future)
                if name is None:
                    continue
                try:
                    ret = future.result()
                    if cbk_dict:
                        callback = cbk_dict.get(name, None)
                        if callback:
                            del cbk_dict[name]                  # 必须先删除，避免回调函数执行完成后，查询字典再次提交回调函数后
                            future = self.__executor.submit(callback, name, ret)
                            new_future_dic[future] = name
                except Exception as e:
                    print(e)
            self.__futures.update(new_future_dic)
            for future in del_future_lst:
                del self.__futures[future]
            if not self.__futures:                              # 字典中没有任务，说明说有任务执行完成，清理资源
                self.clear()

    def execute_only(self, task_dict: dict):
        self._submit(task_dict)
        self.__executor.shutdown(wait=True)

    def execute_callback(self, task_dict: dict, callback_dict: dict=None):
        self._submit(task_dict)
        threading.Thread(target=self._callback, args=(callback_dict, )).start()

    def clear(self):
        self.__event.set()
        self.__executor.shutdown()


# if __name__ == '__main__':            # 仅供测试使用
#     import time
#     import random
#
#
#     def add(name, x, y):
#         t = random.randint(1, 8)
#         time.sleep(t)
#         print('task add finish: name: {}, sleep time: {}, param: {}, {}'.format(str(name), str(t), str(x), str(y)))
#         return x+y, t
#
#
#     def call_back(name, ret):
#         t = random.randint(1, 8)
#         time.sleep(t)
#         print('callback finish: name: {}, sleep time:{}, param {}'.format(str(name), str(t), str(ret)))
#
#
#     task_dic = {i*2+1: [add, i*2+1, i, i+1] for i in range(10)}
#     callback_dic = {i*2+1: call_back for i in range(3, 8)}
#
#     atp = AsyncThreadPool(3)
#     print('------- start --------')
#     atp.execute_callback(task_dic, callback_dic)
#     print('------- end --------')
