# Uncomment this to pass the first stage
import socket

CRLF = "\r\n"
HTTP_VERSION = "HTTP/1.1"
HTTP_202_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"

def parseHttpRequest(data: bytearray) -> tuple[str, str, str]:
    split_request_data = data.decode("utf-8").split("\r\n")


    requestLine = split_request_data[0]
    headers = split_request_data[1:-2]
    body = split_request_data[-1]

    # print(f"REQUEST_LINE: {requestLine}")
    # print(f"HEADERS: {headers}")
    # print(f"BODY: {body}")

    partition = requestLine.split()

    if len(partition) != 3:
        raise ValueError(requestLine)
    
    method, path, version = partition
    return method, path, version


def getResponseStatus(path: str) -> str:
    response_status = ""

    match path:
        case "/":
            response_status = "200 OK"
        case _:
            response_status = "404 Not Found"

    return response_status

def handleNewConnection(client_connection):
    data: bytearray = client_connection.recv(1024)

    if not data:
        return

    method, path, version = parseHttpRequest(data)

    response_status = getResponseStatus(path)

    http_response = f"{HTTP_VERSION} {response_status}{CRLF}{CRLF}"

    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()



def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    host = "localhost"
    port = 4221
    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server((host, port), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        handleNewConnection(conn)




if __name__ == "__main__":
    main()
