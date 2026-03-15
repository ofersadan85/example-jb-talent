import threading
from time import sleep

lock = threading.Lock()
count = []


def task(n: int):
    current = threading.current_thread()
    for i in range(n):
        print("Thread number " + str(current) + ": " + str(i))

        with lock:
            last = 0 if len(count) == 0 else count[-1]
            count.append(last + 1)
    return n


def background_log():
    while True:
        sleep(1)
        with open("log.log", "a") as f:
            f.write("AGAIN\n")


class WorkerThread(threading.Thread):
    def __init__(self, n: int):
        self.n = n
        super().__init__()
        self.start()

    def run(self):
        current = threading.current_thread()
        for i in range(self.n):
            print("Thread number " + str(current) + ": " + str(i))

            with lock:
                last = 0 if len(count) == 0 else count[-1]
                count.append(last + 1)
        self._return = self.n


t1 = threading.Thread(target=task, args=[100])
t2 = threading.Thread(target=task, args=[100])
t3 = WorkerThread(100)
t4 = WorkerThread(10)
t5 = threading.Thread(target=background_log, daemon=True)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
t4.join()

print("COUNT:", count)
print("MAIN THREAD EXIT")
