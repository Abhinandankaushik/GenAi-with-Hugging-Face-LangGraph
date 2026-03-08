def process_order(item,quantity):
    try:
        price = {"coffe":20,"tea":10,"Pizza":199}[item]
        cost = price*quantity
        print(f"total cost is: {cost}")
    except KeyError:
        print("sorry that is not on menu")
    except TypeError:
        print("Quantity must be in number")
    
 
process_order("coffe",2)    
process_order("tea","two")    
    