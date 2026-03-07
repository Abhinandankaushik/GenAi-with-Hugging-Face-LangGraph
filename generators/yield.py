"""
yield:
you 
"""


def numbers():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5
    yield 6
    
num = (x for x in range(1,11) )

even = (ev for ev in num if ev % 2 == 0)

square = (val*val for val in even )

print(next(square))
print(next(square))
print(next(square))
print(next(square))
print(next(square))





    
    
