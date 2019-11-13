# -*- coding: utf-8 -*-
# time ： 2019年4月28日 14:14:54
"""
    redis连接管理器包
"""
import redis
from quotations.conf import config


class RedisPool:
    __intance = {}

    def __new__(cls, db_type):
        if db_type not in cls.__intance:
            cls.__intance[db_type] = redis.ConnectionPool(**config('redis').get(db_type))
        return cls.__intance[db_type]


class RedisManager:
    """
        Redis管理器
    """

    def __init__(self, db_type):
        self.__connection_pool = RedisPool(db_type)  # 根据库类型使用单例连接池
        # 这个连接服务内部能自动管理连接池内的连接，使用完毕自动释放回连接池中（进入find-->get_connection）
        self.__connection = redis.StrictRedis(connection_pool=self.__connection_pool)

    def __getattr__(self, item):
        return getattr(self.__connection, item)

    def hsets(self, name, data):
        for key, value in data.items():
            self.hset(name, key, value)

    def delete_by_list(self, key_list):
        for __key in key_list:
            self.__connection.delete(__key)

    def empty(self, key):
        return self.__connection.llen(key) == 0

    def close(self):
        self.__connection.pubsub().close()











if __name__ == '__main__':

    ### 使用方法介绍
    # 【test】
    # print(RedisManager('b'))
    # print(RedisManager('bus_0'))  # 重复创建同一个实例
    # print(RedisManager('bus_3').pipeline())  # 测试连接指定库
    # print(RedisManager('data_10'))  #
    print(RedisManager('data_10'))  # 传参异常测试


    # keys = RedisManager('bus_3').keys('plate:14903:*')
    # print(keys)

    # pip = RedisManager('bus_3').pipeline()
    # pip.set('atk00001', 'www')

    # pip.set('atk00000', 'www')

    # pip.hset('atk0000', 'ssss', 'www')
    # pip.hset('atk0000', 'ssss1', 'www1')

    # pip.hmset('testplate:14903:{}'.format('00090'), {'reportsNum': 90909, 'reportsNumRanking': 1})
    # pip.hmset('testplate:14903:{}'.format('00091'), {'reportsNum': 90908, 'reportsNumRanking': 1})

    # pip.get('atk00001')

    # 指定key删除
    # pip.delete('testplate:14903:00091')
    # pip.delete('atk0000', 'testplate')  # 多个一起删除
    # 组内单条删除测试
    # pip.hdel('atk0000', 'ssss')
    # pip.hdel('testplate:14903:00090', 'reportsNum')

    # res = pip.execute()
    # print(res)



# import time
# time.sleep(10)