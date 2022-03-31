from multiprocessing.connection import Listener
from multiprocessing import Process, Manager
from multiprocessing.connection import Client
import sys
from time import time
import traceback




def send_msg_all(pid,msg,clients):
    for client,client_info in clients.items():
        print (f"sending {msg} tp {client_info}")
        with Client(address=(client_info["adrdress"],client_info["port"]),authkey=client_info["authkey"]) as conn:
            if not client==pid:
                conn.send((pid,msg))
            else:
                conn.send(f"message {msg} prcessed")
                
def serve_client(conn,pid,clients):
    connected=True
    while connected:
        try:
            m=conn.recv()
            print(f"received message:[m]: from {pid}")
            if m="quit":
                connected=False
                conn.close()
            else:
                send_msg_all(pid,m,clients)
        except EOFError:
            print ("connection abruptly closed by client")
            connected=False
    del clients[pid]
    send_msg_all(pid,f"quit_client {pid}",clients)
    print (pid,"connection closed")
    

def main(ip_address):
    with Listener(address=(ip_address,6000),authkey=b"secret password server") as listener:
        print("listener starting")
        
        m=Manager()
        clients=m.dict()
        
        while True:
            print ("accepting conexions")
            try:
                conn=listener.accept()
                print("connection accepted from",listener.last_accepted)
                client_info=conn.recv()
                pid=listener.last_accepted
                clients[pid]=client_info
                
                send_msg_all(pid,f"new client {pid}",clients)
                
                p=Process(target=serve_client,arg=(args=conn,listener.last_accepted,clients))
                p.start()
            except Exception as e:
                traceback.print exc()
                
        print('end server')
        
if __name__=="__main__":
    ip_address="127.0.0.1"
    iif len(sys.argv)>1:
        ip_address=sys.argv[1]
    main(ip_address)
