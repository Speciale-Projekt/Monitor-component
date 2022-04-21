import socket
import inotify.adapters
import pathlib
import os

# First we should op en a file and read the content
# Then we should send the content via UDP to the server
ip = "127.0.0.1"
port = 4000
filename = pathlib.Path("/home/agw/test/out.txt")

# if the file is written to, then we should


def _main():
    i = inotify.adapters.Inotify()
    if not os.path.isfile(filename):
        with open(filename, "w+") as f:
            pass
    # open the file and read the content
    i.add_watch(filename.__str__())
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, _) = event
        print(event)
        if "IN_CLOSE_WRITE" in type_names or "IN_MOVE_SELF" in type_names:
            # Read file, its in binary format
            with open(filename, "rb") as f:
                sock = socket.socket(socket.AF_INET,
                                     socket.SOCK_DGRAM)
                sock.sendto(f.read(), (ip, port))
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
                    pass# remove old watch, and add new watch to same file


if __name__ == '__main__':
    _main()
