import threading


lock = threading.Lock()

counter = 0

def increment():
    global counter
    for _ in range(100):
        thread_name = threading.current_thread().name
        print(f"writing by thread:{thread_name}")
        with lock:
            counter+=1
        
threads = [threading.Thread(target=increment) for _ in range(5)]
[t.start() for t in threads]
[t.join() for t in threads]


print(f"Final value of counter: {counter}")