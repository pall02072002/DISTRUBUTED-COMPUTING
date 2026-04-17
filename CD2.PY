# Experiment2: Implement Client/Server using RPC/RMI
import socket
import threading
import pickle
import time

class RPCserver:
    def add(self, a, b):
        return a + b
    def multiply(self, a, b):
        return a * b

def server_program():
    server = RPCserver()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 6000
    s.bind((host, port))
    s.listen(1)
    print("RPC Server: Waiting for client...")
    conn, addr = s.accept()
    print("RPC Server: Client connected from", addr)
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        function_name, args = pickle.loads(data)
        print(f"RPC Server: Request -> {function_name}{args}")
        # Call actual method
        result = getattr(server, function_name)(*args)
        conn.send(pickle.dumps(result))
    conn.close()
    s.close()
# RPC CLIENT
def client_program():
    time.sleep(1) # wait for server
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("127.0.0.1", 6000))
    # Remote call 1
    request = ("add", (10, 20))
    c.send(pickle.dumps(request))
    result = pickle.loads(c.recv(1024))
    print("RPC Client: add(10,20) =", result)
    # Remote call 2
    request = ("multiply", (5, 6))
    c.send(pickle.dumps(request))
    result = pickle.loads(c.recv(1024))
    print("RPC Client: multiply(5,6) =", result)
    c.close()
# MAIN
server_thread = threading.Thread(target=server_program)
client_thread = threading.Thread(target=client_program)
server_thread.start()
client_thread.start()
server_thread.join()
client_thread.join()