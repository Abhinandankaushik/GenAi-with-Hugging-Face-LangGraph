from pydantic import BaseModel , Field
from typing import List,Dict,Optional

class Cart(BaseModel):
    user_id: int
    items:  List[str]  #["abc","dfwe"]
    quantities: Dict[str,int]    #{"xyz":232}
    
    
class BlogPost(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None  #its optional default value is none but if provided then it should be an string 
    
class Employee(BaseModel):
    id : int 
    name : str = Field(
        ...,
        min_length=3,        #validation -> minimum length should be 3
        max_length=50,
        description="Employee Name",
        examples="Hitesh Choudhary"
    )
    department: Optional[str] = 'General'
    salary:float = Field(
        ...,       # ... means this filed is requred
        ge=10000   # ge-> >=10000 
    )
    
cart_data = {
    "user_id" : 123,
    "items" : ["Laptop","Mouse","Keyboard"],
    "quantities" : {"laptop":1,"mouse":2}
}    



cdata = Cart(**cart_data)
print(cdata)