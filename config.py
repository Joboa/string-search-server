"""Configuration script file."""

import configparser
import socket

config = configparser.ConfigParser()

# creating a section for the address
config.add_section("socket_info")

# adding key-value pairs
HOST = socket.gethostbyname(socket.gethostname())
config.set("socket_info", "HOST", HOST)
config.set("socket_info", "PORT", "5052")
config.set("socket_info", "PAYLOAD_SIZE", "1024")
config.set("socket_info", "DATA_FORMAT", "utf-8")

# creating a section for the address
config.add_section("text_file")
config.set(
    "text_file",
    "windows_path",
    "C:\\Users\\johna\\Documents\\windsor-code\\string-search-server\\d100.txt",
)

# creating a section for query on reread
config.add_section("query_file")
config.set("query_file", "REREAD_ON_QUERY", "")


with open("configs.ini", "w") as configs:
    config.write(configs)
