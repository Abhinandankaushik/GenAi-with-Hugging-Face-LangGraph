from typing import List,Optional,Union
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    
class Company(BaseModel):
    name: str
    address: Optional[Address] = None
    
class Employee(BaseModel):
    name: str
    company: Optional[Company] = None
    

class TextContent(BaseModel):
    type: str = 'text'
    content:str 
    
class ImageContent(BaseModel):
    type: str = "Image"   # its -> Image: str == type:str = "Image"
    url: str
    alt_text: str 

class Articale(BaseModel):
    title: str
    section: List[Union[TextContent,ImageContent]]