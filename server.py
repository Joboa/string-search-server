"""Server to handle client requests."""

import configparser
import socket
import sys
import datetime

# Importing the ThreadPoolExecutor class from the
# concurrent.futures modulE
from concurrent.futures import ThreadPoolExecutor
from file_handling import text_file_path, search_for_string, strings_list

# Reading the configs.ini file and assigning the
# values to the variables.
config_data = configparser.ConfigParser()
config_data.read("configs.ini")

# Reading the configs.ini file and assigning the
# values to the variables.
DATA_FORMAT = config_data["socket_info"]["DATA_FORMAT"]
PAYLOAD_SIZE = int(config_data["socket_info"]["PAYLOAD_SIZE"])
HOST = config_data["socket_info"]["HOST"]
PORT = int(config_data["socket_info"]["PORT"])
REREAD_ON_QUERY = bool(config_data["query_file"]["REREAD_ON_QUERY"])

SOCK_ADDRESS = (HOST, PORT)
MAX_WORKERS = 4


# Creating a socket object and binding it to the address.
try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(SOCK_ADDRESS)
    server_sock.listen()
except socket.error as err:
    print(f"Error creating socket: {err}")
    sys.exit(1)


def start_server():
    """Start the server.

    It starts the server and listens for connections.
    """
    print(f"Starting server ...")
    print(f"Server listening on {HOST}:{PORT}")
    print(f"Use CTRL + C to end operation")
    print("-------------------------------------------------------")

    # Creating a thread pool executor with a maximum of 4 workers.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            try:
                # It accepts a connection from a client.
                conn, addr = server_sock.accept()
                # Submitting the handle_client function to the
                # thread pool executor.
                executor.submit(handle_client, conn, addr)
            except socket.error as err:
                print(f"Error accepting connection: {err}")
            except KeyboardInterrupt:
                print("Shutting down server...")
                break


def execute_search_query(data, addr, conn, cached_data=None):
    """Execute search query.

    It searches for a string in a file and returns the result to
    the client

    :param data: The string to search for
    :param addr: The IP address of the client
    :param conn: The connection object
    :param cached_data: The data to search in. If it's None, then
    the data is read from the file
    """
    # Getting the file path for the search data
    file_path = text_file_path("configs.ini") if cached_data is None else None

    start_time = datetime.datetime.now()
    found = search_for_string(cached_data or file_path, data)
    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    # Response from the server to the client for search query
    response = "STRING EXISTS\n" if found else "STRING NOT FOUND\n"
    conn.send(response.encode(DATA_FORMAT))
    print(
        f"DEBUG: Search query: {data}, IP: {addr},\n"
        f"Exec.time: {execution_time}s, Timestamp: {datetime.datetime.now()}\n"
    )


def handle_client(conn, addr):
    """Handle client requests.

    It receives a message from the client, and if the message is not
    empty, it sends a message back to
    the client.

    :param conn: the socket object
    :param addr: ("127.0.0.1", 5051)
    """
    print(f"Creating new connection...")
    with conn:
        print(f"Connection established for {addr}")

        # Assigning the value of None to the variable cached_data.
        cached_data = None
        while True:
            data = conn.recv(PAYLOAD_SIZE).decode(DATA_FORMAT).rstrip("\x00")
            if len(data) > PAYLOAD_SIZE:
                print(f"Buffer size exceeded and cannot process data")
                conn.send("PAYLOAD SIZE EXCEEDED\n".encode(DATA_FORMAT))
                break
            if data:
                # A flag that is used to determine whether the data should be
                # read from the file every time a search query is made or not.
                if REREAD_ON_QUERY:
                    execute_search_query(data, addr, conn)
                    break
                else:
                    if cached_data is None:
                        file_path = text_file_path("configs.ini")
                        cached_data = strings_list(file_path)
                    execute_search_query(data, addr, conn, cached_data)
                    break
            else:
                break
        print(f"Connection closed for {addr}")
        print("-------------------------------------------------------")


def stop_server():
    """Stop server.

    It closes the server socket
    """
    server_sock.close()


if __name__ == "__main__":
    start_server()
