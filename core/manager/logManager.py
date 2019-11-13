"""
    日志文件切割参照：https://blog.csdn.net/u012450329/article/details/53067717

"""
import os
import logging
from logging import handlers
from quotations.constants import *  # 项目总根目录


def init_path(log_file_path):
    log_file_path = log_file_path.rsplit(os.sep, 1)[0]
    if not os.path.exists(log_file_path):
        os.mkdir(log_file_path)


def getLogger(logname, name, print_flag=True):

    # 创建一个logger
    lg = logging.getLogger(name)
    lg.setLevel(logging.DEBUG)
    init_path(logname)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(logname, encoding='utf-8')  # 原始
    # 按大小切割模式
    # fh = logging.handlers.RotatingFileHandler(logname, maxBytes=1024 * 1024, backupCount=40)
    # 按时间切割模式 （切分格式：debug.log.2013-06-28，debug.log.2013-06-28）
    # fh = logging.handlers.TimedRotatingFileHandler(logname, when='d', interval=1, backupCount=40)
    fh.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # 给logger添加handler
    lg.addHandler(fh)

    # 再创建一个handler，用于输出到控制台
    if print_flag:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        lg.addHandler(ch)
    return lg


# ## 【logger】
# [data_statistics_and_mining]
# 创建收益率日志  # from data_statistics_and_mining
yield_rate_logger = getLogger(YIELD_RATE_PATH, 'data_statistics_and_mining')
# [quant_backend]
logger = getLogger(QUANT_LOG_PATH, 'quant_backend')  # from quant_backend
# 模拟盘日志
simulation_logger = getLogger(SIMULATION_PATH, 'simulation')
transaction_logger = getLogger(TRANSACTION_PATH, 'transaction')
grand_profit_logger = getLogger(GRAND_PROFIT_LOG_PATH, 'grand_profit_log')

# [quotations]
industry_logger = getLogger(INDUSTRY_LOG_PATH, 'industry')  # 行业日志实例
region_logger = getLogger(REGION_LOG_PATH, 'region')  # 地域日志实例
conseption_logger = getLogger(CONSEPTION_LOG_PATH, 'conseption')  # 概念日志实例
real_time_logger = getLogger(REAL_TIME_LOG_PATH, 'real_time')  # 实时日志实例
real_time_error_logger = getLogger(REAL_ERROR_LOG_PATH, 'real_time_error')  # 实时日志错误信息

