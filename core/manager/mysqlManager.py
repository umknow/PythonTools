# -*- coding: utf-8 -*-
# @Date: 2019-04-25
# @Author:zoubiao
import decimal
from collections import OrderedDict

import pymysql
import sqlalchemy
from DBUtils.PooledDB import PooledDB
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from quotations.conf import config
import pandas as pd


class MysqlPool:
    '''
    数据库连接池的单例模式
    '''
    __intance = {}  ## 单例使用
    __pool = {}  ## 区分不同的连接池


    def __new__(cls, db_type):
        if db_type not in cls.__intance:
            cls.__intance[db_type] = super(MysqlPool, cls).__new__(cls)
        return cls.__intance[db_type]

    def __init__(self, db_type):
        if db_type not in self.__pool:
            MysqlPool.init_pool(db_type)
        self.pool = self.__pool[db_type]

    @staticmethod
    def init_pool(db_type):

        conf = config('mysql').get(db_type)##从配置中获取到数据库信息
        MysqlPool.__pool[db_type] = PooledDB(**conf)


class ORMBase:
    '''
    数据库orm的单例模式
    '''
    __intance = {}
    __engine_obj = {}

    def __new__(cls, db_type):
        if db_type not in cls.__intance:
            cls.__intance[db_type] = super(ORMBase, cls).__new__(cls)
        return cls.__intance[db_type]

    def __init__(self, db_type):

        if db_type not in self.__engine_obj:
            ORMBase.init_engine(db_type)

        self.engine = self.__engine_obj[db_type]
        self.session = scoped_session(sessionmaker(bind=self.engine, autoflush=False, autocommit=False))

    @staticmethod
    def init_engine(db_type):
        MYSQL_PATH = config('mysql').get(db_type, uri=True)
        engine = create_engine(MYSQL_PATH, pool_recycle=10, pool_size=30, max_overflow=0, pool_timeout=60)
        ORMBase.__engine_obj[db_type] = engine


class MysqlManager:
    '''
    mysql数据库封装，使用pooledDB库实现单例数据库连接池，以及SQLALCHAMY的orm实例。
    ##如果想直接通过sql获取到结果，使用read_sql方法，参数to_pandas默认为False，
    ##返回list结果，True代表返回pandas结果。
    >>> sql = "SELECT * FROM `macd_daily_bfq` limit 1;"
    >>> result_list = MysqlManager('quant').read_sql(sql)
    >>> print(isinstance(result_list, list))
    True
    >>> result_pd = MysqlManager('quant').read_sql(sql, to_DataFrame=True)##to_DataFrame
    >>> print(isinstance(result_pd, pd.DataFrame))
    True
    >>> with MysqlManager('quant') as session:
    ...   result = session.fetchall(sql)
    >>> print(isinstance(result_list, list))
    True
    >>> with MysqlManager('quant').Session as session:
    ...    print(isinstance(session, sqlalchemy.orm.session.Session))
    True
    '''
    __intance = {}

    def __init__(self, db_type=None):

        self.__pool = MysqlPool(db_type).pool##单例数据库连接池
        self.__session = ORMBase(db_type).session
        self.engine = ORMBase(db_type).engine

    @property
    def __init_conn(self):

        self.__conn = self.__pool.connection()  ##获取连接
        self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)

    @property
    @contextmanager
    def Session(self):
        session = self.__session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def execute_many(self, sql, params=None):
        sql_list = sql.strip().split(';')
        sql_list.remove('')
        try:
            self.__init_conn
            for sql in sql_list:
                self.__cursor.execute(sql, params)
            self.__conn.commit()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def execute(self, sqls, params=None):
        '''
        等同mysql中的execute，执行sql语句.
        :param sql:
        :param params:u
        :return:
        '''
        try:
            self.__init_conn
            self.__cursor.execute(sqls, params)
            self.__conn.commit()
            return True
        except Exception as e:
            self.__conn.rollback()
            raise e

    def read_sql(self, sql, to_DataFrame=False):
        """
        执行查询sql，返回结果。
        :param sql:
        :param to_DataFrame:是否返回panda结构数据。
        :return:
        """
        return self.__read_main(sql=sql, to_DataFrame=to_DataFrame)

    def read_safe_sql(self, sql, params, to_DataFrame=False):
        """
        安全执行查询sql，添加params，防止sql注入
        :param sql:
        :param params:
        :param to_DataFrame:
        :return:
        """
        return self.__read_main(sql, params, to_DataFrame)

    def __read_main(self, sql, params=None, to_DataFrame=False):
        """
        执行sql查询
        :param sql:
        :param params:
        :param to_DataFrame:
        :return:
        """
        try:
            result = self.fetchall(sql, params, to_DataFrame)
            return result
        except Exception as e:
            print(e)
            raise e


    def __change_type(self, result):

        for info_dict in result:
            for k, v in info_dict.items():
                if isinstance(v, decimal.Decimal):
                    info_dict[k] = float(v)
        return result

    def fetchall(self, sql, params=None, to_DataFrame=False):
        '''
        获取sql查询出的所有数据，默认转换为列表字典格式
        :param sql:
        :param params:
        :return:
        '''
        try:
            self.execute(sql, params)
            result = self.__cursor.fetchall()

            if result:
                result = self.__change_type(result)  ##替换decimal类型数据
            if to_DataFrame:
                # Create DataFrame Preserving Order of the columns:  noqa
                result_fix = list(map(lambda x: OrderedDict(x), result))
                result = pd.DataFrame(list(result_fix))
            return result
        except Exception as e:
            print('sql error %s' % str(e))
            raise e
        finally:
            self.close()

    def insert_many(self, sql, values=[]):
        '''
        批量插入，args为数据列表。
        :param sql: insert into tablename (id,name) values (%s,%s)
        :param values:[(1,'test'),(2, 'new')]
        :return:
        '''
        try:
            self.__init_conn
            self.__cursor.executemany(sql, values)
            self.__conn.commit()
        except Exception as e:
            self.__conn.rollback()
            raise e
        finally:
            self.close()

    def __enter__(self):
        '''
        上下文管理器中进入，则返回该对象
        :return:
        '''
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.__cursor.close()
        self.__conn.close()

if __name__ == '__main__':
    sql = 'select code,date,MA5,MA10,MA20,MA60,resample_date,fact,close from ma_daily_bfq where code = %s and frequency=%s and id>=0 order by `date` desc limit %s '

    params = ['000698.SZ', 'mothly', 60]
    #
    result = MysqlManager('quant')
    data = result.read_safe_sql(sql, params=params)
    print(data)
    # import doctest
    #
    # doctest.testmod(verbose=True)
    # @retry(tries=3, delay=0.5)
    # def deal_sql(sql):
    #     try:
    #         print(sql)
    #         with MysqlManager('quant') as session:
    #             session.fetchall(sql)
    #     except Exception as e:
    #         print('----------------------------')
    #         raise e
    # deal_sql(sql)
    # import time
    # start = time.time()
    # from multiprocessing.pool import ThreadPool
    #
    # start = time.time()
    # pool = ThreadPool(4)
    #
    # for i in range(10000):
    #     pool.apply_async(deal_sql, (i,))
    # pool.close()
    # pool.join()
    # print(time.time()-start)

    # for i in range(10000):
    #     with MysqlManager('python') as session:
    #         session.fetchall(sql)
    # print(time.time() - start)

    