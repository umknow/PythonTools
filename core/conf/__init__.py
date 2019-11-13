# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/4/10 9:56
# describtion: 
"""
    初始化项目配置信息
    服务器系统环境变量初始化设置：
    export QPLUS_ENV=test_env  # 测试
    export QPLUS_ENV=production  # 生产
"""
import os
import pymysql
import configparser
from kombu import Queue


class BaseInfo:
    """
        加载对应的配置文件信息
        备注：
            如果有特殊需求需要获取配置文件内的节点基本信息，则可导入此类自行实例化获取。
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):  # 反射
            cls._instance = object.__new__(cls)
            cls._cached = False
        return cls._instance

    def __init__(self):
        if not BaseInfo._cached:
            self.cf = configparser.ConfigParser()  # 实例化解析配置文件实例
            self.__env = os.environ.get('QPLUS_ENV', 'development')  # 获取当前环境信息,未设置或[环境变量名]设置错误则默认本地环境
            print('[Current Env]', self.__env)
            # self.__env = 'test_env'  # 本地测试测试环境的配置信息
            # self.__env = 'production'  # 本地测试生产环境的配置信息
            self.__env_setting_file_name = {
                'development': 'development.conf',
                'test_env': 'testing.conf',
                'production': 'production.conf'
            }.get(self.__env, 'development')  # 获取环境对应的配置文件名
            self.cf.read(os.path.dirname(__file__) + os.sep + self.__env_setting_file_name, encoding='utf-8')  # 读取到缓存
            BaseInfo._cached = True

    @property
    def secs(self):
        """
            查看所有节点
        :return:
        """
        __secs = self.cf.sections()  # 节点名
        return __secs


# conf_info = BaseInfo()  # 单独实例化Baseinfo


class MySql:
    """
        mysql数据库配置信息的获取
        各库节点名称介绍（get方法的inode_name）：
            quant ：quant_new|quant_start  [数据-quant]
            wind : wind [数据-万德]
            hq : hq [数据-行情]
            liang : liang|laing_zhun [业务]
            trans_niu : 3.0交易[业务]
    """

    def __init__(self):
        self.__conf_info = BaseInfo()  # 实例base_info
        self.__mysql_pol_base_conf = dict(
            creator=pymysql,  # 使用链接数据库的模块
            maxusage=None,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxconnections=None,  # 连接池允许的最大连接数，0和None表示不限制连接数
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            mincached=self.__conf_info.cf.getint("pool_conf", "mincached"),  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=self.__conf_info.cf.getint("pool_conf", "maxcached"),  # 链接池中最多闲置的链接，0和None不限制
            maxshared=self.__conf_info.cf.getint("pool_conf", "maxshared"),
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            ping=self.__conf_info.cf.getint("pool_conf", "ping"),  # ping MySQL服务端，检查是否服务可用。
            local_infile=1,  # 服务器变量指示能否使用load data local infile命令
        )  # DBUtils 配置专用

    def get(self, inode_name, uri=False):
        """
            获取conf中mysql有关的基本配置信息
        :param inode_name:
        :return:
        """
        try:
            if uri is True:
                return self.__conf_info.cf.get(inode_name, "uri")
            __mysql_conf = dict(
                host=self.__conf_info.cf.get(inode_name, "host"),
                port=self.__conf_info.cf.getint(inode_name, "port"),
                user=self.__conf_info.cf.get(inode_name, "user"),
                passwd=self.__conf_info.cf.get(inode_name, "passwd"),
                charset=self.__conf_info.cf.get(inode_name, "charset"),
                db=self.__conf_info.cf.get(inode_name, "db")
            )  # 数据quant
            __mysql_conf.update(self.__mysql_pol_base_conf)
        except:
            raise ValueError('Invalid keys! \n 【请检查输入参数的正确性！\n目前支持:'
                             '\nquant <-- quant_new|quant_start  [数据-quant]'
                             '\nwind <-- wind [数据-万德]'
                             '\nhq <-- hq [数据-行情]'
                             '\nliang <-- liang|laing_zhun [业务]'
                             '\ntrans_niu <-- 3.0交易[业务] 】.')
        return __mysql_conf


class Redis:
    """
        redis配置信息的获取
    """

    def __init__(self):
        # 【注册】 库mapping (如果后期添加了新的，须先在这注册一个)
        self.__mapping = dict(
            bus_0='redis_bus',  # 业务
            bus_3='redis_bus',
            bus_15='redis_bus',  # 自选业务新需求
            data_10='redis_data',  # 数据
            test_data='redis_data',  # 【开放通道】测试使用
            test_bus='redis_bus',
        )
        self.__conf_info = BaseInfo()  # 实例base_info

    def get(self, db_type):
        """
            根据传入库类型返回对应的配置信息
        :param db_type: [
                data_db10 : 数据使用的库
                bus_db0 : 业务的官方赛
                bus_db3 : 业务
                test_data_num : 数据开放接口
                test_bus_num : 业务开放接口
                  ]  # 后期添加同理
        :return:
        """
        try:
            __db_type_str_list = db_type.rsplit('_', 1)
            __db_num = int(__db_type_str_list[-1])  # 库序号
            if __db_type_str_list[0].startswith('test_'):  # 开放入口
                db_type = __db_type_str_list[0]  # 不能设置默认值，下游传错直接异常即可
            __db_name = self.__mapping.get(db_type)  # 不能设置默认值，下游传错直接异常即可
            __return_info = dict(
                decode_responses=True,
                host=self.__conf_info.cf.get(__db_name, 'host'),
                port=self.__conf_info.cf.getint(__db_name, 'port'),
                password=self.__conf_info.cf.get(__db_name, 'passwd'),
                db=__db_num
            )
        except:
            raise ValueError('Invalid keys! \n 【请检查输入参数的格式，比如: bus_3 ,结尾数字代表要连接的目标库序号，如果没有注册，请到Redis类中注册一个。\
                \n目前支持：\n  bus_0 : 业务的官方赛\n  bus_3 : 业务\n  data_10 : 数据使用的库\n  test_data_[num] : 数据开放入口'
                             '\n  test_bus_[num] : 业务开放入口 \n 备注：[num]是任意库序号 】.')
        return __return_info


class Mongo:
    """
        mongo配置信息的获取
    """

    def __init__(self):
        self.__conf_info = BaseInfo()  # 实例base_info

    def get(self, uri=False):
        if uri is True:
            return self.__conf_info.cf.get("mongo", "uri")
        try:
            __return_info = dict(
                host_main=self.__conf_info.cf.get("mongo", "host_main"),  # 主
                host_standby=self.__conf_info.cf.get("mongo", "host_standby"),  # 备
                port=self.__conf_info.cf.getint("mongo", "port"),
                authSource=self.__conf_info.cf.get("mongo", "auth_source"),
                username=self.__conf_info.cf.get("mongo", "user"),
                password=self.__conf_info.cf.get("mongo", "passwd"),
                replica_set=self.__conf_info.cf.get("mongo", "replica_set")  # 副本集模式地址
            )
        except:
            raise ValueError('Invalid keys! \n 【请检查输入参数的格式，比如: config("mongo").get(uri=True) 】.')
        return __return_info


class Celerys:
    """
    celery配置信息获取
    """

    def __init__(self):
        self.__conf_info = BaseInfo()  # 实例base_info

    def get(self):
        __return_info = dict(
            CELERY_BROKER_URL=self.__conf_info.cf.get("celery", "CELERY_BROKER_URL"),
            CELERY_RESULT_BACKEND=self.__conf_info.cf.get("celery", "CELERY_RESULT_BACKEND"),
            CELERY_IGNORE_RESULT=True,
            CELERYD_MAX_TASKS_PER_CHILD=self.__conf_info.cf.getint("celery", "CELERYD_MAX_TASKS_PER_CHILD"),
            CELERYD_TASK_TIME_LIMIT=self.__conf_info.cf.getint("celery", "CELERYD_TASK_TIME_LIMIT"),
            CELERY_TIMEZONE=self.__conf_info.cf.get("celery", "CELERY_TIMEZONE"),
            CELERY_TASK_SERIALIZER=self.__conf_info.cf.get("celery", "CELERY_TASK_SERIALIZER"),
            CELERY_RESULT_SERIALIZER=self.__conf_info.cf.get("celery", "CELERY_RESULT_SERIALIZER"),
            CELE_ACCEPT_CONTENT=['json'],
            CELERY_QUEUES=(
                Queue('default'),
                Queue('priority_high'),
            )
        )
        return __return_info


def config(type):
    """
    获取配置信息入口
    :param type: 实例类型
    :return: 对应实例对象
    """
    __type_mapping = {
        'mysql': MySql,
        'redis': Redis,
        'mongo': Mongo,
        'celery': Celerys,
    }
    __Type = __type_mapping.get(type)
    if not __Type:
        raise ValueError('Invalid keys! \n 【请检查config()输入参数的正确性！目前支持：mysql，redis，mongo,celery】.')
    return __Type()


if __name__ == '__main__':
    # 【使用测试】
    print(config('mysql').get('trans_niu', uri=True))  # mysql
    print(config('redis').get('test_data_10'))  # redis
    print(config('mongo').get(uri=True))  # mongo
    print(config('celery').get())
