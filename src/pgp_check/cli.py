import argparse
import hashlib
import sys

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """Calculate the hash of a file."""
    hash_func = getattr(hashlib, hash_algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_hash(file_path, expected_hash, hash_algorithm='sha256'):
    """Verify if the file's hash matches the expected hash."""
    calculated_hash = calculate_file_hash(file_path, hash_algorithm)
    return calculated_hash == expected_hash

def main():
    parser = argparse.ArgumentParser(description='Verify file hash')
    parser.add_argument('file_location', help='Path to the file to check')
    parser.add_argument('hash', help='Expected hash value')
    parser.add_argument('--algorithm', default='sha256', choices=['md5', 'sha1', 'sha256', 'sha512'],
                        help='Hash algorithm to use (default: sha256)')
    
    args = parser.parse_args()

    try:
        calculated_hash = calculate_file_hash(args.file_location, args.algorithm)
        print(f"Debug: Calculated hash: {calculated_hash}")
        print(f"Debug: Expected hash: {args.hash}")
        print(f"Debug: Algorithm: {args.algorithm}")
        
        if verify_hash(args.file_location, args.hash, args.algorithm):
            print(f"Hash verification successful for {args.file_location}")
            sys.exit(0)
        else:
            print(f"Hash verification failed for {args.file_location}")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found - {args.file_location}")
        sys.exit(2)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(3)


if __name__ == '__main__':
    main()
