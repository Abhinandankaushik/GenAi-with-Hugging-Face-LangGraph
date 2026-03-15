from pydantic import BaseModel , ConfigDict
from typing import List
from datetime import datetime


class Address (BaseModel):
    street: str
    city: str
    zip_code: str


class User(BaseModel):
    id: int 
    name: str
    email: str
    is_active: bool =True
    createdAt: datetime
    address: Address
    tags: List[str] = []
    
    model_config = ConfigDict(
        json_encoders={datetime:lambda v:v.strftime('%d-%m-%Y %H:%M:%S')}
    )
    

user = User(
    id=1,
    name="Abhi",
    email="abhi@324.ai",
    createdAt=datetime(2024,3,15,14,13),
    address=Address(
        street="xyz",
        city="sdfsd",
        zip_code="32423"
    ),
    is_active=False,
    tags=["user"]
)


python_dict = user.model_dump()

print(python_dict)

print("="*30)

json_str = user.model_dump_json()
print(json_str)

user2 = User(
    id=1,
    name="Abhi",
    email="abhi@324.ai",
    createdAt=datetime(2024,3,15,14,13),
    address=Address(
        street="xyz",
        city="sdfsd",
        zip_code="32423"
    ),
    is_active=False,
    tags=["user"]
)
