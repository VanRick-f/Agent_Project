from pydantic import BaseModel,EmailStr,ConfigDict
class UserCreatSchemal(BaseModel):
    email:EmailStr
    username: str
    password: str

class UserCreatRespones(BaseModel):
    id:int
    email:EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)
    
class UserSchema(BaseModel):
    id:int
    email:EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    email:EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)