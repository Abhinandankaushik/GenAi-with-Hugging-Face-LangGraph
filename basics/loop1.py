# program for first 10 odd number in python
count = 0
value = 1

while count < 10:
    if value%2 != 0:
        print(value)
        count+=1
    value+=1
        
