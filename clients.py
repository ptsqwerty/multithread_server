import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 12344
client_list = []
active_client = None

def thread_for_client():
    global active_client
    while True:
        user_input = input(
            "Введите сообщение для сервера (или 'change' для смены клиента, 'quit' для выхода): ")
        if user_input == 'quit':
            break
        elif user_input == 'change':
            active_client = change_active_client()
            continue
        active_client.sendall(user_input.encode())
        server_response = active_client.recv(1024)
        print('Ответ сервера:', server_response.decode())
    active_client.close()

def change_active_client():
    print("Список доступных клиентов:")
    for index, client in enumerate(client_list):
        print(f"{index + 1}: {client}")
    while True:
        selected_client = input("Введите номер клиента, которого хотите выбрать: ")
        if selected_client.isdigit() and 0 < int(selected_client) <= len(client_list):
            return client_list[int(selected_client) - 1]
        else:
            print("Неверный ввод. Пожалуйста, введите номер доступного клиента.")

def main():
    global active_client
    client_count = int(input("Введите количество клиентов: "))

    for _ in range(client_count):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_list.append(client_socket)
    active_client = client_list[0]
    client_thread = threading.Thread(target=thread_for_client)
    client_thread.start()

    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

if __name__ == "__main__":
    main()
