""""
It used to save memory or it uses less memory which makes program faster

syntax :
   (expression for item in iterable if condition)
   
   
   [x for x in items] -> make entire list in memory

   (x for x in items) -> like a stream (means it give value one by one not store entire value at once like list)
                         which creates once in memory then it will return 
                         but generator do one by one and we apply function on it 
    
"""



daily_sales = [2,3,45,6,7,4,5,7,9,9,56,4,2,3,5,2,34,234]

# total_sale = sum( sale for sale in daily_sales if sale > 5)  #generator comprehension
# print(total_sale)

total_sale = ( sale for sale in daily_sales if sale > 5)  #generator comprehension

print(next(total_sale))
print(next(total_sale))
print(next(total_sale))

