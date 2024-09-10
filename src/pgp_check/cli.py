import argparse
import hashlib
import sys
import time
import threading
import itertools

# Unicode emojis
CHECK_MARK = "\u2705"  # Green checkmark
RED_X = "\u274C"  # Red X
WARNING = "\u26A0"  # Warning sign

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

def spinner_animation():
    """Display a spinner animation."""
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while True:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(description='Calculate or verify file hash')
    parser.add_argument('file_location', help='Path to the file to check')
    parser.add_argument('expected_hash', nargs='?', help='Expected hash value for verification')
    parser.add_argument('--algorithm', default='sha256', choices=['md5', 'sha1', 'sha256', 'sha512'],
                        help='Hash algorithm to use (default: sha256)')
    
    args = parser.parse_args()

    try:
        print(f"{WARNING} Calculating hash for: {args.file_location}")
        print(f"Algorithm: {args.algorithm}")
        print("Calculating: ", end='', flush=True)

        # Start the spinner animation in a separate thread
        spinner_thread = threading.Thread(target=spinner_animation)
        spinner_thread.daemon = True
        spinner_thread.start()

        # Calculate the hash
        calculated_hash = calculate_file_hash(args.file_location, args.algorithm)

        # Stop the spinner animation
        spinner_thread.do_run = False
        time.sleep(0.2)  # Give a moment for the spinner to stop
        sys.stdout.write('\b \b')  # Erase the last spinner character
        print("Done!")

        if args.expected_hash:
            print(f"Calculated: {calculated_hash}")
            print(f"Expected:   {args.expected_hash}")
            
            if verify_hash(args.file_location, args.expected_hash, args.algorithm):
                print(f"\n{CHECK_MARK} Hash verification successful!")
                sys.exit(0)
            else:
                print(f"\n{RED_X} Hash verification failed!")
                sys.exit(1)
        else:
            print(f"Hash: {calculated_hash}")
            sys.exit(0)
    except FileNotFoundError:
        print(f"{RED_X} Error: File not found - {args.file_location}")
        sys.exit(2)
    except Exception as e:
        print(f"{RED_X} An error occurred: {str(e)}")
        sys.exit(3)

if __name__ == '__main__':
    main()
