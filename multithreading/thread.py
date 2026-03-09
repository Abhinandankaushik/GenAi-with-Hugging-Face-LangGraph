import threading
import time

def take_orders():
    for i in range(1,5):
        print(f"Taking order for #{i}")
        time.sleep(1)
    

def brew_coffe():
    for i in range(1,5):
        print(f"Brewing coffe for #{i}")
        time.sleep(2)
        

# create threads

order_thread = threading.Thread(target=take_orders)    

brew_thread = threading.Thread(target=brew_coffe)

order_thread.start()
brew_thread.start()

# # wait for both to finish
""" This t.join() method used to pause or wait for main thread to execute until mentioned thread are finished 
 means : 

  process:
     main thead - wait
     order_thread - running 
     brew_thread - running  
     
output: 
    print(f"Taking order for #{i}")
    print(f"Brewing coffe for #{i}")
    ...
    ...
     
and then last -> print(f"All orders taken and coffe brewed")

without join :

this statement will not wait to finish those two thread   
  print(f"All orders taken and coffe brewed")
 
"""
order_thread.join()
brew_thread.join()

print(f"All orders taken and coffe brewed")
