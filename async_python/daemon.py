import threading
import time


def monitor_temp():
    while True:
        print(f"Monitoring temperature...")
        time.sleep(2)
        

#daemon=True -> when main thread will stop then thread created from that main thread will automatically stop
#daemon=False -> even when main thread will stop but thread created from that will running until we force fully
# stop it

t = threading.Thread(target=monitor_temp,daemon=True)
t.start()

print("Main program done")
