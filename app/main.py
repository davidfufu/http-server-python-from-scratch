# Uncomment this to pass the first stage
import socket
import threading
import argparse
import os

CRLF = "\r\n"
HTTP_VERSION = "HTTP/1.1"
HTTP_202_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"


def parseHeaders(headers: list) -> dict:
    parsedHeaders = {}

    for header in headers:
        if header == "":
            continue
        hName, hValue = header.split(": ")
        parsedHeaders[hName] = hValue

    return parsedHeaders


#  {#8b9,29}
def parseHttpRequest(data: bytearray) -> dict:
    parsedRequestArgs = {}

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

    parsedRequestArgs["method"] = method
    parsedRequestArgs["path"] = path
    parsedRequestArgs["version"] = version
    parsedRequestArgs["headers"] = parseHeaders(headers)

    # print(parsedRequestArgs)

    return parsedRequestArgs


#  {#2d9,14}
def getResponseStatus(path: str) -> str:
    response_status = ""
    if "echo" in path:
        response_status = "200 OK"
        return response_status

    match path:
        case "/":
            response_status = "200 OK"
        case _:
            response_status = "404 Not Found"

    return response_status


#  {#ed9,3}
def getRandomString(path: str) -> str:
    randomString = path.split("/echo/")[-1]
    return randomString


#  {#53f,17}
def handleNewConnection(client_connection):
    data: bytearray = client_connection.recv(1024)

    if not data:
        return

    allParsedArgs = parseHttpRequest(data)

    response_status = getResponseStatus(allParsedArgs["path"])

    randomString = getRandomString(allParsedArgs["path"])
    HEADERS = f"Content-Type: text/plain\nContent-Length: {len(randomString)}"
    http_response = f"{HTTP_VERSION} {response_status}{CRLF}{CRLF}"

    if "echo" in allParsedArgs["path"]:

        randomString = getRandomString(allParsedArgs["path"])
        HEADERS = f"Content-Type: text/plain\nContent-Length: {len(randomString)}"
        http_response = (
            f"{HTTP_VERSION} {response_status}{CRLF}{HEADERS}{CRLF}\n{randomString}"
        )

    elif "user-agent" in allParsedArgs["path"]:

        userAgent = allParsedArgs["headers"]["User-Agent"]
        HEADERS = f"Content-Type: text/plain\nContent-Length: {len(userAgent)}"
        http_response = (
            f"{HTTP_VERSION} {response_status}{CRLF}{HEADERS}{CRLF}\n{userAgent}"
        )

    elif "files" in allParsedArgs["path"]:
        fileName = allParsedArgs["path"].split("files/")[-1]
        filePath = os.path.join(file_directory, fileName)

        response_status = ""

        if os.path.exists(filePath):
            response_status = "200 OK"
        else:
            response_status = "404 Not Found"

        HEADERS = "Content-Type: text/plain"
        http_response = f"{HTTP_VERSION} {response_status}{CRLF}{HEADERS}{CRLF}"

    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()


#  {#6b1,13}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str)
    args = parser.parse_args()
    global file_directory
    file_directory = args.directory

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    host = "localhost"
    port = 4221
    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server((host, port), reuse_port=True)

    while True:
        conn, addr = server_socket.accept()  # wait for client
        thread = threading.Thread(target=handleNewConnection, args=(conn,))
        thread.start()


if __name__ == "__main__":
    main()
