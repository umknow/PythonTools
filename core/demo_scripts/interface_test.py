# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/21 11:31
# describtion: 
"""
    Python 接口的实现
    Python默认不支持接口和抽象类
    利用了第三方包实现
    抽象类和接口类是两个类似而又不同的概念
    方案一其实只是抽象类
    方案二符合真正意义上的接口规范
"""
import abc
from zope.interface import Interface
from zope.interface.declarations import implementer


# 【方案一：继承ABC抽象基类】
class Base(abc.ABC):
    """抽象基类（白鹅特性）
        https://blog.csdn.net/weixin_34240520/article/details/93561832
    """
    a = "ss"  # 抽象类中可以添加类属性，并且子类不用去实现
    @abc.abstractmethod
    def my_protocol(self):
        """
            自定义协议
            只要在当前环境中，任何类实现了接口中@abc.abstractmethod定义的所有方法，即这个类实现了这个接口
        """

    def get_name(self):
        return "wang yongsheng"

    @classmethod
    def __subclasshook__(cls, subclass):  # 实现虚拟子类的钩子（不用显示继承，隐式触发）
        if cls is Base:
            if any("my_protocol" in B.__dict__ for B in subclass.__mro__):
                return True
        return NotImplemented


class MyClass:  # 抽象类中实现了__subclasshook__所以这里不用显示继承也可以
    def my_protocol(self):
        pass

    def get_my(self):
        pass


# 【方案二：zope.interface实现】
# 定义接口
class MyMiss(Interface):
    def imissyouatlost(self, miss):
        """Say i miss you at lost to miss"""


@implementer(MyMiss)  # 继承接口，这里的继承其实跟通常意义上的继承还是不一样的
class Miss:
    def imissyouatlost(self, somebody):
        """Say i miss you at lost to somebody"""
        return "i miss you at lost, %s!" % somebody


if __name__ == '__main__':
    print("【方案一】")
    k = MyClass()
    print(isinstance(k, Base))

    print("方案二")
    z = Miss()
    hi = z.imissyouatlost('Zy')
    print(hi)
    print(isinstance(z, MyMiss))
