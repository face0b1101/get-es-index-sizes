#!/usr/bin/env python

from unittest.mock import MagicMock, patch

import pytest

from get_es_index_sizes.config.env import VERSION
from get_es_index_sizes.main import (
    bytes_to_gibibytes,
    bytes_to_gigabytes,
    create_es_client,
    fetch_es_data,
    parse_size,
    process_es_indices,
    write_output,
)


def test_version():
    assert VERSION == "0.1.0"


def test_create_es_client_url():
    client = create_es_client(es_url="http://localhost:9200")
    assert client is not None


# Can't create a client without a valid cloud_id?
# def test_create_es_client_cloud_id():
#     client = create_es_client(
#         es_id="testing:dYtzb1V0aC5henVyZS5lbGFzdGljLYNsb1VkLmNvbTo0NDMkMGEyXmXyXzEyZDJlNDFjZGI5Njg5NjIxM2Y2ZYJkMGQkMzY0ZTdmZjRjNGE1NDI1M2I5ZjBiZTI1MDNlNYNiZDY="
#     )
#     assert client is not None


def test_create_es_client_api_key():
    client = create_es_client(es_url="http://localhost:9200", api_key="api_key_example")
    assert client is not None


def test_create_es_client_auth():
    client = create_es_client(es_url="http://localhost:9200", auth=("user", "pass"))
    assert client is not None


def test_create_es_client_invalid():
    with pytest.raises(ValueError):
        create_es_client(es_url="http://localhost:9200", es_id="cloud_id_example")

    with pytest.raises(ValueError):
        create_es_client(api_key="api_key_example", auth=("user", "pass"))


@patch("get_es_index_sizes.main.Elasticsearch")
def test_fetch_es_data(mock_es):
    mock_client = MagicMock()
    mock_es.return_value = mock_client
    mock_client.cat.indices.return_value = "index1 10kb\nindex2 20mb\n"
    response = fetch_es_data(mock_client)
    assert response == "index1 10kb\nindex2 20mb\n"


def test_parse_size():
    assert parse_size("10kb") == 10 * 1024
    assert parse_size("2mb") == 2 * 1024**2
    assert parse_size("1gb") == 1 * 1024**3
    assert parse_size("1tb") == 1 * 1024**4
    assert parse_size("100b") == 100
    assert parse_size("invalid") == 0.0


@patch("get_es_index_sizes.main.fetch_es_data")
def test_process_es_indices(mock_fetch):
    # Mock the fetch_es_data function to return a sample response
    mock_fetch.return_value = "index store.size\nindex1 1073741824\nindex2 2147483648\n"

    # Create a mock Elasticsearch client
    mock_client = MagicMock()

    # Call the function with the mock client
    processed_data = process_es_indices(mock_client)

    # Expected results
    expected_data = [
        {
            "index": "index1",
            "store.size": "1073741824",
            "Store Size (GB)": 1.073741824,
            "Store Size (GiB)": 1.0,
        },
        {
            "index": "index2",
            "store.size": "2147483648",
            "Store Size (GB)": 2.147483648,
            "Store Size (GiB)": 2.0,
        },
    ]

    # Assert the processed data matches the expected data
    assert processed_data == expected_data


def test_write_output(tmp_path):
    data_list = [
        {
            "index": "index1",
            "pri.store.size": 10240,
            "store.size": 20480,
            "dataset.size": 1073741824,
        },
        {
            "index": "index2",
            "pri.store.size": 20480,
            "store.size": 30720,
            "dataset.size": 2147483648,
        },
    ]
    output_csv = tmp_path / "output.csv"

    write_output(data_list, output_csv)

    with open(output_csv, "r") as file:
        content = file.read()

    assert "index,pri.store.size,store.size,dataset.size" in content
    assert "index1,10240,20480,1073741824" in content
    assert "index2,20480,30720,2147483648" in content


def test_bytes_to_gigabytes():
    assert bytes_to_gigabytes(1_000_000_000) == 1.0  # 1 GB
    assert bytes_to_gigabytes(5_000_000_000) == 5.0  # 5 GB
    assert bytes_to_gigabytes(500_000_000) == 0.5  # 0.5 GB
    assert bytes_to_gigabytes(0) == 0.0  # 0 bytes

    with pytest.raises(TypeError):
        bytes_to_gigabytes("1000000000")  # String instead of integer

    with pytest.raises(ValueError):
        bytes_to_gigabytes(-1000000000)  # Negative value


def test_bytes_to_gibibytes():
    assert bytes_to_gibibytes(1_073_741_824) == 1.0  # 1 GiB
    assert bytes_to_gibibytes(5_368_709_120) == 5.0  # 5 GiB
    assert bytes_to_gibibytes(536_870_912) == 0.5  # 0.5 GiB
    assert bytes_to_gibibytes(0) == 0.0  # 0 bytes

    with pytest.raises(TypeError):
        bytes_to_gibibytes("1073741824")  # String instead of integer

    with pytest.raises(ValueError):
        bytes_to_gibibytes(-1073741824)  # Negative value
