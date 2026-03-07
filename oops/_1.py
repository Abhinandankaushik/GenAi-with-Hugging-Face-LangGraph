
class demo:
    x=10
    def __init__(self):
        self.y = 20
        

obj = demo()

print(f" class : {demo.__dict__}")
print(f"object: {obj.__dict__}")
demo.e =20

print(f" class : {demo.__dict__}")
print(f"object: {obj.__dict__}")
