import socket
from _thread import start_new_thread

server = "192.168.29.184"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started...")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])  # str to tuple


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])  # tuple to str


pos = [(0, 0), (100, 100)]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    while True:
        try:
            # receive position from player
            data = read_pos(conn.recv(2048 * 8).decode())

            if not data:
                print("Disconnected")
                break
            else:
                # update position with the received values
                pos[player] = data

                # send the other player's position to client
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received : ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except socket.error as e:
            print(e)
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
