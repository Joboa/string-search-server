"""Unit test for client.py"""

import pytest
import socket

from unittest.mock import MagicMock, patch
from client import send_request, PAYLOAD_SIZE, DATA_FORMAT


@pytest.fixture
def mock_socket():
    """Mock socket.

    It creates a mock socket object, and passes it to the
    function that you're testing
    """
    with MagicMock(spec=socket.socket) as mock_socket:
        yield mock_socket


def test_send_request_socket_error(mock_socket):
    """Test socket error.

    It takes a string, converts it to bytes, and sends it to a server

    :param mock_socket: the name of the fixture
    """
    with patch("socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = socket.error
        with pytest.raises(SystemExit):
            send_request("3;0;1;28;0;23;4;0;")


def test_send_request_socket_timeout():
    """Test socket timeout.

    It creates a mock socket object, sets the recv method to
    raise a socket.timeout exception, and the calls the
    send_request function
    """
    with patch("socket.socket") as mock_socket:
        mock_socket.return_value.recv.side_effect = socket.timeout
        with pytest.raises(SystemExit):
            send_request("3;0;1;28;0;23;4;0;")


def test_send_request_string_not_found(mock_socket):
    """Test string not found request.

    It creates a mock socket object, sets the return value of the
    recv method to a string, and then calls the send_request
    function with a string as an argument

    :param mock_socket: a mock object that is used to replace the
    socket.socket object
    """
    mock_socket.recv.return_value = "STRING NOT FOUND\n".encode(DATA_FORMAT)
    query = "3;0;1;28;0;23;4;0;"
    with patch.object(socket, "socket", return_value=mock_socket):
        send_request(query)
    mock_socket.connect.assert_called_once()
    mock_socket.send.assert_called_once_with(query.encode(DATA_FORMAT))
    mock_socket.recv.assert_called_once_with(PAYLOAD_SIZE)
    mock_socket.close.assert_called_once()


def test_send_request_string_exists(mock_socket):
    """Test string exists request.

    It creates a mock socket object, sets the return value of the
    recv method to a string, and then calls the send_request function
    with a string as an argument

    :param mock_socket: a mock object that is used to replace the
    socket.socket object
    """
    mock_socket.recv.return_value = "STRING EXISTS\n".encode(DATA_FORMAT)
    with patch.object(socket, "socket", return_value=mock_socket):
        send_request("test_query")
    mock_socket.connect.assert_called_once()
    mock_socket.send.assert_called_once_with("test_query".encode(DATA_FORMAT))
    mock_socket.recv.assert_called_once_with(PAYLOAD_SIZE)
    mock_socket.close.assert_called_once()


def test_send_request_socket_connection_error():
    """Test socket connection error.

    It creates a mock socket object, sets the side effect of the connect
    method to raise a ConnectionRefusedError, and then asserts that the
    send_request function raises a SystemExit exception
    """
    with patch("socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = ConnectionRefusedError
        with pytest.raises(SystemExit):
            send_request("3;0;1;28;0;23;4;0;")
