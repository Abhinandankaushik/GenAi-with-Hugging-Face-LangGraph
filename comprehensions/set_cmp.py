
# syntax : {expression for item in iterable if condition}

std_rolls = [
    100,
    200,
    400,
    500,
    900,
    200,
    300,
    500
]

"""
unique = { roll for roll in std_rolls  } #as it is set comprehension it gives only unique value from list

#as it is set comprehension it gives even num but only unique value from list
# unique = { roll for roll in std_rolls if roll%2 == 0 } 

print(unique)

"""


student = {
    
    "name" : ["Raein","Bran","lilly"],
    "roll" : [100,203,504],
    "regNo" : [323432,23423,23423]
}

""" comprehension is a way to wright long code into concise shorter way but execution of it will be same
as long code execute ,

for below code executed as : 

for item in student.values():
   for each in item :
     print(item)

output :     
 ["Raein","Bran","lilly"]
 ["Raein","Bran","lilly"]
 ["Raein","Bran","lilly"]
 [100,203,504]
 [100,203,504]
 [100,203,504]
 [323432,23423,23423]
 [323432,23423,23423]
 [323432,23423,23423]
 
"""

unique_std = { print(each) for item in student.values() for each in item }  

print(unique_std)
