import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12344

def client_handler(connection, client_address):
    print('Новое подключение от клиента:', client_address)
    with connection:
        while True:
            received_data = connection.recv(1024)
            if not received_data:
                break
            print(f'Клиент {client_address} прислал: {received_data.decode()}')
            connection.sendall(received_data)
            print(f'Ответ клиенту {client_address} отправлен: {received_data.decode()}')

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()

        print("Сервер успешно запущен...")

        while True:
            connection, client_address = server_socket.accept()
            new_thread = threading.Thread(target=client_handler, args=(connection, client_address))
            new_thread.start()

if __name__ == "__main__":
    run_server()
