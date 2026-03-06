
lst = [1,2,3,4,5]


# list comprehensions -> [expression for item in iterable if condition]


# evenNum = [ item for item in lst if (item%2 == 0) ]   #gives all even num

evenNum = [ item*2 for item in lst if (item%2 == 0) ]   #gives all even num with 2*item

print(evenNum)