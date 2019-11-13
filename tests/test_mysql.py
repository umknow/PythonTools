# -*- coding: utf-8 -*-
# @Date: 2019-05-17
# @Author: zoubiao
from sqlalchemy import and_

from quotations.manager.mysqlManager import MysqlManager
from quotations.models import MarketFocusNews

sql = 'SELECT * FROM `macd_daily_bfq` where date>"2018-10-11" and frequency = "daily" limit 1;'

###查询，获取padas结构数据
result_pd = MysqlManager('quant').read_sql(sql, to_pandas=True)
print('------------padas result----------------')
print(result_pd)


###查询，获取list结果数据
result_list = MysqlManager('quant').read_sql(sql)
print('----------------list result-------------')
print(result_list)
print(type(result_list))

###上下文管理器,
with MysqlManager('quant') as session:

    result = session.fetchall(sql)
    print('--------------use with ')
    print(result)

###上下文管理器，orm使用。
orm_session = MysqlManager('quant').Session
print(type(orm_session))
with MysqlManager('quant').Session as session:
    result = session.query(MarketFocusNews).filter(and_(
        MarketFocusNews.theme == '',
        MarketFocusNews.news_time == '')
    )
    print(result.first())