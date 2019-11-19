# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/13 14:13
# describtion: 
"""
    元类的测试
"""


class HelloMeta(type):

    def __init__(cls, name, bases, attrs):
        super(HelloMeta, cls).__init__(name, bases, attrs)
        print("name, bases, attrs >> ", name, bases, attrs)
        attrs_ = {}
        for k, v in attrs.items():
            if not k.startswith("__"):
                attrs_[k] = v
        setattr(cls, "_new_dict", attrs_)


class NewHello(object, metaclass=HelloMeta):  # metaclass=HelloMeta
    """自定义元类"""
    a = 1
    b = True

    def __init__(self):
        self.c = "sss"


print(NewHello._new_dict)
h2 = NewHello()
print(h2._new_dict)




# 【直接使用type动态创建类】
def hello(self):
    self.name = 10
    print("hello world")

t = type("hello", (), {"a": 1, "hello": hello})
print(t)
T = t()
print(T.a)
T.hello()
print(T.name)
