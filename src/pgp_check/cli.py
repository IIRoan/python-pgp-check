import argparse
import hashlib
import hmac
import sys
import time
import threading
import itertools
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
from pathlib import Path
from typing import Optional, Tuple

# Unicode emojis and colors
CHECK_MARK = "\u2705"
RED_X = "\u274C"
WARNING = "\u26A0"
INFO = "\u2139"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

__version__ = version("python-pgp-check")

class HashCalculator:
    """Class to handle hash calculation with improved performance and feedback."""
    
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks for better memory management
    
    def __init__(self, file_path: str, algorithm: str = 'sha256'):
        self.file_path = Path(file_path)
        self.algorithm = algorithm
        self.hash_func = getattr(hashlib, algorithm)
        self._stop_event = threading.Event()
        self.progress = 0
        
    def _calculate_chunk_hash(self, chunk: bytes) -> bytes:
        """Calculate hash for a single chunk."""
        return self.hash_func(chunk).digest()
    
    def calculate_hash(self) -> Tuple[str, float]:
        """Calculate file hash with progress tracking."""
        start_time = time.time()
        file_size = self.file_path.stat().st_size
        
        try:
            # For small files, use single-threaded processing
            if file_size < 10 * 1024 * 1024:  # 10MB threshold
                return self._calculate_single_threaded(), time.time() - start_time
            
            # For large files, use parallel processing
            return self._calculate_parallel(), time.time() - start_time
            
        except IOError as e:
            raise IOError(f"Error reading file: {e}")
    
    def _calculate_single_threaded(self) -> str:
        """Calculate hash using single thread for small files."""
        hasher = self.hash_func()
        
        with open(self.file_path, 'rb') as f:
            mm = memoryview(bytearray(self.CHUNK_SIZE))
            while not self._stop_event.is_set():
                n = f.readinto(mm)
                if not n:
                    break
                hasher.update(mm[:n])
                
        return hasher.hexdigest()
    
    def _calculate_parallel(self) -> str:
        """Calculate hash using parallel processing for large files."""
        chunks = []
        final_hasher = self.hash_func()
        
        with open(self.file_path, 'rb') as f:
            while True:
                chunk = f.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                chunks.append(chunk)
        
        # Use ThreadPoolExecutor for I/O-bound operations
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            chunk_hashes = list(executor.map(self._calculate_chunk_hash, chunks))
        
        # Combine chunk hashes
        for chunk_hash in chunk_hashes:
            final_hasher.update(chunk_hash)
        
        return final_hasher.hexdigest()

def spinner_animation(stop_event: threading.Event):
    """Display an enhanced spinner animation."""
    spinners = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not stop_event.is_set():
        sys.stdout.write(next(spinners))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

def format_time(seconds: float) -> str:
    """Format time duration in a human-readable format."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes} minutes {seconds:.2f} seconds"

def verify_hash(calculated_hash: str, expected_hash: str) -> bool:
    """Compare hashes using constant-time comparison."""
    if not calculated_hash or not expected_hash:
        return False
    
    # Convert to bytes for constant-time comparison
    return hmac.compare_digest(
        calculated_hash.lower().encode(),
        expected_hash.lower().encode()
    )


def main():
    parser = argparse.ArgumentParser(
        description='Fast and secure file hash calculator and verifier',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file_location', help='Path to the file to check')
    parser.add_argument('expected_hash', nargs='?', help='Expected hash value for verification')
    parser.add_argument(
        '--algorithm',
        default='sha256',
        choices=['md5', 'sha1', 'sha256', 'sha384', 'sha512'],
        help='Hash algorithm to use (default: sha256)'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Show the version of the package'
    )
    
    args = parser.parse_args()

    try:
        file_path = Path(args.file_location).expanduser().resolve()
        
        if not file_path.exists():
            print(f"\n{RED_X} {RED}Error: File not found - {file_path}{RESET}")
            sys.exit(2)
        
        # Show file info with better formatting
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024*1024)
        
        print(f"{'─'*80}")

        print(f"{INFO} File Details:")
        print(f"  • Path: {file_path}")
        print(f"  • Size: {file_size_mb:.2f} MB")
        print(f"  • Algorithm: {args.algorithm.upper()}")
        print(f"{'─'*80}")
        print(f"Calculating hash... ", end='', flush=True)

        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            calculator = HashCalculator(str(file_path), args.algorithm)
            calculated_hash, duration = calculator.calculate_hash()
        finally:
            stop_event.set()
            time.sleep(0.1)
            sys.stdout.write('\r' + ' ' * 50 + '\r')
            sys.stdout.flush()
        
        print(f"Completed in {format_time(duration)}")


        if args.expected_hash:
            print("Hash Verification:")
            print(f"  Calculated: {YELLOW}{calculated_hash}{RESET}")
            print(f"  Expected:   {YELLOW}{args.expected_hash}{RESET}")
            
            if verify_hash(calculated_hash, args.expected_hash):
                print(f"{CHECK_MARK} {GREEN}Success: Hashes match!{RESET}")
                sys.exit(0)
            else:
                print(f"{RED_X} {RED}Error: Hashes do not match!{RESET}")
                sys.exit(1)
        else:
            print(f"Generated Hash: {YELLOW}{calculated_hash}{RESET}")
        

    except KeyboardInterrupt:
        print(f"\n{WARNING} {YELLOW}Operation cancelled by user{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{RED_X} {RED}An error occurred: {str(e)}{RESET}")
        sys.exit(3)

if __name__ == '__main__':
    main()