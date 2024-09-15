import hashlib

def calculate_file_hash(file_contents, hash_algorithm='sha256'):
    """Calculate the hash of file contents."""
    hash_func = getattr(hashlib, hash_algorithm)()
    hash_func.update(file_contents)
    return hash_func.hexdigest()

def verify_hash(file_contents, expected_hash, algorithm='sha256'):
    """Verify the hash of file contents against the expected hash."""
    try:
        calculated_hash = calculate_file_hash(file_contents, algorithm)
        if calculated_hash == expected_hash:
            return True, calculated_hash
        else:
            return False, calculated_hash
    except Exception as e:
        return False, f"Error: {str(e)}"
