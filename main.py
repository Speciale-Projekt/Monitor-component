import socket
import inotify.adapters
import pathlib
import os
from statemachine import *
import sys
import hashlib
import threading

# First we should op en a file and read the content
# Then we should send the content via UDP to the server
ip = "127.0.0.1"

filename = pathlib.Path("/home/lars/test/out.txt")
sm = ThreadStateMachine(Thread.states[0])

def proxy(listenport, servport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    aflnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aflnet.bind((ip, listenport))

    while True:
        data, addr = aflnet.recvfrom(1024)  # buffer size is 1024 bytes
        print(data)
        sock.sendto(data, (ip, servport))



def _main():
    if len(sys.argv) == 1:
        print("Please provide the id for the Thread Device")
        return -1

    id = int(sys.argv[1])
    listenport = 9000 + id
    servport = 5000 + id
    port = 4000 + id

    print("Id of this device is: ", id)
    print("Listen port is: ", listenport)
    print("Serv port is: ", servport)
    print("Aflnet local port is:", port)

    thread = threading.Thread(target=proxy, args=(listenport,servport))
    thread.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    i = inotify.adapters.Inotify()
    if not os.path.isfile(filename):
        with open(filename, "w+") as f:
            pass
    # open the file and read the content
    i.add_watch(filename.__str__())
    for event in i.event_gen(yield_nones=False):
       (_, type_names, path, _) = event
       print(event)
       if "IN_CLOSE_WRITE" in type_names or "IN_MOVE_SELF" in type_names or "IN_MODIFY" in type_names:
           # Read file, its in binary format
           with open(filename, "rb") as f:
               sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)
               content = f.read()
               print(content)
               sock.sendto(content, (ip, port))
               print("File sent to server")
       else:
           # check what files are in notify watchlist
           try:
               i.remove_watch(filename.__str__())
           except Exception as ignored:
               pass
           i.add_watch(filename.__str__())
           if not os.path.isfile(filename):
               with open(filename, "w+") as f:
                   pass  # remove old watch, and add new watch to same file


if __name__ == '__main__':
    _main()
