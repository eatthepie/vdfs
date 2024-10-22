# This file contains code adapted from heun630/VDF-Prover-Optimization
# Source: https://github.com/heun630/VDF-Prover-Optimization/blob/main/python/pietrzak_vdf.py

import logging
import time
import json
from web3 import Web3
from typing import List, Tuple
import pickle

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Pietrzak_VDF')

class VDFVerifier:
    @staticmethod
    def process_single_halving_proof(VDF_claim: Tuple[int, int, int, int, int]) -> Tuple[int, int, int, int] or bool:
        """Process a single halving proof"""
        n, x, y, T, v = VDF_claim
        if T == 1:
            return y == pow(x, 2, n)
        r = hash_eth_128(x, y, v)
        x_prime = pow(x, r, n) * v % n
        T_half = T // 2 if T % 2 == 0 else (T + 1) // 2
        y = y * y % n if T % 2 != 0 else y
        y_prime = pow(v, r, n) * y % n
        return (n, x_prime, y_prime, T_half)

    @staticmethod
    def verify_recursive_halving_proof(proof_list: List[Tuple[int, int, int, int, int]]) -> bool:
        """Verify the recursive halving proof"""
        for i, proof in enumerate(proof_list):
            output = VDFVerifier.process_single_halving_proof(proof)
            if output is True:
                return True
            if output is False or (i + 1 < len(proof_list) and output != proof_list[i + 1][:-1]):
                log.warning('[-] Verification failed')
                return False
        return True

# Utility functions
def int_to_bytes(x: int) -> bytes:
    """Convert an arbitrarily large integer to bytes."""
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

def hash_eth(*integers: int) -> int:
    """Compute the Keccak-256 hash of the input integers"""
    # Convert integers to variable-length bytes
    byte_strings = [int_to_bytes(i) for i in integers]
    
    # Concatenate all byte strings
    input_bytes = b''.join(byte_strings)
    
    # Compute Keccak-256 hash
    r = Web3.keccak(input_bytes)
    return int.from_bytes(r, byteorder='big')

def hash_eth_128(*integers: int) -> int:
    """Compute the last 128 bits of the Keccak-256 hash of the input integers"""
    full_hash = hash_eth(*integers)
    return full_hash & ((1 << 128) - 1)  # Keep only the last 128 bits

def verify_vdf_proof(proof_file: str = 'proof.pickle') -> bool:
    """Verify the VDF proof"""
    with open(proof_file, 'rb') as f:
        proof_list = pickle.load(f)

    verifier = VDFVerifier()
    start_time = time.time()
    result = verifier.verify_recursive_halving_proof(proof_list)
    end_time = time.time()

    print(f"Verification time: {end_time - start_time:.2f} seconds")

    if result:
        print(f"✅ Verification successful!")
    else:
        print(f"❌ Verification failed")

def main():
    verify_vdf_proof()

if __name__ == '__main__':
    main()