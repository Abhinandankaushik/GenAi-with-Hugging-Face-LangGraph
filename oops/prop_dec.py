class Student :
    def __init__(self,name):
        self._name = name
    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self,rename):
        self._name = rename
        
        
st = Student("John")

print(st.name)