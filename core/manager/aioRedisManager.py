# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/9/23 18:20
# describtion: 
"""
    redis异步存储管理器
    # 使用方法介绍 >>
    主要用于写操作，因为读操作需要设置回调，相对消耗资源，暂未提供
    使用需构造如main中的方法，便于使用到串行脚本的循环中
"""
from quotations.conf import config
import functools
import aioredis
import asyncio


class BaseRedis:

    _redis = None

    def __init__(self, db_type):
        self.__db_type = db_type

    def __getattr__(self, item):
        return getattr(self._redis, item)

    def __enter__(self):
        """
        上下文管理器中进入，则返回该对象
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if self._redis:
            self._redis.close()
            self._redis.wait_closed()

    async def get_redis_pool(self):
        __redis_config = config('redis').get(self.__db_type)
        if not self._redis:
            self._redis = await aioredis.create_redis_pool(
                (__redis_config['host'], __redis_config['port']), password=__redis_config['password'],
                db=__redis_config['db'],
                encoding='utf-8'
            )
        return self._redis

    async def close(self):
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()


class AsyncRedis:

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        _loop = asyncio.get_event_loop()
        _get_future = self.func(*args, **kwargs)
        _loop.run_until_complete(_get_future)
        # return _get_future.result()  # 异步存储不需要结果


class AioRedisCon:
    __intance = {}

    def __new__(cls, db_type):
        """
        :param db_type:
        :return:
        """
        if db_type not in cls.__intance:
            cls.__intance[db_type] = BaseRedis(db_type)
        return cls.__intance[db_type]


class GetCon:
    def __init__(self, db):
        self._aio_redis = AioRedisCon(db)

    async def aio_op_redis(self, *args,  **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        _r = await self._aio_redis.get_redis_pool()
        await _r.execute(*args, **kwargs)

    async def close_pool(self):
        """释放连接池"""
        await self._aio_redis.close()


class AioRedisManager:

    __db_type = None

    def __new__(cls, db_type):
        cls.__db_type = db_type
        return cls

    def __init__(self, db_type, *args, **kwargs):
        pass

    @classmethod
    @AsyncRedis
    def async_redis(cls, *args, **kwargs):
        """
            将注册好的事件返回到回环监听处
        :param args:
        :param db:
        :param kwargs:
        :return:
        """
        return asyncio.ensure_future(GetCon(db=cls.__db_type).aio_op_redis(*args, **kwargs))

    @classmethod
    @AsyncRedis
    def close_pool(cls, *args, **kwargs):
        """
            关闭连接池
        :param db:
        :return:
        """
        return asyncio.ensure_future(GetCon(db=cls.__db_type).close_pool())


if __name__ == '__main__':

    # 使用测试
    go_redis = AioRedisManager('bus_3')

    # res_name = aio_redis_test('get', 'my-key')  # 读操作
    for i in range(100):
        res_name = go_redis.async_redis('set', 'my-key', 'MS Wang')  # 写
    else:
        go_redis.close_pool()  # 节约开关pool的开销
