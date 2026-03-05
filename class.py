"""class demo:
   x=5
   y=6
   def __init__(self,x):
    self.a=10

     

x = demo(12)

print(x.x)   #working beacuse of lookup chain just like Javascript instance(not found)->class(found)->parent_class->object
print(x.y)
print(demo.x)
print(demo.y)"""

"""
class Test:
    @staticmethod
    def f3():
        print("this is static method")
    @classmethod
    def f1():
        x=10
        print(x)
        return 20
    def f2(self):
     self.y=20
     print(self.y)
  

t1 = Test() #__init__(t1)
"""
"""
t1.f2()   #t1.f2(t1)    for instance method
Test.f3() #f3()         for static method
Test.f1() #t1.f1(Test)  for class method

"""


class Person:
    def __init__(self, age):
        self.age = age

    @classmethod
    def from_birth_year(cls, year):
        return cls(2026 - year)

p = Person.from_birth_year(2000)
print(p.age)
print(p)

