import os
import tempfile
import pytest
from pgp_check.cli import calculate_file_hash, verify_hash, main
import sys

# Helper function to create a temporary file with content
def create_temp_file(content):
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path

# Fixture to create a temporary file for testing
@pytest.fixture
def temp_file():
    content = "Hello, World!"
    path = create_temp_file(content)
    yield path
    os.remove(path)

def test_calculate_file_hash(temp_file):
    expected_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    assert calculate_file_hash(temp_file) == expected_hash

def test_verify_hash_success(temp_file):
    correct_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    assert verify_hash(temp_file, correct_hash) == True

def test_verify_hash_failure(temp_file):
    incorrect_hash = "incorrect_hash"
    assert verify_hash(temp_file, incorrect_hash) == False

def test_main_success(temp_file, capsys):
    correct_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    
    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', temp_file, correct_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Hash verification successful" in captured.out
    assert "\u2705" in captured.out  # Check for green checkmark

def test_main_failure(temp_file, capsys):
    incorrect_hash = "incorrect_hash"
    
    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', temp_file, incorrect_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Hash verification failed" in captured.out
    assert "\u274C" in captured.out  # Check for red X

def test_main_file_not_found(capsys):
    non_existent_file = "/path/to/non_existent_file"
    some_hash = "some_hash"
    
    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', non_existent_file, some_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out
    assert "\u274C" in captured.out  # Check for red X

def test_main_with_algorithm(temp_file, capsys):
    md5_hash = "65a8e27d8879283831b664bd8b7f0ad4"

    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', temp_file, md5_hash, '--algorithm', 'md5']

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Hash verification successful" in captured.out
    assert "\u2705" in captured.out  # Check for green checkmark

def test_main_calculate_only(temp_file, capsys):
    # Simulate CLI arguments for hash calculation only
    sys.argv = ['python-pgp-check', temp_file]

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Calculating hash for:" in captured.out
    assert "\u26A0" in captured.out  # Check for warning sign
    assert "Algorithm: sha256" in captured.out
    assert "Hash:" in captured.out

# Test for invalid algorithm
def test_main_invalid_algorithm(temp_file, capsys):
    some_hash = "some_hash"
    
    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', temp_file, some_hash, '--algorithm', 'invalid_algo']
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2  # argparse exits with code 2 for invalid arguments

# Test for spinner animation
def test_main_spinner_animation(temp_file, capsys):
    # Simulate CLI arguments
    sys.argv = ['python-pgp-check', temp_file]

    with pytest.raises(SystemExit) as e:
        main()

    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Calculating: " in captured.out
    assert "Done!" in captured.out
