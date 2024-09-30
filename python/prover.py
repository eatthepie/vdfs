import sys
import logging
import time
from sympy import Integer
import json
from web3 import Web3
from typing import List, Tuple, Dict, Any
import pickle

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Pietrzak_VDF')

# Constants
N = 25195908475657893494027183240048398571429282126204032027777137836043662020707595556264018525880784406918290641249515082189298559149176184502808489120072844992687392807287776735971418347270261896375014971824691165077613379859095700097330459748808428401797429100642458691817195118746121515172654632282216869987549182422433637259085141865462043576798423387184774447920739934236584823824281198163815010674810451660377306056201619676256133844143603833904414952634432190114657544454178424020924616515723350778707749817125772467962926386356373289912154831438167899885040445364023527381951378636564391212010397122822120720357
T = 67108864 # 2 ** 26 ...... T = 1048576  # 2 ** 20

class VDFProver:
    def __init__(self, n: int, g: int, T: int):
        self.n = n
        self.g = g
        self.T = T

    def vdf(self) -> Tuple[int, List[int]]:
        """Compute the VDF function: g^(2^T) mod n"""
        exp_list = [self.g]
        g = self.g
        for _ in range(self.T):
            g = (g * g) % self.n
            exp_list.append(g)
        return g, exp_list

    @staticmethod
    def evaluate(exp_list: List[int], exp: int, n: int) -> int:
        """Evaluate g^exp mod n using the precomputed exp_list"""
        res = 1
        i = 0
        while exp > 0:
            if exp & 1:
                res = (res * exp_list[i]) % n
            exp >>= 1
            i += 1
        return res

    @staticmethod
    def eval_v(n: int, x: int, T: int, r: int) -> int:
        """Compute the intermediate value v for the proof"""
        i = 1
        sum_part = 0
        Z = Integer
        for j in range(2 ** (i - 1)):
            product_part = 1
            for k in range(1, i - 1):
                if (j % 2 ** k) > 0:
                    product_part *= r[i - 1 - k]
            sum_part += product_part * pow(Z(2), ((T / Z(2) ** i) + j * pow(T, Z(2) ** (i - 1))))
        return pow(x, int(sum_part), n) % n

    def gen_single_halving_proof(self, claim: Tuple[int, int, int, int, int]) -> Tuple[int, int, int, int, int]:
        """Generate a single halving proof"""
        n, x, y, T, v = claim
        r = hash_eth_128(x, y, v)
        x_prime = pow(x, r, n) * v % n
        y_prime = pow(v, r, n) * y % n
        T_half = T // 2 if T % 2 == 0 else (T + 1) // 2
        v = self.eval_v(n, x_prime, T_half, r)
        return (n, x_prime, y_prime, T_half, v)

    def gen_recursive_halving_proof(self, claim: Tuple[int, int, int, int, int]) -> List[Tuple[int, int, int, int, int]]:
        """Generate a recursive halving proof"""
        proof_list = [claim]
        while claim[3] > 1:
            claim = self.gen_single_halving_proof(claim)
            proof_list.append(claim)
        return proof_list

    @staticmethod
    def format_proof_for_onchain(proof_list: List[Tuple[int, int, int, int, int]]) -> Dict[str, Any]:
        """Format the proof for on-chain verification"""
        n_hex, x_hex, y_hex = map(hex, proof_list[0][:3])
        v_hex = [hex(p[4]) for p in proof_list[:-1]]

        return {
            "n": {"val": hex_to_bytes32(n_hex), "bitlen": compute_bitlen(n_hex)},
            "x": {"val": hex_to_bytes32(x_hex), "bitlen": compute_bitlen(x_hex)},
            "y": {"val": hex_to_bytes32(y_hex), "bitlen": compute_bitlen(y_hex)},
            "T": proof_list[0][3],
            "v": [{"val": hex_to_bytes32(val), "bitlen": compute_bitlen(val)} for val in v_hex]
        }

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

def compute_bitlen(hex_str: str) -> int:
    """Compute the bit length of a hex string"""
    return int(hex_str, 16).bit_length()

def hex_to_bytes32(hex_str: str) -> str:
    """Convert a hex string to a 32-byte hex string"""
    return hex_str[2:].zfill(64) if hex_str.startswith('0x') else hex_str.zfill(64)

def evaluate_vdf(g: int) -> Dict[str, Any]:
    """Evaluate the VDF and return the result and proof"""
    start_time = time.time()
    prover = VDFProver(N, g, T)

    print(f"Starting VDF evaluation with g={g}")
    y, exp_list = prover.vdf()
    T_half = T // 2 if T % 2 == 0 else (T + 1) // 2
    v = prover.evaluate(exp_list, pow(2, T_half), N)

    end_time = time.time()
    execution_time = end_time - start_time

    claim = (N, g, y, T, v)
    print(f"VDF evaluation completed in {execution_time:.2f} seconds")

    # Prepare and save proof for onchain verification
    proof_list = prover.gen_recursive_halving_proof(claim)
    proof_json = prover.format_proof_for_onchain(proof_list)

    with open('proof.json', 'w') as f:
        json.dump(proof_json, f, indent=4)

    # Generate and save raw proof
    with open('proof.pickle', 'wb') as f:
        pickle.dump(proof_list, f)

    print("✅ Proof saved to proof.json and proof.pickle")

def main():
    if len(sys.argv) < 2:
        print("Usage: python prover.py <g>")
        return

    g = int(sys.argv[1])
    evaluate_vdf(g)

if __name__ == '__main__':
    main()