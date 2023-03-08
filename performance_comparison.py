"""Performance comparison script."""

import configparser
import datetime

from client import send_request


# Reading the configs.ini file and assigning the values
# to the variables.
config_data = configparser.ConfigParser()
config_data.read("configs.ini")

# Reading the configs.ini file and assigning the values
# to the variables.
file_path = config_data["text_file"]["windows_path"]


def get_query_statistics(query, algorithm_name, file_path):
    """Get query statistics of search algorithm.

    This function takes in a query, an algorithm name, and a file
    path to a text file. It then writes the query statistics to a
    text file

    :param query: the query string
    :param algorithm_name: The name of the algorithm you want to use
    :param file_path: This is the path to the file that contains the
    list of queries

    EXAMPLE: get_single_query('foo', BINARY, file_path_to_text_file),
    get_single_query('bar', LINEAR,file_path_to_text_file)
    """
    with open(algorithm_name + "_query_" + "statistics.txt", "w") as f:
        f.write("-------BENCHMARK STATISTICS FOR SEARCH ALGORITHMS--------\n")
        f.write(f"------------------ {algorithm_name} SEARCH --------------\n")
        f.write("\n\n")

        # for single query
        f.write("-------------------- SINGLE QUERY ------------------\n")
        f.write("\n")
        start_time = datetime.datetime.now()
        f.write(f"START TIME: {start_time}\n")
        send_request(query)
        end_time = datetime.datetime.now()
        f.write(f"END TIME: {end_time}\n")
        f.write(f"Total time (s): {(end_time - start_time).total_seconds()}\n")
        f.write("\n")
        f.write(f"--Single query completed for {algorithm_name} search--\n")

        # For 1000 queries
        with open(file_path, "r") as fr:
            f.write("\n\n")
            f.write("---------------- 100 QUERIES ---------------------\n")
            all_strings = fr.readlines()
            start_time = datetime.datetime.now()
            f.write(f"START TIME: {start_time}\n")
            count = 0
            for str in all_strings:
                str = str.strip()
                send_request(str)
                count += 1
                print(count)
                if count > 99:
                    break
            end_time = datetime.datetime.now()
            f.write(f"Total queries: {count}\n")
            f.write(f"END TIME: {end_time}\n")
            time_results = (end_time - start_time).total_seconds()
            f.write(f"Total execution time (s): {time_results}\n")
            f.write(f"Average exec time per query (s): {time_results/count}\n")
            f.write("\n")
            f.write(f"{count} queries completed for {algorithm_name} search\n")


if __name__ == "__main__":
    get_query_statistics("2;3;12;29;13;3;19;22;", "BINARY", file_path=file_path)
