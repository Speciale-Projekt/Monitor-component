import os
import pathlib
import socket
import subprocess
import sys
import threading
from datetime import datetime

import inotify.adapters

import parser as p
from Statemachine.rules import valid_order_for_messages, Message, message_commands_succession
from Statemachine.statemachine import *

# First we should op en a file and read the content
# Then we should send the content via UDP to the server
ip = "127.0.0.1"

filename = pathlib.Path("child.bin")
log = pathlib.Path("log.txt")
smt_crash_log = pathlib.Path("stmch_crash.txt")
sm = ThreadStateMachine(Thread.states[0])
openthread_args = '../openthread/output/simulation/bin/ot-cli-ftd 1 --master --dataset ' \
                  '"{\\"Network_Key\\": \\"cf70867da8d41fbdb614aa9677addf9e\\", \\"PAN_ID\\": \\"0x7063\\"}" '

rcode = 0
prev_message: Message = None


def init_log(log_path):
    with open(log_path, "w") as f:
        f.write(f"Inti: {datetime.now().isoformat()}\n\n")




def openthread():
    global rcode
    while True:
        rcode = subprocess.Popen(openthread_args, shell=True).wait()
        print(rcode)


def communication_aflnet(listenport):
    global rcode
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    aflnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aflnet.bind((ip, listenport))
    aflnet.setblocking(0)

    while True:
        try:
            data, addr = aflnet.recvfrom(1024)  # buffer size is 1024 bytes
            res = p.assign_command_type(data[:-1])
            print(res[0]['Name'])
            # sm.advance_state(res[0]['Name'])
            # print(sm.to_str())
            sock.sendto(data, (ip, 5001))
            global prev_message
            msg = Message()
            msg.tlvs = res[0].get('tlvs')
            msg.command = res[0].get('Name')
            prev_message = msg

        except:
            pass
        if rcode != 0:
            with open(log, "a+") as f:
                print("Crash?")
                f.write("----- ----- ----- ----- ----- " + "\n")
                f.write(datetime.now().isoformat())
                f.write("Crashed with rcode: " + str(rcode) + "\n")
                f.write(res.__str__() + "\n")
                f.write("----- ----- ----- ----- -----\n")
            rcode = 0


def communication_OT(port):
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
                    msg: Message = Message()
                    msg.tlvs = cmd_type[0].get('tlvs')
                    msg.command = cmd_type[0].get('Name')
                    if not prev_message:
                        print("test")
                        continue
                    is_valid, extra = valid_order_for_messages(prev_message, msg)
                    if not is_valid:
                        print("Invalid order")
                        with open(smt_crash_log, "a+") as file:
                            file.write(
                                f"{'-' * 53}\n"
                                f"------ Invalid order detected or missing TLV! -------\n"
                                f"{'-' * 53}\n"
                                f'[{datetime.now().isoformat()}] \n'
                                f"{prev_message.__str__()}\n"
                                f"\n====resulted in===== \{msg.__str__()}\n"
                                f"extra info: {extra}\n"
                            )

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

    init_log(log)
    init_log(smt_crash_log)

    print("Id of this device is: ", id)
    print("Listen port is: ", listenport)
    print("Aflnet local port is:", port)
    openthreadthread = threading.Thread(target=openthread)
    thread = threading.Thread(target=communication_OT, args=(port,))
    thread.start()
    openthreadthread.start()
    communication_aflnet(listenport)


if __name__ == '__main__':
    _main()
