
class ZeroDevError(Exception):
    pass


def calculate(x,y):
    try:
       if y == 0:
          raise ZeroDevError("not divided by zero")
    except ZeroDevError as e:
        print(e)

calculate(10,0)    
    