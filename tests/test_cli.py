import os
import tempfile
import pytest
from pgp_check.cli import calculate_file_hash, verify_hash, main

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
    import sys
    sys.argv = ['python-pgp-check', temp_file, correct_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Hash verification successful" in captured.out

def test_main_failure(temp_file, capsys):
    incorrect_hash = "incorrect_hash"
    
    # Simulate CLI arguments
    import sys
    sys.argv = ['python-pgp-check', temp_file, incorrect_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Hash verification failed" in captured.out

def test_main_file_not_found(capsys):
    non_existent_file = "/path/to/non_existent_file"
    some_hash = "some_hash"
    
    # Simulate CLI arguments
    import sys
    sys.argv = ['python-pgp-check', non_existent_file, some_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out

def test_main_with_algorithm(temp_file, capsys):
    md5_hash = "65a8e27d8879283831b664bd8b7f0ad4"

    # Print file content for debugging
    with open(temp_file, 'r') as f:
        print(f"File content: {f.read()}")

    # Simulate CLI arguments
    import sys
    sys.argv = ['python-pgp-check', temp_file, md5_hash, '--algorithm', 'md5']

    with pytest.raises(SystemExit) as e:
        main()

    captured = capsys.readouterr()
    print(f"Captured output: {captured.out}")

    assert e.value.code == 0
    assert "Hash verification successful" in captured.out



# Test for invalid algorithm
def test_main_invalid_algorithm(temp_file, capsys):
    some_hash = "some_hash"
    
    # Simulate CLI arguments
    import sys
    sys.argv = ['python-pgp-check', temp_file, some_hash, '--algorithm', 'invalid_algo']
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2  # argparse exits with code 2 for invalid arguments
