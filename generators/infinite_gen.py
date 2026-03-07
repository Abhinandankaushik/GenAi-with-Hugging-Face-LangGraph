import random

def infinite_num():
    count = 1
    while True:
        yield random.random()
        
for i in range(10):        
   # here every time new generator created and destroyed and garbase collector hold the memory
   # of destroyed generator and for next iteration when new generator creates it used
   # recently freed memory space thats why when we print id(next(infinite_num()))
   # we saw same id every time
   print(next(infinite_num()))   
                           



