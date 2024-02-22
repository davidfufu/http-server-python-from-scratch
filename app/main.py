# Uncomment this to pass the first stage
import socket

HTTP_202_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    host = "localhost"
    port = 4221
    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server((host, port), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    conn.recv(4096)

    with conn:
        conn.sendall(HTTP_202_RESPONSE)




if __name__ == "__main__":
    main()
