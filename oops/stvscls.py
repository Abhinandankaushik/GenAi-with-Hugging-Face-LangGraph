class Student:
    def __init__(self,name,id):
        self.name = name
        self.id = id

    @classmethod
    def init_student_list(cls,lst):
        return cls(lst[0],lst[1])
    
    @classmethod 
    def init_student_dict(cls,dct):
        return cls(dct["name"],dct["id"])
    
    
st1 = Student.init_student_dict({"name":"John","id":12323})


print(st1)
print(st1.__dict__)

st2 = Student.init_student_list(["Don",122000])

print(st2)
print(st2.__dict__)
