import json
from web3 import Web3

node_url = ""
contract_address = ""
abi_file = ""
proof_file = ""

def hex_to_bytes(hex_str):
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]

    hex_str = ''.join(hex_str.split()).lower()
    
    if not all(c in '0123456789abcdef' for c in hex_str):
        raise ValueError("Invalid hexadecimal string")

    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    
    try:
        return bytes.fromhex(hex_str)
    except ValueError as e:
        print(f"Error converting to bytes: {e}")
        raise

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
        return json.load(f)

def connect_to_ethereum(node_url: str) -> Web3:
    """Connect to an Ethereum node."""
    return Web3(Web3.HTTPProvider(node_url))

def prepare_proof_data(proof_data: dict) -> tuple:
    """Prepare proof data for the smart contract function."""
    x_bn = prepare_bignumber(proof_data['x']['val'], proof_data['x']['bitlen'])
    y_bn = prepare_bignumber(proof_data['y']['val'], proof_data['y']['bitlen'])
    v_array_bn = [prepare_bignumber(entry['val'], entry['bitlen']) for entry in proof_data['v']]
    return v_array_bn, x_bn, y_bn

def verify_vdf_onchain(w3: Web3, contract_address: str, contract_abi: list, proof_data: dict) -> bool:
    """Verify the VDF proof on-chain."""
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    v_array_bn, x_bn, y_bn = prepare_proof_data(proof_data)

    print("Verifying proof on-chain...")

    try:
        verification_result = contract.functions.verifyPietrzak(
            v_array_bn,
            x_bn,
            y_bn
        ).call()
        return verification_result
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

def main():
    print("Starting VDF proof verification on Ethereum...")
    # Load data and connect to Ethereum
    w3 = connect_to_ethereum(node_url)
    contract_abi = load_contract_abi(abi_file)
    proof_data = load_proof_data(proof_file)

    # Verify the proof
    result = verify_vdf_onchain(w3, contract_address, contract_abi, proof_data)

    if result:
        print("✅ VDF proof verified successfully on-chain!")
    else:
        print("❌ VDF proof verification failed.")

if __name__ == "__main__":
    main()