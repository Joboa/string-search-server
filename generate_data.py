"""Generate data script."""

import configparser
import random


# Reading the configs.ini file and assigning the values
# to the variables.
config_data = configparser.ConfigParser()
config_data.read("configs.ini")

# Reading the configs.ini file and assigning the values
# to the variables.
file_path = config_data["text_file"]["windows_path"]


def write_to_file(file_path):
    """Write to file.

    It reads all the lines from the file at the given path, and
    writes the first 100,000 lines to a new file called d100k.txt

    :param file_path: The path to the file you want to read from
    """
    with open(file_path, "r") as fr:
        with open("d100.txt", "w") as fw:
            all_strings = fr.readlines()
            count = 0
            for str in all_strings:
                fw.write(str)
                count += 1
                if count > 99:
                    break


def generate_random_ips():
    """Generate random ips.

    It generates a million random IP addresses and writes
    them to a file called d1M.txt
    """
    with open("d1M.txt", "w") as f:
        for i in range(0, 1000000):
            col = ";"
            ip = (
                str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
                + str(random.randint(0, 30))
                + col
            )
            f.write(ip + "\n")

if __name__ == "__main__":
    write_to_file(file_path=file_path)