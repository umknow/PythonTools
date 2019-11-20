# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/20 13:36
# describtion: 
"""
    弱引用测试
"""
import time
import weakref


class A:
    def __init__(self, x):
        self._x = x

    def __repr__(self):
        return f'A类的{self._x}实例 {id(self)}'

    def __del__(self):
        print(f'摧毁啦 {self._x} 。。。。')


# wd = dict()  # 常规字典
wd = weakref.WeakKeyDictionary()  # 弱引用字典（对key）
# wd = weakref.WeakValueDictionary()

a1 = A(1)
a2 = A(2)

wd[a1] = 'xxxxxxx'
wd[a2] = 'yyyyyyy'

print('销毁a1对象前')
for item in wd.items():
    print(item)

del a1
print('销毁a1对象后')
for item in wd.items():
    print(item)

while 1:
    time.sleep(10)  # 阻止退出触发del，导致不方便观察
