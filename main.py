import socket
import threading
import random
import os

# def display_board(board):
#     for row in board:
#         print(" | ".join(row))
#         print("--" * 5)
#     print()
#
#
# def check_winner(board, symbol):
#     for i in range(3):
#         if all(cell == symbol for cell in board[i]) or all(board[j][i] == symbol for j in range(3)):
#             return True
#
#     if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
#         return True
#
#     return False
#
#
# def start_game(clients):
#     symbols = ['X', 'O']
#     random.shuffle(symbols)
#     symbols_dict = {0: symbols[0], 1: symbols[1]}
#
#     board = [[' ' for _ in range(3)] for _ in range(3)]
#     display_board(board)
#     current_player = 0
#
#     for i, (client_socket, _) in enumerate(clients):
#         symbol = symbols_dict[i]
#         client_socket.sendall(f"You are playing as '{symbol}'\n".encode())
#
#     while True:
#         client_socket = clients[current_player][0]
#         client_socket.sendall("Your move: ".encode())
#         move = client_socket.recv(1024).decode()
#         row, col = map(int, move.split())
#         if move == "quit":
#             print("Game stopped. Player", current_player + 1, "has quit.")
#             other_player_socket = clients[1 - current_player][0]
#             other_player_socket.sendall("Your opponent has quit. You win!".encode())
#             break
#
#
#         if board[row][col] == ' ':
#             symbol = 'X' if current_player == 0 else 'O'
#             board[row][col] = symbol
#
#             if check_winner(board, symbol):
#                 display_board(board)
#                 client_socket.sendall("You win!".encode())
#                 other_player_socket = clients[1 - current_player][0]
#                 other_player_socket.sendall("You lose!".encode())
#                 break
#
#             if all(cell != ' ' for row in board for cell in row):
#                 display_board(board)
#                 client_socket.sendall("It's a draw!".encode())
#                 other_player_socket = clients[1 - current_player][0]
#                 other_player_socket.sendall("It's a draw!".encode())
#                 break
#
#             for i, player_socket in enumerate(clients):
#                 player_socket[0].sendall("Current board state:\n".encode())
#                 for row in board:
#                     row_str = "|".join(row)
#                     player_socket[0].sendall((row_str + "\n").encode())
#
#                 if i == current_player:
#                     player_socket[0].sendall("Your move: ".encode())
#                 else:
#                     player_socket[0].sendall("Opponent's move. Please wait...".encode())
#
#             current_player = 1 - current_player
#
#             display_board(board)
#
#
#
# def handle_client(client_socket, player_id, clients, players_ready):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             if message == "start":
#                 players_ready[player_id - 1] = True
#                 if all(players_ready):
#                     start_game(clients)
#                     print("Both players are ready. Starting the game.")
#                     break
#             elif message == "quit":
#                 print("Player", player_id, "quit the game.")
#                 break
#         except ConnectionResetError:
#             print("Player", player_id, "disconnected.")
#             break
#     client_socket.close()
#
#
# def main():
#     global players_ready
#
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(("localhost", 12345))
#     server_socket.listen(2)
#
#     clients = []
#     players_ready = [False, False]
#
#     print("Waiting for players...")
#     while len(clients) < 2:
#         client_socket, _ = server_socket.accept()
#         clients.append((client_socket, threading.Event()))
#         print("Player connected.")
#
#     threads = []
#     for i, (client_socket, event) in enumerate(clients):
#         thread = threading.Thread(target=lambda: handle_client(client_socket, i + 1, clients, players_ready))
#         thread.start()
#         threads.append(thread)
#
#     for thread in threads:
#         thread.join()
#
#     server_socket.close()
#
#
# if __name__ == "__main__":
#     main()
# # Завдання 2
# SERVER_HOST = "0.0.0.0"
# SERVER_PORT = 12345
# BUFFER_SIZE = 4096
#
#
# def handle_client(client_socket, client_id, clients):
#     print(f"Connected with client {client_id}")
#
#     while True:
#         try:
#             # Отримання команди від клієнта
#             command = client_socket.recv(BUFFER_SIZE).decode().strip()
#
#             if command == "send":
#                 # Отримання інформації про файл від клієнта
#                 file_name = client_socket.recv(BUFFER_SIZE).decode().strip()
#                 file_size = int(client_socket.recv(BUFFER_SIZE).decode().strip())
#                 if os.path.exists(file_name):
#                     # file_size = os.path.getsize(file_name)
#
#                     # Надсилання запиту іншому клієнту про готовність прийняти файл
#                     other_client_socket = clients[1 - client_id]
#                     other_client_socket.sendall("ready to receive file. send now.".encode())
#
#                     # Очікування підтвердження від іншого клієнта
#                     confirmation = other_client_socket.recv(BUFFER_SIZE).decode().strip()
#                     if confirmation.lower() == "ok":
#
#                         # Отримання файлу
#                         print(f"Receiving file '{file_name}'...")
#                         with open(file_name, "wb") as f:
#                             remaining_bytes = file_size
#                             while remaining_bytes > 0:
#                                 data = client_socket.recv(min(BUFFER_SIZE, remaining_bytes))
#                                 f.write(data)
#                                 remaining_bytes -= len(data)
#                         print("File received successfully.")
#
#             elif command == "receive":
#                 # Відправлення запиту на отримання файлу іншому клієнту
#                 other_client_socket = clients[1 - client_id]
#                 other_client_socket.sendall("receive".encode())
#
#                 # Отримання інформації про файл від іншого клієнта
#                 file_name = other_client_socket.recv(BUFFER_SIZE).decode().strip()
#                 file_size = int(other_client_socket.recv(BUFFER_SIZE).decode().strip())
#
#                 print(f"Sending file '{file_name}' to client {1 + client_id}")
#                 other_client_socket.sendall(file_name.encode())
#                 other_client_socket.sendall(str(file_size).encode())
#
#                 # Надсилання файлу блоками даних
#                 remaining_bytes = file_size
#                 while remaining_bytes > 0:
#                     data = client_socket.recv(min(BUFFER_SIZE, remaining_bytes))
#                     other_client_socket.sendall(data)
#                     remaining_bytes -= len(data)
#
#                     print("File sent successfully.")
#                 else:
#                     print("File transmission canceled.")
#
#
#
#             elif command == "quit":
#                 print(f"Client {client_id} quit the game.")
#                 break
#
#             else:
#                 # Невідома команда
#                 client_socket.sendall("Unknown command.".encode())
#         except Exception as e:
#             print(f"Error: {e}")
#             break
#
#     client_socket.close()
#     print(f"Connection with client {client_id} closed")
#
#
# def main():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((SERVER_HOST, SERVER_PORT))
#     server_socket.listen(2)
#     print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
#
#     clients = [None, None]
#
#     try:
#         client_id = 0
#         while True:
#             client_socket, _ = server_socket.accept()
#             clients[client_id] = client_socket
#
#             client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id, clients))
#             client_thread.start()
#
#             client_id += 1
#             if client_id == 2:
#                 break
#     except KeyboardInterrupt:
#         print("Server shutting down.")
#     finally:
#         server_socket.close()
#
#
# if __name__ == "__main__":
#     main()
# # Завдання 3

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5555
BUFFER_SIZE = 1024

users = {
    "Vlad": "111",
    "Vlad1": "222"
}

connected_clients = []

def handle_client(client_socket, username):
    print(f"Connected with {username}")
    connected_clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            if message.lower() == "exit":
                print(f"{username} disconnected.")
                break
            broadcast_message(f"{username}: {message}")
    except Exception as e:
        print(f"Error handling client {username}: {e}")
    finally:
        client_socket.close()
        connected_clients.remove(client_socket)

def broadcast_message(message):
    for client_socket in connected_clients:
        try:
            client_socket.sendall(message.encode())
        except Exception as e:
            print(f"Error broadcasting message to a client: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            username = client_socket.recv(BUFFER_SIZE).decode()
            password = client_socket.recv(BUFFER_SIZE).decode()

            if username in users and users[username] == password:
                client_socket.sendall("Welcome to the chat!".encode())
                client_thread = threading.Thread(target=handle_client, args=(client_socket, username))
                client_thread.start()
            else:
                client_socket.sendall("Invalid username or password. Connection closed.".encode())
                client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
