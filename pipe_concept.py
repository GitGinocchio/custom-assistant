import multiprocessing
import time


def worker(conn):
    data = conn.recv()
    print("Worker received:", data)
    time.sleep(10)
    conn.send("Data received")

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=worker, args=[child_conn])
    process.start()


    parent_conn.send("Hello from the parent")
    while process.is_alive():
        print('working')

    response = parent_conn.recv()
    print("Parent received:", response)

    while True: pass