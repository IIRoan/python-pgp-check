import os
import tempfile
import pytest
import threading
from pathlib import Path
from pgp_check.cli import HashCalculator, main
import sys

# Import emoji constants from cli.py
from pgp_check.cli import CHECK_MARK, RED_X, WARNING, INFO

# Helper function to create a temporary file with content
def create_temp_file(content: str) -> str:
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(content)
    return path

@pytest.fixture
def temp_file():
    content = "Goodnight, Moon!"
    path = create_temp_file(content)
    yield path
    os.remove(path)

def test_hash_calculator(temp_file):
    calculator = HashCalculator(temp_file)
    calculated_hash, duration = calculator.calculate_hash()
    expected_hash = "ef763006da6fd870bcf8c389050cac0f0f2b62f5355d0379d7162a39642ce68c"
    assert calculated_hash == expected_hash
    assert isinstance(duration, float)
    assert duration > 0

def test_hash_calculator_different_algorithms(temp_file):
    algorithms = ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
    for algo in algorithms:
        calculator = HashCalculator(temp_file, algorithm=algo)
        hash_value, _ = calculator.calculate_hash()
        assert isinstance(hash_value, str)
        assert len(hash_value) > 0

def test_main_success(temp_file, capsys):
    correct_hash = "ef763006da6fd870bcf8c389050cac0f0f2b62f5355d0379d7162a39642ce68c"
    sys.argv = ['python-pgp-check', temp_file, correct_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Success: Hashes match!" in captured.out
    assert CHECK_MARK in captured.out

def test_main_failure(temp_file, capsys):
    incorrect_hash = "incorrect_hash"
    sys.argv = ['python-pgp-check', temp_file, incorrect_hash]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Hashes do not match!" in captured.out
    assert RED_X in captured.out

def test_main_file_not_found(capsys):
    non_existent_file = "/path/to/non_existent_file"
    sys.argv = ['python-pgp-check', non_existent_file]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out
    assert RED_X in captured.out

def test_main_with_algorithm(temp_file, capsys):
    md5_hash = "3af7eae7dfeba42339bf8517f011a21f"
    sys.argv = ['python-pgp-check', temp_file, md5_hash, '--algorithm', 'md5']
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Success: Hashes match!" in captured.out
    assert CHECK_MARK in captured.out

def test_main_calculate_only(temp_file, capsys):
    sys.argv = ['python-pgp-check', temp_file]
    main()  # No SystemExit expected for calculation only
    
    captured = capsys.readouterr()
    assert "Generated Hash:" in captured.out
    assert "Algorithm: SHA256" in captured.out

def test_main_invalid_algorithm(temp_file, capsys):
    sys.argv = ['python-pgp-check', temp_file, 'somehash', '--algorithm', 'invalid_algo']
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 2

def test_parallel_processing(temp_file):
    large_content = "x" * (11 * 1024 * 1024)  # 11MB file
    large_file = create_temp_file(large_content)
    
    try:
        calculator = HashCalculator(large_file)
        hash_value, duration = calculator.calculate_hash()
        assert isinstance(hash_value, str)
        assert len(hash_value) > 0
    finally:
        os.remove(large_file)

def test_keyboard_interrupt(temp_file, capsys, monkeypatch):
    def mock_calculate_hash(*args):
        raise KeyboardInterrupt()
    
    monkeypatch.setattr(HashCalculator, "calculate_hash", mock_calculate_hash)
    sys.argv = ['python-pgp-check', temp_file]
    
    with pytest.raises(SystemExit) as e:
        main()
    
    assert e.value.code == 130
    captured = capsys.readouterr()
    assert "Operation cancelled by user" in captured.out
    assert WARNING in captured.out