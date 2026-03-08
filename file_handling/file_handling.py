# file = open("order.txt","w")


# try: 
#   file.write("File updated")
  
# finally:
#     file.close() 
     
     

with open("order.txt","w") as file:
    file.write("Order processing")