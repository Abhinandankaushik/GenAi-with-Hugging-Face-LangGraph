from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username : str 
    
    @field_validator('username')
    def username_length(cls,v):
        if len(v) < 4 :
            raise ValueError("Username must be atleast 4 characters")
        return v
  
class SignupData(BaseModel):    
    password : str
    confirm_password:str
    
    @model_validator(mode='before')           #befor -> cls #after -> self
    def password_match(cls,values):  
        if values["password"] != values["confirm_password"]:
          raise ValueError
        return values
    
    
user = User(username="abcr")
signupdata = SignupData(password="abc",confirm_password="abc")
print(user.username)