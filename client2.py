import socket
import threading
import os

# def receive_message(sock):
#     while True:
#         message = sock.recv(1024).decode()
#         print(message)
#
# def main():
#
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('localhost', 12345)
#     client_socket.connect(server_address)
#
#     threading.Thread(target=receive_message, args=(client_socket,), daemon=True).start()
#
#     while True:
#         message = input()
#         client_socket.send(message.encode())
#
# if __name__ == "__main__":
#     main()
# # Завдання 2

# SERVER_HOST = "localhost"
# SERVER_PORT = 12345
# BUFFER_SIZE = 4096
#
#
# def send_file(client_socket, file_name):
#     # Відправлення команди про надіслання файлу
#     client_socket.sendall("send".encode())
#
#     # Надсилання інформації про файл
#     client_socket.sendall(file_name.encode())
#     file_size = os.path.getsize(file_name)
#     client_socket.sendall(str(file_size).encode())
#
#     # Надсилання файлу блоками даних
#     with open(file_name, "rb") as f:
#         while True:
#             data = f.read(BUFFER_SIZE)
#             if not data:
#                 break
#             client_socket.sendall(data)
#
#     print("File sent successfully.")
#
#
# def receive_file(client_socket):
#     # Відправлення команди про отримання файлу
#     client_socket.sendall("receive".encode())
#
#     # Очікування підтвердження від сервера про успішне прийняття файлу
#     confirmation = client_socket.recv(BUFFER_SIZE).decode().strip()
#     print("Server:", confirmation)
#
#     if confirmation.lower() == "ready to receive file. send now.":
#         # Відправлення підтвердження про успішне отримання файлу на сервер
#         client_socket.sendall("OK".encode())
#
#         # Отримання інформації про файл
#         file_name = client_socket.recv(BUFFER_SIZE).decode().strip()
#         file_size = int(client_socket.recv(BUFFER_SIZE).decode().strip())
#
#         # Отримання файлу
#         print(f"Receiving file '{file_name}'...")
#         with open(file_name, "wb") as f:
#             remaining_bytes = file_size
#             while remaining_bytes > 0:
#                 data = client_socket.recv(min(BUFFER_SIZE, remaining_bytes))
#                 f.write(data)
#                 remaining_bytes -= len(data)
#         print("File received successfully.")
#
#
#
# def main():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((SERVER_HOST, SERVER_PORT))
#
#     while True:
#         choice = input("Choose an option (send/receive/exit): ").strip().lower()
#
#         if choice == "send":
#             file_name = input("Enter the name of the file to send: ").strip()
#             if os.path.exists(file_name):
#                 send_file(client_socket, file_name)
#             else:
#                 print("File not found.")
#         elif choice == "receive":
#             receive_file(client_socket)
#         elif choice == "exit":
#             break
#         else:
#             print("Invalid option.")
#
#     client_socket.close()
#
#
# if __name__ == "__main__":
#     main()
# Завдання 3

# Параметри сервера
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
BUFFER_SIZE = 1024

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode()
            print(message)
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        client_socket.sendall(username.encode())
        client_socket.sendall(password.encode())

        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)

        if response == "Welcome to the chat!":
            print("You are now connected to the chat. Type 'exit' to quit.")
            receiving_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receiving_thread.start()

            while True:
                message = input("You: ")
                client_socket.sendall(message.encode())
                if message.lower() == "exit":
                    break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
