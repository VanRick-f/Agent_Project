from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


DB_URI = "postgresql+psycopg_async://rick_van:8989100@127.0.0.1:5432/mydb"
engine = create_async_engine(
    DB_URI,
    # 将输出所有执行SQL的日志（默认是关闭的）
    echo=True,
    # 连接池大小（默认是5个）
    pool_size=10,
    # 允许连接池最大的连接数（默认是10个）
    max_overflow=20,
    # 获得连接超时时间（默认是30s）
    pool_timeout=10,
    # 连接回收时间（默认是-1，代表永不回收）
    pool_recycle=3600,
    # 连接前是否预检查（默认为False）
    pool_pre_ping=True,
)



AsyncSessionFactory = sessionmaker(
    # Engine或者其子类对象（这里是AsyncEngine）
    bind=engine,
    # Session类的代替（默认是Session类）
    class_=AsyncSession,
    # 是否在查找之前执行flush操作（默认是True）
    autoflush=True,
    # 是否在执行commit操作后Session就过期（默认是True）
    expire_on_commit=False
)


# 定义命名约定的 Base 类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        # ix: 普通索引，格式为 ix_列名
        "ix": 'ix_%(column_0_label)s',
        # uq: 唯一约束，格式为 uq_表名_列名
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        # ck: 检查约束，格式为 ck_表名_约束名
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        # fk: 外键约束，格式为 fk_表名_列名_关联表名
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        # pk: 主键约束，格式为 pk_表名
        "pk": "pk_%(table_name)s"
    })

