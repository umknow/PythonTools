# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/13 14:13
# describtion: 
"""
    关于元类的测试
    测试后小结：
        1、动态生成类
        2、可自由组装类的namespace中的数据
        3、用户可以继承经过封装的自定义元类从而自由定义类属性并输出指定的数据集（ORM就是典型的案例）
"""


class HelloMeta(type):
    """继承type，自定义元类"""
    def __init__(cls, name, bases, attrs):
        super(HelloMeta, cls).__init__(name, bases, attrs)
        print("name, bases, attrs >> ", name, bases, attrs)
        attrs_ = {}
        for k, v in attrs.items():
            if not k.startswith("__"):  # 将类的成员属性重新
                attrs_[k] = v
        setattr(cls, "_new_dict", attrs_)


class NewHello(object):  # metaclass=HelloMeta
    """常规类"""
    a = 1
    b = True

    def __init__(self):
        self.c = "sss"


class NewHelloM(object, metaclass=HelloMeta):  # metaclass=HelloMeta
    """自定义元类"""
    a = 1
    b = True

    def __init__(self):
        self.c = "sss"


print("常规类实例前：", NewHello.__dict__)
h2 = NewHello()
print("常规类实例后：", h2.__dict__)

print("实例前M：", NewHelloM._new_dict)
h2 = NewHelloM()
print("实例后M：", h2._new_dict)


print("#"*30)
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


print("*"*40)
# 【区分type、obejct、class之间的关系】
"""
    type是元类实例，本身就是本身的实例
    所有的对象都是type的实例
    type继承了object类
    常见数据类型其实本身就是type的实例
"""


print("类似type>>", type(HelloMeta))
print("常规类引用>>", type(NewHello))
print("常规类实例后>>", type(NewHello()))
print("自定义元类引用>>", type(NewHelloM))
print("自定义元类实例后>>", type(h2))
print("object类引用>>", type(object))
print("obejct实例>>", type(object()))
print("常规数据类型int>>", type(1232))
print("常规数据类型str>>", type("sdfa"))
