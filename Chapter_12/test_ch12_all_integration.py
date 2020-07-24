"""Python Cookbook 2nd ed.

Tests for all ch12_r??_client and ch12_r??_server pairs

This requires ``demo.cert`` and ``demo.key`` in the local working directory.

"""
import os
import subprocess
import sys
import time
import pytest  # type: ignore
from pytest import *  # type: ignore

client_server_pairs = [
    ("Chapter_12/ch12_r04_client.py", "Chapter_12/ch12_r04_server.py"),
    ("Chapter_12/ch12_r05_client.py", "Chapter_12/ch12_r05_server.py"),
    ("Chapter_12/ch12_r06_client.py", "Chapter_12/ch12_r06_server.py"),
]

@fixture(params=client_server_pairs, ids=lambda x:f"{x[0]}-{x[1]}")  # type: ignore
def client_server(request):
    client, server = request.param
    server_process = subprocess.Popen(["python", server])
    print(f"Starting {server_process.pid}")
    time.sleep(0.5)  # Pause to let the server start.

    yield client, server

    time.sleep(0.25)
    server_process.terminate()
    time.sleep(0.25)  # Pause while the server finishes.
    server_process.wait()
    assert server_process.returncode == 0, f"Server Exit Status {server_process.returncode}"

@pytest.mark.ssl
def test_client_main(client_server, tmp_path):
    client, server = client_server
    cache = tmp_path/"log"
    with cache.open('w') as log_output:
        client_process = subprocess.run(
            ["python", client],
            text=True,
        )
    print(cache.read_text(), file=sys.stdout)
    assert client_process.returncode == 0

