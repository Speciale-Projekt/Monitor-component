ip = "0.0.0.0"

def proxy(listenport, servport):
    aflnet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aflnet.bind((ip, listenport))

    ot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data, addr = aflnet.recvfrom(1024)  # buffer size is 1024 bytes
        print(data)
        ot.sendto(data, (ip, servport))


id = int(sys.argv[1])
print(id)
listenport = 9000 + id
servport = 5000 + id

proxy(listenport,servport)