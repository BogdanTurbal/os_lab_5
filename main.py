from multiprocessing import Process, Queue
import time

def f(x):
    res = 1 + x
    while res > 0.000001:
        res *= 0.9999999
    return 0

def g(x):
    while x <= 0:
        pass
    return x

def process(fn, x, out_queue):
    res = fn(x)
    out_queue.put(res)

def terminate_processes(process_list):
    for process in process_list:
        if process.is_alive():
            process.terminate()
            process.join()  

if __name__ == "__main__":
    x = float(input("Init value: "))
    ask = True
    out_queue = Queue()

    process_f = Process(target=process, args=(f, x, out_queue))
    process_g = Process(target=process, args=(g, x, out_queue))

    process_f.start()
    process_g.start()

    current_time = 0
    t_step = 1
    t_num = 0
    complete = False
    while True:
        while not out_queue.empty():
            elem = out_queue.get()
            t_num += 1
            if elem > 0:
                complete = True
                
        if complete:
            print("Program ended successfully with result: True")
            terminate_processes([process_f, process_g]) 
            break
        if t_num >= 2:
            print("Program ended successfully with result: False")
            terminate_processes([process_f, process_g]) 
            break
            
        time.sleep(t_step)
        current_time += t_step
        
        if current_time % 10 == 0 and ask:
            print("Enter: \n 1 - Continue program \n 2 - End program \n 3 - Continue without further asking")
            try:
                res = int(input())
            except ValueError:
                res = 2
                
            if res == 1:
                pass
            elif res == 2:
                terminate_processes([process_f, process_g]) 
                break
            elif res == 3:
                ask = False
