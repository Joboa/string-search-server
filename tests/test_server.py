"""Unit test for server.py"""

import pytest
import socket
import threading
import time
import server

from unittest.mock import Mock, patch, MagicMock

from server import (
    start_server,
    stop_server,
    PAYLOAD_SIZE,
    execute_search_query,
    DATA_FORMAT,
    handle_client,
)
from file_handling import text_file_path, strings_list

SOCK_ADDRESS = ("localhost", 8871)
addr, port = SOCK_ADDRESS


@pytest.fixture(scope="module")
def server_socket():
    """Server socket.

    It creates a socket, starts a server in a separate thread, waits
    for the server to start listening for connections, and then yields
    the socket to the test
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(SOCK_ADDRESS)
    sock.listen()

    # Start the server in a separate thread.
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()

    time.sleep(0.1)
    yield sock
    stop_server()
    sock.close()


@pytest.fixture
def mock_conn():
    return MagicMock(name="socket.socket")


@pytest.fixture(scope="module")
def get_catched_data():
    file_path = text_file_path("configs.ini")
    cached_data = strings_list(file_path)
    yield cached_data


def test_server_socket_creation():
    """Test server socket creation.

    It creates a socket, binds it to a local address, and then listens
    for incoming connections
    """
    SOCK_ADDRESS = ("127.0.0.1", 8000)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(SOCK_ADDRESS)
    server_sock.listen()

    # Check that the socket is valid and bound to the expected address
    assert server_sock.fileno() != -1
    assert server_sock.getsockname() == SOCK_ADDRESS


def test_accepts_connections(server_socket):
    """Test server connections.

    It creates a client socket, connects it to the server socket,
    and then checks that the server socket accepted the connection

    :param server_socket: The socket that the server is listening on
    """
    # Connect to the server socket.
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(SOCK_ADDRESS)

    # Check that the server accepted the connection.
    conn, addr = server_socket.accept()
    assert addr == client_sock.getsockname()
    client_sock.close()


def test_execute_search_query_with_string_exists():
    """Test execute search query with string exists.

    It takes a string, an IP address, a connection, and some cached data,
    and sends the connection a response based on whether the string exists
    in the cached data
    """
    data = "3;0;1;28;0;23;4;0;"
    conn = Mock()

    execute_search_query(data, addr, conn)
    expected_response = "STRING EXISTS\n"
    conn.send.assert_called_once_with(expected_response.encode(DATA_FORMAT))


def test_execute_search_query_with_string_exists_with_cache():
    """Test execute search query with cache data.

    It takes a string, an IP address, a connection, and some cached data,
    and sends the connection a response based on whether the string exists
    in the cached data
    """
    cached_data = None
    data = "3;0;1;28;0;23;4;0;"
    conn = Mock()

    execute_search_query(data, addr, conn, cached_data=None)
    expected_response = "STRING EXISTS\n"
    conn.send.assert_called_once_with(expected_response.encode(DATA_FORMAT))


def test_execute_search_query_with_string_not_found():
    """Test execute search query with string not found.

    It takes a string and a connection object, and sends a response to
    the connection object
    """
    data = "foo"
    conn = Mock()

    execute_search_query(data, addr, conn)
    expected_response = "STRING NOT FOUND\n"
    conn.send.assert_called_once_with(expected_response.encode(DATA_FORMAT))


def test_handle_client_with_data_reread_on_query(mock_conn):
    """Test handle client with reread on query.

    It tests that the function `handle_client` calls `execute_search_query`
    with the correct arguments when the `REREAD_ON_QUERY` flag is set to `True`

    :param mock_conn: a mock object that represents the
    connection to the client
    """
    with patch("server.execute_search_query") as mock_execute_search_query:
        data = "foo"
        mock_conn.recv.return_value.decode.return_value = data
        mock_conn.recv.return_value.decode.return_value += "\x00" * (
            PAYLOAD_SIZE - len(data)
        )

        with patch("server.REREAD_ON_QUERY", True):
            handle_client(mock_conn, ("localhost", 5051))
        mock_execute_search_query.assert_called_once_with(
            data, ("localhost", 5051), mock_conn
        )


def test_handle_client_with_cached_data(
        mock_conn, get_catched_data,
        monkeypatch
):
    """Test handle client with cached data.

    It tests that the function handle_client calls
    execute_search_query with cached data

    :param mock_conn: a mock object that represents the connection
    to the client
    :param get_catched_data: a list of strings
    :param monkeypatch: a fixture that allows you to replace a
    function with a mock
    """
    mock_conn.recv.return_value.decode.return_value = "foo"
    mock_conn.recv.return_value.decode.return_value += "\x00" * (
        PAYLOAD_SIZE - len("foo")
    )

    def execute_search_query_mock(data, addr, conn, cached_data=None):
        assert cached_data == expected_cached_data
        assert data == "foo"

    expected_cached_data = get_catched_data
    with monkeypatch.context() as m:
        m.setattr(server, "execute_search_query", execute_search_query_mock)
        m.setattr(server, "text_file_path", lambda _: "")
        m.setattr(server, "strings_list", lambda _: expected_cached_data)
        handle_client(mock_conn, ("localhost", 5051))


def test_handle_client_with_empty_data(mock_conn):
    """Test handle client with empty data.

    It tests that when the client sends an empty string, the
    server sends an empty string back

    :param mock_conn: the mock object that will be passed to the function
    """
    mock_conn.recv.return_value.decode.return_value = ""
    handle_client(mock_conn, ("localhost", 5051))
    assert mock_conn.recv.call_count == 1
    assert mock_conn.send.called_once_with("".encode(DATA_FORMAT))


def test_handle_client_with_invalid_data(mock_conn):
    """Test handle client with invalid data.

    It tests that the server sends the correct error message when
    the client sends a message that is too long

    :param mock_conn: a mock object that represents the connection
    to the client
    """
    mock_conn.recv.return_value.decode.return_value = "a" * 2048
    handle_client(mock_conn, ("localhost", 5051))
    assert mock_conn.recv.call_count == 1
    assert mock_conn.send.called_once_with(
        "PAYLOAD SIZE EXCEEDED\n".encode(DATA_FORMAT)
    )
