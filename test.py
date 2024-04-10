import threading
import time
import Time
import count
import val

def thread_function(name, delay):
    print("Thread {} started".format(name))
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("Thread {}: {}".format(name, time.ctime(time.time())))

if __name__ == "__main__":
    thread1 = threading.Thread(target=Time.runTime)  # thread with delay of 2 seconds
    thread2 = threading.Thread(target=count.conut,args=(val.token,val.text))  # thread with delay of 3 seconds
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()