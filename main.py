import os
import pathlib
import socket
import sys
import threading
import subprocess
import time

import inotify.adapters

from statemachine import *
import parser as p

# First we should op en a file and read the content
# Then we should send the content via UDP to the server
ip = "127.0.0.1"

filename = pathlib.Path("child.bin")
log = pathlib.Path("log.txt")
sm = ThreadStateMachine(Thread.states[0])
openthread_args = '../openthread/output/simulation/bin/ot-cli-ftd 1 --master --dataset ' \
                  '"{\\"Network_Key\\": \\"cf70867da8d41fbdb614aa9677addf9e\\", \\"PAN_ID\\": \\"0x7063\\"}" '

rcode = 0


def openthread():
    global rcode
    while True:
        rcode = subprocess.Popen(openthread_args, shell=True).wait()
        print(rcode)


def proxy(listenport):
    global rcode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    aflnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aflnet.bind((ip, listenport))
    aflnet.setblocking(0)

    while True:
        try:
            data, addr = aflnet.recvfrom(1024)  # buffer size is 1024 bytes
            res = p.assign_command_type(data)
            print(res[0]['Name'])
            # sm.advance_state(res[0]['Name'])
            # print(sm.to_str())
            sock.sendto(data, (ip, 5001))
        except:
            pass
        if rcode != 0:
            print(type)
            with open(log, "a+") as f:
                print("Crash?")
                f.write("----- ----- ----- ----- -----")
                f.write("Crashed with rcpde: " + rcode)
                f.write(res.__str__() + '\n')
                f.write("----- ----- ----- ----- -----")
            rcode = 0


def superduper(port):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    i = inotify.adapters.Inotify()

    bin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if not os.path.isfile(filename):
        with open(filename, "w+") as f:
            pass
    # open the file and read the content
    i.add_watch(filename.__str__())
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, _) = event
        if "IN_CLOSE_WRITE" in type_names or "IN_MOVE_SELF" in type_names or "IN_MODIFY" in type_names:
            # Read file, its in binary format
            with open(filename, "rb") as f:
                content = f.read()
                cmd_type = p.assign_command_type(content)
                if cmd_type and cmd_type[0] and cmd_type[0]['Name'] != Commands.ANNOUNCE:
                    print(cmd_type[0]['Name'])
                    # sm.advance_state(cmd_type[0]['Name'])
                    sock.sendto(content, (ip, port))
                    bin.sendto(content, (ip, 7331))

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
    openthreadthread = threading.Thread(target=openthread)
    thread = threading.Thread(target=superduper, args=(port,))
    thread.start()
    openthreadthread.start()
    proxy(listenport)


if __name__ == '__main__':
    _main()
