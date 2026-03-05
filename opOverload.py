class add_str_init:
    
    @classmethod
    def __add__(cls,strV,intV):
        return int(strV)+intV
    
     
print(add_str_init.__add__("45",34))        