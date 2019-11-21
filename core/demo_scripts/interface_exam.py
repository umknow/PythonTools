# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/10/28 14:32
# describtion: 
"""
    Python interface 概念的实现
"""
from aifc import Error
from zope.interface import Interface
from zope.interface.declarations import implementer


# 【鱼产品日交易】

class CountFishInterface(Interface):
    "Fish counting interface"
    def oneFish():
        "Increments the fish count by one"

    def twoFish():
        "Increments the fish count by two"

    def getFishCount():
        "Returns the fish count"


class ColorFishInterface(Interface):
    "Fish coloring interface"

    def redFish():
        "Sets the current fish color to red"

    def blueFish():
        "Sets the current fish color to blue"

    def getFishColor():
        "This returns the current fish color"


class FishMarketInterface(CountFishInterface, ColorFishInterface):
    "This is the documentation for the FishMarketInterface"

    def getFishMonger():
        "Returns the fish monger you can interact with"

    def hireNewFishMonger(name):
        "Hire a new fish monger"

    def buySomeFish(quantity=1):
        "Buy some fish at the market"


class FishError(Error):
    pass


@implementer(FishMarketInterface)
class FishMarket:
    number = 0
    color = None
    monger_name = 'Crusty Barnacles'

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def oneFish(self):
        self.number += 1

    def twoFish(self):
        self.number += 2

    def redFish(self):
        self.color = 'red'

    def blueFish(self):
        self.color = 'blue'

    def getFishCount(self):
        return self.number

    def getFishColor(self):
        return self.color

    def getFishMonger(self):
        return self.monger_name

    def hireNewFishMonger(self, name):
        self.monger_name = name

    def buySomeFish(self, quantity=1):
        if quantity > self.number:
            raise FishError("There's not enough fish")
        self.number -= quantity
        return quantity

if __name__ == '__main__':

    # 需求：有个产品，其有10个子产品，现在要统计每日消费数据
    # 其中8个子产品的消费入账金额算法相同，2个不同;

    f = FishMarket(2, 'red')
    f.buySomeFish()
    print(f.getFishCount())

