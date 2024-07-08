#!/usr/bin/env python

import csv
import logging
import re
from getpass import getpass

from elasticsearch import Elasticsearch
from rich import print
from rich.logging import RichHandler

from get_es_index_sizes.config.env import (
    DEFAULT_TZ,
    ES_API_KEY,
    ES_CLOUD_ID,
    ES_PASS,
    ES_URL,
    ES_USER,
    LOG_LEVEL,
    OUTPUT_DIR,
)


def create_es_client(
    es_url: str = None, es_id: str = None, api_key: str = None, auth: tuple = None
) -> Elasticsearch:
    """
    Create an Elasticsearch client instance.

    Args:
    es_url (str): URL of the Elasticsearch instance.
    es_id (str): Cloud ID of the Elasticsearch instance.
    api_key (str): API key for Elasticsearch authentication.
    auth (tuple): Username and password tuple for Elasticsearch authentication.

    Returns:
    Elasticsearch: The Elasticsearch client instance.
    """

    if es_url and es_id:
        raise ValueError(
            "Both es_url and es_id cannot be provided together. Choose one."
        )
    if api_key and auth:
        raise ValueError(
            "Both api_key and auth cannot be provided together. Choose one."
        )

    client_params = {}
    if es_url:
        client_params["hosts"] = [es_url]
    if es_id:
        client_params["cloud_id"] = es_id
    if api_key:
        client_params["api_key"] = api_key
    if auth:
        client_params["basic_auth"] = auth

    return Elasticsearch(**client_params)
    # return requests.get(f"{es_url}/_cat/indices?v", auth=auth_param, headers=headers)


def parse_size(size_str: str):
    """
    Convert a size string to bytes. The input string is expected to be binary (e.g., '10KiB', not '10kB')
    This is what Elasticsearch _cat/indices emits by default. Use bytes="b" for raw bytes values

    Args:
    size_str (str): The string representing the size. Examples: '10kb', '2mb'.

    Returns:
    float: The size in bytes.
    """

    # Define the conversion units from various size units to bytes.
    size_units = {"kb": 1024, "mb": 1024**2, "gb": 1024**3, "tb": 1024**4, "b": 1}

    # Normalize the size string for consistent parsing.
    size_str = size_str.lower().replace(",", ".")

    # Extract the number and unit from the size string and calculate the size in bytes.
    for unit in size_units:
        if unit in size_str:
            return float(re.findall(r"\d+\.?\d*", size_str)[0]) * size_units[unit]
    return 0.0


def bytes_to_gigabytes(bytes_value: int) -> float:
    """
    Convert a value in bytes to gigabytes (GB).

    Args:
    bytes_value (int): The value in bytes.

    Returns:
    float: The value converted to gigabytes.

    Raises:
    TypeError: If bytes_value is not an integer.
    ValueError: If bytes_value is negative.
    """
    if not isinstance(bytes_value, int):
        raise TypeError("The bytes_value must be an integer.")
    if bytes_value < 0:
        raise ValueError("The bytes_value cannot be negative.")

    return bytes_value / (1000**3)


def bytes_to_gibibytes(bytes_value: int) -> float:
    """
    Convert a value in bytes to gibibytes (GiB).

    Args:
    bytes_value (int): The value in bytes.

    Returns:
    float: The value converted to gibibytes.

    Raises:
    TypeError: If bytes_value is not an integer.
    ValueError: If bytes_value is negative.
    """
    if not isinstance(bytes_value, int):
        raise TypeError("The bytes_value must be an integer.")
    if bytes_value < 0:
        raise ValueError("The bytes_value cannot be negative.")

    return bytes_value / (1024**3)


def fetch_es_data(client: Elasticsearch):
    """
    Fetch data from Elasticsearch using a GET request.

    Args:
    client (Elasticsearch): Elasticsearch client instance.

    Returns:
    requests.Response: The response object from the GET request. Sizes are in bytes.
    """
    return client.cat.indices(v=True, human=True, pretty=True, bytes="b")


def process_es_indices(es_client: Elasticsearch) -> list:

    es_data = fetch_es_data(es_client)

    # Split the response text into individual lines for further processing.
    lines = es_data.strip().split("\n")

    data_list = []
    # Extract headers (column names) from the first line of the response.
    headers_list = lines[0].split()

    # Convert each line of data into a dictionary and append to the data list.
    for line in lines[1:]:
        line = line.split()
        data_list.append(dict(zip(headers_list, line[0:])))

    # Calculate GB and GiB values for each index
    for data in data_list:
        data["Store Size (GB)"] = bytes_to_gigabytes(int(data["store.size"]))
        data["Store Size (GiB)"] = bytes_to_gibibytes(int(data["store.size"]))

    # Convert size values in the data list from strings to bytes.
    # for data in data_list:
    #     data["pri.store.size"] = parse_size(data["pri.store.size"])
    #     data["store.size"] = parse_size(data["store.size"])
    #     data["dataset.size"] = parse_size(data["dataset.size"])

    return data_list


def write_output(data_list: list, output_csv: str = "output.csv"):
    # Write the processed data to a CSV file.
    with open(output_csv, "w", newline="") as file:
        # Create a csv.DictWriter object to write dictionaries to a CSV.
        writer = csv.DictWriter(file, fieldnames=data_list[0].keys())

        # Write column headers to the CSV file.
        writer.writeheader()

        # Write each row of data to the CSV file.
        for row in data_list:
            writer.writerow(row)


def elasticsearch_location() -> tuple:
    """
    Prompts the user to choose an Elasticsearch location and returns the chosen location.

    Returns:
        tuple: A tuple containing the Elasticsearch Cloud ID and URL, based on the user's choice.
    """

    es_id = None
    es_url = None

    es_loc = input("Choose Elasticsearch Location (1: Cloud ID, 2: URL): ")

    if es_loc == "1":
        es_id = input("Enter Elasticsearch Cloud ID: ")
    elif es_loc == "2":
        es_url = input("Enter Elasticsearch URL: ")
    else:
        print("Invalid Elasticsearch Location chosen.")

    return es_id, es_url


def elasticsearch_auth() -> tuple:
    """
    Prompts the user to choose an authentication method for Elasticsearch.

    Returns:
        tuple: A tuple containing the API key and authentication credentials.
    """

    api_key = None
    auth = None

    # Prompt the user to choose the authentication method.
    auth_method = input(
        "Choose authentication method (1: API key, 2: username/password): "
    )

    if auth_method == "1":
        api_key = getpass("Enter Elasticsearch API key: ")

    elif auth_method == "2":
        username = input("Enter Elasticsearch username: ")
        password = getpass("Enter Elasticsearch password: ")
        auth = (username, password)

    else:
        print("Invalid authentication method chosen.")

    return api_key, auth


def main():
    """Main function of the script.

    This function sets up basic logging with a specific format, date format, log level, and handler.
    It then logs the current log level and default timezone.

    The function prompts the user to choose between Elasticsearch Cloud or an Elasticsearch URL. Depending on the user's choice,
    it either prompts the user to enter the Elasticsearch Cloud ID or the Elasticsearch URL. If the user's choice is not recognized,
    it prints an error message and returns.

    Args:
        None

    Returns:
        None
    """

    # setup basic logging
    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(module)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=LOG_LEVEL.upper(),
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logging.debug(f"LOG_LEVEL: {logging.getLevelName(logging.root.level)}")
    logging.debug(f"DEFAULT_TZ: {DEFAULT_TZ}")

    es_id = None
    es_url = None

    auth = None
    api_key = None

    # check for environment variables
    if ES_CLOUD_ID is not None and ES_API_KEY is not None:
        logging.debug("ES_CLOUD_ID and ES_API_KEY are set in env file.")
        use_env_vars = input(
            "Elastic Cloud ID and API Key environment variables detected \n"
            "Elastic Cloud ID is favoured over URLs \n"
            "Do you want to use the detected variables (y/n)?"
        )
        if use_env_vars.lower() == "y":
            es_id = ES_CLOUD_ID
            api_key = ES_API_KEY

        else:
            es_id, es_url = elasticsearch_location()
            api_key, auth = elasticsearch_auth()

    else:
        logging.debug("ES_CLOUD_ID or ES_API_KEY is not set in env file.")

    output_csv = (
        input("Enter output CSV file name (default: output/output.csv): ")
        or f"{OUTPUT_DIR}/output.csv"
    )

    print(f"\nOutput CSV file: {output_csv}")

    logging.debug(f"ES_ID: {es_id}")
    logging.debug(f"ES_URL: {es_url}")

    es_client = create_es_client(es_url=es_url, es_id=es_id, api_key=api_key, auth=auth)

    write_output(process_es_indices(es_client), output_csv=output_csv)


if __name__ == "__main__":
    main()
