# vdf_onchain_verifier.py

import json
from web3 import Web3

def hex_to_bytes(hex_str: str) -> bytes:
    """Convert a hex string to bytes."""
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    return bytes.fromhex(hex_str.zfill(64))  # Ensure 32 bytes

def prepare_bignumber(val_hex: str, bitlen: int) -> dict:
    """Prepare a BigNumber struct for the smart contract."""
    return {
        'val': hex_to_bytes(val_hex),
        'bitlen': bitlen
    }

def load_proof_data(file_path: str) -> dict:
    """Load proof data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def load_contract_abi(file_path: str) -> list:
    """Load contract ABI from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)['abi']

def connect_to_ethereum(node_url: str) -> Web3:
    """Connect to an Ethereum node."""
    return Web3(Web3.HTTPProvider(node_url))

def prepare_proof_data(proof_data: dict) -> tuple:
    """Prepare proof data for the smart contract function."""
    n_bn = prepare_bignumber(proof_data['n']['val'], proof_data['n']['bitlen'])
    x_bn = prepare_bignumber(proof_data['x']['val'], proof_data['x']['bitlen'])
    y_bn = prepare_bignumber(proof_data['y']['val'], proof_data['y']['bitlen'])
    v_array_bn = [prepare_bignumber(entry['v']['val'], entry['v']['bitlen']) for entry in proof_data['v']]
    T = proof_data['T']
    return v_array_bn, x_bn, y_bn, n_bn, T

def verify_vdf_onchain(w3: Web3, contract_address: str, contract_abi: list, proof_data: dict, delta: int) -> bool:
    """Verify the VDF proof on-chain."""
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    v_array_bn, x_bn, y_bn, n_bn, T = prepare_proof_data(proof_data)

    try:
        verification_result = contract.functions.verifyPietrzak(
            v_array_bn,
            x_bn,
            y_bn,
            n_bn,
            delta,
            T
        ).call()
        return verification_result
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

def main():
    # User inputs
    node_url = input("Enter the Ethereum node URL: ")
    contract_address = input("Enter the contract address: ")
    proof_file = input("Enter the path to the proof JSON file: ")
    abi_file = input("Enter the path to the ABI JSON file: ")
    delta = int(input("Enter the delta value: "))

    # Load data and connect to Ethereum
    w3 = connect_to_ethereum(node_url)
    contract_abi = load_contract_abi(abi_file)
    proof_data = load_proof_data(proof_file)

    # Verify the proof
    result = verify_vdf_onchain(w3, contract_address, contract_abi, proof_data, delta)

    if result:
        print("VDF proof verified successfully on-chain!")
    else:
        print("VDF proof verification failed.")

if __name__ == "__main__":
    main()