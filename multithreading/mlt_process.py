from multiprocessing import Process
import time


def brew_coffe(name):
    print(f"Start of {name} coffe brewing")
    time.sleep(2)
    print(f"End of {name} coffe brewing")
        

if __name__ == "__main__":
    coffe_makers = [
        Process(target=brew_coffe , args=(f"Coffe Maker #{i+1}",))
        for i in range(3)
    ]

    # Start all process
    for p in coffe_makers :
       p.start()    
     
    # wait for all to complete   
    for p in coffe_makers:
       p.join()  

    print("All coffe served")