import socket
from _thread import start_new_thread
from player import Player
import pickle

server = "192.168.29.184"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started...")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            # receive player from client
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                # update stored player with the received player
                players[player] = data

                # send the other player to client
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received : ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))

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
