# main.py
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field,field_validator
import re
from fastapi.responses import JSONResponse
from typing import Dict
from fastapi import Cookie
from fastapi import Header


# 创建 FastAPI 实例
app = FastAPI(title="智能招聘系统", version="1.0.0")

# 根路径
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 健康检查
@app.get("/test")
async def test():
    return {"function": "url test"}


@app.get("/items/{item_id}")
async def read_items(item_id:int = Path(description='用户 id', gt=1)):
    results = {"item_id": item_id}
    
    return results

# 查询参数
@app.get("/items")
async def read_item(
    page :int = Query(1,description="页码",ge=1),
    size :int = Query(10,description="每页数量",ge=10)
):
    return {"page": page, "size": size}

class LoginSchema(BaseModel):
    username: str = Field(..., description="用户名", min_length=3, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)


class LoginSchema(BaseModel):
    username: str = Field(..., description="用户名", min_length=3, max_length=20)
    password: str = Field(..., description="密码", min_length=6, max_length=20)

    @field_validator("password")#只校验这一个字段
    @classmethod#cls相当于self，因为这里只是传数据，类并没有实例化，校验成功之后才实例化
    def password_validator(cls, value) -> str: 
        pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
        if not re.match(pattern, value):
            raise ValueError("密码必须是数字和字母组合！")
        return value
@app.post("/login")
async def login(login_data: LoginSchema):
    return {"username": login_data.username, "password": login_data.password}


@app.get('/cookie/set')
async def set_cookie():
    response = JSONResponse(content={"username": "rick"})
    response.set_cookie('sessionid', 'xxx')
    return response



@app.get('/cookie/getcookie')
async def get_cookie(username: str = Cookie(default=None)):
    print("username:", username)
    return 'success'



@app.get('/header')
def get_header(user_agent: str|None=Header()):
    print('user-agent:', user_agent)
    return 'success'


# 依赖注入
from fastapi import Depends
from dependencies import common

@app.get('/item1')
async def read_items(common: Dict=Depends(common)):
    print(common.get('q'), common.get('page'), common.get('size'))
    return {"message": "ok"}

@app.get("/users")
async def read_users(common: dict = Depends(common)):
    return common





# 类依赖注入
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 2):
        self.q = q
        self.skip = skip
        self.limit = limit
@app.get("/item2")
async def read_items(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response




# 子依赖注入
users = [
    {"id": "1", "username": "张三"},
    {"id": "2", "username": "李四"}
]

def get_user_id(user_id: str = Header()):
    return user_id
def get_current_user(
    user_id: str = Depends(get_user_id)
) -> dict|None:
    for user in users:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail="该用户不存在！")
@app.get("/user1")
async def my(
    current_user: dict|None = Depends(get_current_user)
):
    return {"user": current_user}


# 装饰器依赖注入
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/item3/", dependencies=[Depends(verify_token)])
async def read_items(x_key=Depends(verify_key)):
    return {"x_key": x_key}




'''
ApiRouter
'''
from router import router as api_router

app.include_router(api_router)
