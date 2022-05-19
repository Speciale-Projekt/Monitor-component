import socket
import inotify.adapters
import pathlib
import os
from statemachine import *
import sys
import threading
import parser

# First we should op en a file and read the content
# Then we should send the content via UDP to the server
ip = "127.0.0.1"

filename = pathlib.Path("/home/lars/test/child.bin")
sm = ThreadStateMachine(Thread.states[0])


def proxy(listenport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    bin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    bin.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    aflnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aflnet.bind((ip, listenport))

    while True:
        data, addr = aflnet.recvfrom(1024)  # buffer size is 1024 bytes
        print(data)
        sock.sendto(data, (ip, 5001))
        bin.sendto(data, (ip,7331))

def superduper(port):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
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
                content = f.read()
                print(content)
                sock.sendto(content, (ip, port))
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

def _main():
    if len(sys.argv) == 1:
        print("Please provide the id for the Thread Device")
        return -1

    id = int(sys.argv[1])
    listenport = 10000 + id
    port = 4000 + id

    print("Id of this device is: ", id)
    print("Listen port is: ", listenport)
    print("Aflnet local port is:", port)
    thread = threading.Thread(target=superduper, args=(port,))
    thread.start()
    proxy(listenport)



if __name__ == '__main__':
    _main()
