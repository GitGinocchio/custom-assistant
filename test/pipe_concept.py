import multiprocessing

def worker(conn):
    data = conn.recv()
    print("Worker received:", data)
    conn.send("Data received")

if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=worker, args=(child_conn))
    process.start()


    parent_conn.send("Hello from the parent")
    response = parent_conn.recv()
    print("Parent received:", response)

    process.join()