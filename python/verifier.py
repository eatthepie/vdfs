# This file is adapted from heun630/VDF-Prover-Optimization
# Source: https://github.com/heun630/VDF-Prover-Optimization/blob/main/python/pietrzak_vdf.py

import logging
import time
from web3 import Web3
from typing import List, Tuple, Union
import pickle

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Pietrzak_VDF')

def pad_hex(x: str) -> str:
    """
    Pad hex string to ensure consistent length
    Critical for deterministic hashing across implementations
    """
    n = (64 - (len(x) % 64)) % 64
    return ('0' * n) + x

def hash_eth(*integers: int) -> int:
    """
    Keccak-256 hash function for proof challenges
    Processes integers by converting to padded hex strings
    Must match prover's implementation exactly
    """
    toHex = [format(int(x), '02x') for x in integers]
    padToEvenLen = [pad_hex(x) for x in toHex]
    input = ''.join(padToEvenLen)
    r = Web3.keccak(hexstr=input)
    return int(r.hex(), 16)

def hash_eth_128(*integers: int) -> int:
    """
    128-bit challenge generator
    Uses upper bits of Keccak-256 hash for better security
    Must be identical to prover's implementation
    """
    r = hash_eth(*integers)
    return r >> 128

class VDFVerifier:
    @staticmethod
    def process_single_halving_proof(VDF_claim: Tuple[int, int, int, int, int]) -> Union[Tuple[int, int, int, int], bool]:
        """
        Verify a single step of the VDF proof
        For T=1, directly checks x^2 = y
        For T>1, computes next verification step
        
        Parameters:
        - VDF_claim: (n, x, y, T, v) where:
            n: RSA modulus
            x: Current base
            y: Claimed result
            T: Time parameter
            v: Intermediate value for verification
        
        Returns:
        - For T=1: Boolean indicating if proof step is valid
        - For T>1: Tuple of values for next verification step
        """
        n, x, y, T, v = VDF_claim

        # Base case: direct verification for T=1
        if T == 1:
            check = pow(x, 2, n)
            return y == check

        # Generate challenge using Fiat-Shamir transform
        r = hash_eth_128(x, y, v)
        x_prime = pow(x, r, n) * v % n

        # Handle odd T by squaring y
        if T % 2 == 0:
            T_half = T // 2
        else:
            T_half = (T + 1) // 2
            y = y * y % n

        y_prime = pow(v, r, n) * y % n
        return (n, x_prime, y_prime, T_half)

    @staticmethod
    def verify_recursive_halving_proof(proof_list: List[Tuple[int, int, int, int, int]]) -> bool:
        """
        Verify complete VDF proof through recursive halving
        
        Checks each proof step and validates consistency between steps
        Proof should reduce T by half each step until T=1
        
        Parameters:
        - proof_list: List of (n, x, y, T, v) tuples representing each step
        
        Returns:
        - Boolean indicating if the entire proof is valid
        """
        for i in range(len(proof_list)):
            output = VDFVerifier.process_single_halving_proof(proof_list[i])

            if output is True:  # Final step verified successfully
                break
            elif output is False:  # Final step verification failed
                log.warning('[-] Verification failed: The final proof returned False')
                return False
            elif i + 1 < len(proof_list) and output != proof_list[i + 1][:-1]:
                # Intermediate step doesn't match next proof step
                log.warning('[-] Verification failed: The proof chain is invalid')
                log.warning(f'invalid proof: {proof_list[i + 1][:-1]}')
                return False

        return True

def verify_vdf_proof(proof_file: str = 'proof.pickle') -> bool:
    """
    Main verification function
    Loads proof from file and performs complete verification
    
    Parameters:
    - proof_file: Path to pickled proof file
    
    Returns:
    - Boolean indicating if proof is valid
    
    Times and logs the verification process
    """
    with open(proof_file, 'rb') as f:
        proof_list = pickle.load(f)

    verifier = VDFVerifier()
    start_time = time.time()
    result = verifier.verify_recursive_halving_proof(proof_list)
    end_time = time.time()

    print(f"Verification time: {end_time - start_time:.2f} seconds")

    if result:
        print("✅ Verification successful!")
    else:
        print("❌ Verification failed")
    return result

def main():
    verify_vdf_proof()

if __name__ == '__main__':
    main()