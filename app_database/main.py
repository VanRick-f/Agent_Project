from app_database import AsyncSessionFactory,AsyncSession
from fastapi import FastAPI,HTTPException
from app_database.schema import UserCreatSchemal,UserCreatRespones,UserSchema,UserUpdateSchema
from fastapi import Depends
from . import models
from app_database.models import User
from sqlalchemy import select,or_,and_,update
from typing import List

async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()

app = FastAPI()

@app.post('/user/add',response_model=UserCreatRespones)
async def add_user(
    user_data:UserCreatSchemal,
    session :AsyncSession= Depends(get_session)
):
    async with session.begin():
        user = models.User(**user_data.model_dump())
        session.add(user)
    return user


from sqlalchemy import delete

@app.delete('/user/delete/{user_id}')
async def delete_user(
    user_id: int, session:AsyncSession = Depends(get_session)
):
    async with session.begin():
        stmt = delete(User).where(User.id==user_id)
        await session.execute(stmt)
        return {"message": "删除成功！"}


# 查找一条数据
@app.get('/user/select/{user_id}', response_model=UserSchema)
async def select_user_by_id(
    user_id: int, 
    session: AsyncSession = Depends(get_session)
):
    async with session.begin():
        #query = select(User.id, User.email, User.username).where(User.id==user_id)
        query = select(User).where(User.id==user_id)
        result = await session.execute(query)
        result = result.scalar()
        if not result:
            raise HTTPException(404,detail="该用户不存在")
        return result

@app.get('/users/select/',response_model=List[UserSchema])
async def select_users(
    q:str = None,
    page = 1,
    size = 10,
    session:AsyncSession=Depends(get_session)
):
    async with session.begin(): 
        stmt = select(User)
        if q is not None:
            stmt = stmt.where(or_(User.email.contains(q),User.name.contains(q)))
        # 分页
        offset = (page - 1) * size  
        stmt = stmt.offset(offset).limit(size)
        #排序
        stmt = stmt.order_by(User.id) 
        result = await session.execute(stmt)
        users = result.scalars()
        return users
    
# 1. 查找，修改，再保存
@app.put('/user/update/{user_id}', response_model=UserSchema)
async def update_user(
    user_id: int, 
    user_data: UserUpdateSchema,
    session:AsyncSession = Depends(get_session)
):
    async with session.begin():
        stmt = select(User).where(User.id==user_id)
        user = await session.execute(stmt)
        if not user:
            raise HTTPException(404,'该用户不存在')
        user = user.scalar()
        user.email = user_data.email
        user.username = user_data.username
    return user

# 2. 直接修改
@app.put('/user/update_only/{user_id}')
async def update_user(
    user_id: int, 
    user_data: UserUpdateSchema,
    session:AsyncSession = Depends(get_session)
):
    async with session.begin():
        stmt = update(User).where(User.id==user_id).values(**(user_data.model_dump()))
        await session.execute(stmt)
    return {"message": "数据修改成功！"}
