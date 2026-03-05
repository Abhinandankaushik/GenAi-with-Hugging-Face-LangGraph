class student:
    def __init__(self,m):
        self._mark = m
    
    @property
    def mark(self):
       print("Printing current mark:\n",self._mark)
       return self._mark
    
    @mark.setter
    def mark(self,value):
        if(value < 0):
            print("Error: Makrs can not be -ve")
    @mark.deleter
    def mark(self):
        del self._mark
        print("deleting mark for:",self.__dict__.items())


s = student(50)
s.mark
del s.mark
s.mark = -90