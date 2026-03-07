from functools import wraps

def my_dec(func):
    @wraps(func)
    def wrapper():
        print("Before function execution")
        func()
        print("After function execution")
    return wrapper


@my_dec
def greet():
    print("Hello from Decorators")
    
    
greet()   # greet = my_dec(greet) it return wrapper -> greet = wrapper -> greet() == wrapper()

print(greet.__name__)   #it shows the name of wrapper because geet = wrapper()
                        # to preserve the metadata we use wraps module 
                        # it does that it copy all metadata of original greet into wrapper metadata 
                        # like :- wrapper.__name__ = greet.__name__ etc                        
print(greet.__closure__)