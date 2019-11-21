# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/11/14 13:49
# describtion: 
"""
    魔法方法测试
"""


class Test:

    def __doc__(self, *args, **kwargs):
        return "__doc__ test"

    def __new__(cls, *args, **kwargs):
        res_cls = super(Test, cls).__new__(cls)
        print("res_cls >>", res_cls)
        return res_cls

    def __init__(self):
        pass

    def __str__(self):
        return "__str__ test"

    def __call__(self, *args, **kwargs):
        return "__call__ test"

    def __repr__(self, *args, **kwargs):
        return "__repr__ test"


class A:
    a = 12
    b = 23
    c = 45

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    # def __getattribute__(self, key):
    def __getattr__(self, key):
        return_info = self.__dict__.get(key)
        print('return_info:', return_info)
        return False

    def __str__(self):
        return 'Context mapping:{}'.format(self.__dict__)

    def __bool__(self):
        return self


# aa = A()

# print(dir(aa))
# print(getattr(aa, 'a_'))

# if hasattr(aa, 'a_'):
#     print('ssssssssssss', aa.a_)

# setattr(aa, 'ss', 23)

# aa.sd = 'asda'
# print(aa)

# la = lambda mods: getattr(globals()[mods[0]], mods[1])

class Foo:
    def __init__(self, item):
        self.item = item

    def __eq__(self, other):
        print('使用了equal函数的对象的id',id(self))
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        print('f'+str(self.item)+'使用了hash函数')
        return hash(self.item)



f1 = Foo(1)
f2 = Foo(2)
f3 = Foo(3)
fset = set([f1, f2, f3])


class Employee:
    """自定义字典"""
    def __init__(self, username=None, age=None):
        # self.username = username
        # self.age = age
        pass

    def __getitem__(self, attr):
        return super(Employee, self).__getattribute__(attr)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


if __name__ == '__main__':

    test = Test()

    print("[__doc__]", test.__doc__())
    print("[Test]", Test)
    print("[__str__]", test)
    print("[__call__]", test())
    print("[__repr__]", repr(test))
    print("[__repr__]", test.__repr__())

    print("*"*40)

    print(fset)
    d = dict()
    d[f1] = "sss"
    print(d)

    print("#"*49)
    em = Employee()
    em["age"] = 88
    print(em["age"])

    print("测试继承关系>>", issubclass(Test, object))
