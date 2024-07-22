import threading
import api

if __name__ == "__main__":

    thread1 = threading.Thread(target=api.detect)
    thread2 = threading.Thread(target=api.mainapi)
    

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Main thread exiting.")