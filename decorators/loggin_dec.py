from functools import wraps


def log_activity(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print(f"Calling: {func.__name__}")
        result = func(*args,**kwargs)
        print(f"Finished: {func.__name__}")
        return result
    return wrapper

@log_activity
def  log_error(*basic, **Complex):
     print(f"Logging basic Errors: {basic}")
     print(f"Logging Complex Errors: {Complex}")
     
 
log_error("Cpu Error",new_err="memory Error")     
