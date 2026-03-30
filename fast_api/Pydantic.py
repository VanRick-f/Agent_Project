from datetime import date
from pydantic import BaseModel, PositiveInt,EmailStr, ValidationError,Field,ConfigDict

class UserSchema_d(BaseModel):

    id: int
    name: str
    email:EmailStr = None
    date_joined: date | None
    tastes: dict[str, PositiveInt] #正整数

external_data = {
        'id': 123,
        'date_joined': '2030-06-01',
        'email': 'zhangsan@example.com',
        'name':"张三" ,
        'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
},
}

try:
    user_schema = UserSchema_d(**external_data)
except ValidationError as e:
    print(e.errors())




# 添加 Field字段
class UserSchema_F(BaseModel):
    id: int = Field(..., description="用户id")
    name: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    date_joined: date | None = Field(None, description="加入时间")
    tastes: dict[str, PositiveInt] = Field(..., description="用户口味")

    id = Field(18, description="用户id")
    print(id)



# 属性校验
class UserSchema(BaseModel):
    name: str
    age: int

    model_config = ConfigDict(
        from_attributes=True
    )

class UserModel:
    def __init__(self, name, age):
        self.name = name
        self.age = age


user_model = UserModel(name="张三", age=18)
user_schema = UserSchema.model_validate(user_model)
print(user_schema)

