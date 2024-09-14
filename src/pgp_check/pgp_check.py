import hashlib
import os

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """Calculate the hash of a file."""
    hash_func = getattr(hashlib, hash_algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_hash(file_path, expected_hash, algorithm='sha256'):
    """Verify the hash of a file against the expected hash."""
    try:
        calculated_hash = calculate_file_hash(file_path, algorithm)
        if calculated_hash == expected_hash:
            return True, calculated_hash
        else:
            return False, calculated_hash
    except FileNotFoundError:
        return False, "Error: File not found"
    except Exception as e:
        return False, f"Error: {str(e)}"
