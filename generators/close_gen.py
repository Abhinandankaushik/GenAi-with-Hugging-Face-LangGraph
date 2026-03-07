"""
def get_Name():
    yield "Abhi"
    yield "Aadi"
    
    
def get_roll():
    yield "3001"
    yield "3002"
    
    
def get_details():
    
    yield from get_Name()   # it finish first 
    yield from get_roll()   # after that this line execute 
    

for d in get_details():
    print(d)
    """

def handle():
    try:
        while True:
            detail = yield "abhi:3001"
    except :
        print("No details available")

d = handle()

for i in range(5):
    print(next(d))
    d.close()
    break