"""
student = {"name":"john","id":23123}


try:
    print(student["reg"])
except Exception as e:
    print(type(e))
    print(e)
"""

def get_student(name):
    try:
        print(f"Getting student...")
        if name == "":
         raise ValueError("Given Blank name")
    except ValueError as e:
        print("Error: ",e)
    else:
        print(f"Student : Found")
    finally:
        print("Thankyou for your query")
        
get_student("d")