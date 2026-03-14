from pydantic import BaseModel,field_validator

class Person(BaseModel):
    first_name: str
    last_name : str

    @field_validator('first_name','last_name')
    def names_must_be_capitalize(cls,v):
        if not v.istitle():
            raise ValueError("Name must be capitalized")
        return v
    
