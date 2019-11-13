# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/4/10 13:27
# describtion:
"""
    mongo连接管理器包
    QPLUS_ENV:
            'development': 'development.conf',
            'test_env': 'testing.conf',
            'production': 'production.conf'
"""
from pymongo import MongoClient
from quotations.conf import config
from  quotations.constants import QPLUS_ENV


class MongoManager:
    """
        根据传入参数实例避免倒入时全部实例浪费资源
        # , waitqueuetimeoutms=3, maxpoolsize默认100
        MongoClient(config('mongo').get(uri=True), maxpoolsize=100)['pol']
    :param :
        pol  # 都有
        daily  # 生产环境
        ceshi_hq  # 同上，测试环境使用的，只是名字不一样
        test  # 测试环境
    # 【使用方法】
    # 方法一：上下文管理器调用   退出管理器时能主动释放连接池
    # 注意：如果在同一个进程系统中需要多处使用连接池，则不太推荐使用上下文管理器
    >>> with MongoManager() as man:
    ...     print(man.pol.strategy_factor.find_one({}))
    True
    # 方法二：直接调用实例对象
    >>> print(mongoManager.pol.strategy_factor.find_one({}))
    >>> print(mongoManager.hqdb_test.hq_D_INDEX_000001.SH.find_one({}))  # 该连接对象没有的库强行接上不报错，只是查询为空
    >>> data = [{'aaaa': 2}]
    >>> print(mongoManager.hqdb_test.hq_D_INDEX_000001.SH.insert(data))  # 添加
    >>> mongoManager.client  # 直接获取client

    # 备注
        如果有需要连接的库不在实例属性中，则需获取client对接
        比如：mongoManager.client['db_name']
    """
    client = MongoClient(config('mongo').get(uri=True), maxpoolsize=150)  # 默认100  waitqueuetimeoutms=3

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MongoManager, cls).__new__(cls)
        return cls._instance

    @property
    def pol(self):  # 都有
        print(self.client.max_pool_size)
        return self.client['pol']  # , waitqueuetimeoutms=3, maxpoolsize默认100

    @property
    def ceshi_hq(self):  # 同上，测试环境使用的，只是名字不一样
        return self.client['ceshi_hq']

    @property
    def hqdb_test(self):  # 生产环境  daily  ;  测试环境 test
        return {
            'development': self.client['test'],
            'test_env': self.client['test'],
            'production': self.client['daily']
        }.get(QPLUS_ENV)

    # @property
    # def test(self):  # 测试环境
    #     return self.__client['test']

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()  # 退出时释放连接池

    def __enter__(self):
        """
            上下文管理器中进入，则返回该对象
            :return:
        """
        return self


# 【管理器入口实例】在此包中直接实例化一个，以便调用
mongoManager = MongoManager()








if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)



### 【使用介绍】

# 方法一：上下文管理器调用   退出管理器时能主动释放连接池
# 注意：如果在同一个进程系统中需要多处使用连接池，则不太推荐使用上下文管理器
# with MongoManager() as man:
#     print(man.pol.strategy_factor.find_one({}))


# 方法二：直接调用实例对象
# # 【test】
# print(mongoManager.pol.strategy_factor.find_one({}))
# print(mongoManager.test.hq_D_INDEX_000001.SH.find_one({}))  # 该连接对象没有的库强行接上不报错，只是查询为空
# data = [{'aaa': 1}]
# print(mongoManager.test.hq_D_INDEX_000001.SH.insert(data))  # 添加
# print(id(mongoManager.pol))
# print(id(mongoManager.test))
