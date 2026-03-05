
class A:
    def __init__(self):
        self.b=80
        print("constuctor of A")
        
    def feature1():
        print("Feature 1 of A running")    
     
        
class B(A):
    def __init__(self):
        super().__init__()
        self.a=50
        print("constructor of B")
    
    def feature1():
        print("feature 1 of B running")       
        
        


b1 = B()
print(b1.a)
print(b1.b)
      