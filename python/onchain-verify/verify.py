import json
from web3 import Web3
from eth_account.signers.local import LocalAccount
from eth_account import Account
import eth_account

node_url = "http://127.0.0.1:8545"
# contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3" # 20
# contract_address = "0x9A676e781A523b5d0C0e43731313A708CB607508" # 21
# contract_address = "0x0B306BF915C4d645ff596e518fAf3F9669b97016" # 22
# contract_address = "0x959922bE3CAee4b8Cd9a407cc3ac1C251C2007B1" # 22.b  -> original implementation from VDFs repo
# contract_address = "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE" # 22.c
# contract_address = "0x68B1D87F95878fE05B998F19b66F4baba5De1aed" # 23.new
# contract_address = "0x3Aa5ebB10DC797CAC828524e59A333d0A371443c" # 23.old
# contract_address = "0xc6e7DF5E7b4f2A278906862b61205850344D4e7d" # 24.old
# contract_address = "0x59b670e9fA9D0A427751Af201D676719a970857b" # 25.old

# contract_address = "0x322813Fd9A801c5507c9de605d63CEA4f2CE6c44" # 25.old delta 10
# contract_address = "0x4A679253410272dd5232B3Ff7cF5dbB88f295319" # 25.old delta 15
# contract_address = "0x67d269191c92Caf3cD7723F116c85e6E9bf55933" # 25.old delta 14
contract_address = "0xc3e53F4d16Ae77Db1c982e75a937B9f60FE63690" # 25.old delta 10

abi_file = "abi.json"
proof_file = "proof_original_25_1146.json"

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
        return json.load(f)['abi']

def connect_to_ethereum(node_url: str) -> Web3:
    """Connect to an Ethereum node."""
    w3 = Web3(Web3.HTTPProvider(node_url))
    # Set default account
    w3.eth.default_account = w3.eth.accounts[0]
    return w3

def prepare_proof_data(proof_data: dict) -> tuple:
    """Prepare proof data for the smart contract function."""
    x_bn = prepare_bignumber(proof_data['x']['val'], proof_data['x']['bitlen'])
    y_bn = prepare_bignumber(proof_data['y']['val'], proof_data['y']['bitlen'])
    v_array_bn = [prepare_bignumber(entry['val'], entry['bitlen']) for entry in proof_data['v']]
    return v_array_bn, x_bn, y_bn

def verify_vdf_onchain(w3: Web3, contract_address: str, contract_abi: list, proof_data: dict) -> tuple:
    """Verify the VDF proof on-chain and return verification result and gas used."""
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    v_array_bn, x_bn, y_bn = prepare_proof_data(proof_data)

    print("Verifying proof on-chain...")

    try:
        # First, estimate gas
        estimated_gas = contract.functions.verifyPietrzak(
            v_array_bn,
            x_bn,
            y_bn
        ).estimate_gas()
        
        print(f"Estimated gas: {estimated_gas}")

        # Send transaction directly
        tx_hash = contract.functions.verifyPietrzak(
            v_array_bn,
            x_bn,
            y_bn
        ).transact({
            'gas': estimated_gas
        })
        
        # Wait for transaction receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get actual gas used
        gas_used = receipt.gasUsed
        
        # Check if the transaction was successful
        if receipt.status == 1:
            return True, gas_used
        else:
            return False, gas_used

    except Exception as e:
        print(f"Verification failed: {e}")
        raise  # Let's raise the exception to see the full error

def main():
    print("Starting VDF proof verification on Ethereum...")
    # Load data and connect to Ethereum
    w3 = connect_to_ethereum(node_url)
    contract_abi = load_contract_abi(abi_file)
    proof_data = load_proof_data(proof_file)

    try:
        # Verify the proof and get gas used
        result, gas_used = verify_vdf_onchain(w3, contract_address, contract_abi, proof_data)
        
        print(f"Verification result: {result}")
        print(f"Gas used: {gas_used}")
        
        if result:
            print("✅ VDF proof verified successfully on-chain!")
        else:
            print("❌ VDF proof verification failed.")
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    main()