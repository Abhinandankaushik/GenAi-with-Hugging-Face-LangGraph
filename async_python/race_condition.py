import threading

stock = 1


def restStock():
    global stock
    for _ in range(100000):
        stock+=1
          
temp =[threading.Thread(target=restStock) for _ in range(2)] 

for t in temp : t.start()
for j in temp : j.join()   

print(f"Stock is: {stock}")