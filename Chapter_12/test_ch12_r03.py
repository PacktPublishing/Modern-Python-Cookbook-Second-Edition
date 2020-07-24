"""Python Cookbook 2nd ed.

Tests for ch12_r03
"""
import os
import re
from pathlib import Path
import subprocess
import time
from pytest import *  # type: ignore

import Chapter_12.ch12_r03

@fixture(scope="module")  # type: ignore
def ch12_r02_server():
    """Start and stop the server."""
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).parent.parent)
    env['DEAL_APP_SEED'] = '42'
    server = subprocess.Popen(["python", "Chapter_12/ch12_r02.py"], env=env)
    time.sleep(0.5)  # Pause to let the server start.

    yield server  # allow the test to run

    time.sleep(0.25)
    server.terminate()
    time.sleep(0.25)  # Pause while the server finishes.
    server.wait()
    # server.kill()
    assert server.returncode == 0, f"Server Exit Status {server_process.returncode}"

def test_get_spec(ch12_r02_server, capsys):
    spec = Chapter_12.ch12_r03.get_openapi_spec()
    assert spec['info']['title'] == 'Python Cookbook Chapter 12, recipe 2.'
    out, err = capsys.readouterr()
    assert out == "openapi.json is valid\n"

header_pattern = re.compile(r"[\w-]+: .*?")

def test_query_build_1(ch12_r02_server, capsys):
    Chapter_12.ch12_r03.query_build_1()
    out, err = capsys.readouterr()
    status_headers, _, body = out.partition("\n\n")
    status, *headers = status_headers.splitlines()
    assert status == "200"
    assert all(header_pattern.match(h) for h in headers)
    assert body == "\n[{'__class__': 'Card', '__init__': {'rank': 10, 'suit': '♡'}}, {'__class__': 'Card', '__init__': {'rank': 4, 'suit': '♡'}}, {'__class__': 'Card', '__init__': {'rank': 7, 'suit': '♠'}}, {'__class__': 'Card', '__init__': {'rank': 11, 'suit': '♢'}}, {'__class__': 'Card', '__init__': {'rank': 12, 'suit': '♡'}}]\n"

def test_query_build_2(ch12_r02_server, capsys):
    spec = Chapter_12.ch12_r03.get_openapi_spec()
    Chapter_12.ch12_r03.query_build_2(spec)
    out, err = capsys.readouterr()
    status_headers, _, body = out.partition("\n\n")
    spec_response, status, *headers = status_headers.splitlines()
    assert spec_response == "openapi.json is valid"
    assert status == "200"
    assert all(header_pattern.match(h) for h in headers)
    assert body == "\n[{'cards': [{'__class__': 'Card', '__init__': {'rank': 3, 'suit': '♣'}}, {'__class__': 'Card', '__init__': {'rank': 10, 'suit': '♠'}}], 'hand': 0}, {'cards': [{'__class__': 'Card', '__init__': {'rank': 9, 'suit': '♠'}}], 'hand': 1}, {'cards': [{'__class__': 'Card', '__init__': {'rank': 13, 'suit': '♣'}}], 'hand': 2}, {'cards': [{'__class__': 'Card', '__init__': {'rank': 5, 'suit': '♣'}}], 'hand': 3}]\n"
