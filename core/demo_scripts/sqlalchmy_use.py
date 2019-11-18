"""
    【ORM】
    sqlalchemy use demo
"""
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# quant
# 创建engine
engine = create_engine('mysql+pymysql://root:xxx@xxx:3306/db_name')

# 基类的声明
BaseModel = declarative_base()


# 数据模型声明
class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))


# 自动创建
def init_db():
    BaseModel.metadata.create_all(engine)
init_db()


# 【使用】
DBSession = sessionmaker(bind=engine)
session = DBSession()


def write_test():
    # 写
    new_user = User(name='Huangyi')
    session.add(new_user)
    session.commit()
    session.close()


def read_test():
    # 查
    user = session.query(User).filter(User.id == 2).one()
    print('type:', type(user))
    print('name:', user.name)
    session.close()


if __name__ == '__main__':
    # write_test()
    read_test()
