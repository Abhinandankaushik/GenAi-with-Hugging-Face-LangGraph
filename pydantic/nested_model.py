from typing import List,Optional
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    postal_code: str


class User(BaseModel):
    id: int 
    name: str
    address: Address
    
address = Address(
    street= "124 something",
    city= "Bilaspur",
    postal_code = "453345"
)



user = User(
    id = 123,
    name = "Abhii",
    address = address
)

print(user)