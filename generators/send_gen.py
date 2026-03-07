
def process():
    print("Welcom ! What Process you want ?")
    process = yield
    while True:
        print(f"Executing Process: {process}")
        process = yield
    


execute = process()

next(execute) #start the generator

execute.send("CPU Halt")
execute.send("Collect Garbage Blocks")
execute.send("Run BIOS")