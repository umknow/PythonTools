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

print("*" * 40)

# 【实现简单的垃圾回收机制】


class Container:
    def __init__(self):
        self.dict = {}

    def add(self, obj):
        # 维护弱引用, 实现gc回调
        self.dict[weakref.ref(obj, self.gc)] = id(obj)

    def gc(self, ref_obj):
        obj_id = self.dict[ref_obj]
        print("移除object id:", obj_id, "weakref对象:", ref_obj, "指向的对象:", ref_obj())
        del self.dict[ref_obj]


class SomeCls:
    pass


# 容器
container = Container()
# 任意对象
obj1 = SomeCls()
obj2 = SomeCls()
# 加入容器
container.add(obj1)
container.add(obj2)
# 释放对象
del obj2
del obj1





while 1:
    time.sleep(10)  # 阻止退出触发del，导致不方便观察
