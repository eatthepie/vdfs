![Eat The Pie](https://github.com/eatthepie/docs/blob/main/static/img/header.png)

# Eat The Pie VDF Prover

This repository contains the VDF prover used in [eatthepie.eth](https://www.eatthepie.xyz), the world lottery on Ethereum. 🎲

Verifiable Delay Functions (VDFs) are cryptographic primitives that require a specified amount of sequential computation time to evaluate, even with parallel computing resources. In the context of eatthepie.eth lottery, this time-locked property ensures truly random number generation that cannot be manipulated or predicted in advance, making it a cornerstone of our fair lottery system.

## 📂 Project Structure

```
vdfs/
├── helpers/
│   └── print_bignum_solidity.py
├── onchain-verification/
│   └── verify.py
├── python/
│   ├── prover.py
│   └── verifier.py
└── .gitignore
```

## Components 🛠️

### Helpers

- `print_bignum_solidity.py`: Utility for handling large numbers compatible with Solidity smart contracts

### Onchain Verification

- `verify.py`: Implementation of the VDF verification logic for Ethereum smart contracts

### Python Implementation

- `prover.py`: Core VDF proving system implementation
- `verifier.py`: VDF verification system implementation

## Setup

1. Ensure you have Python 3.7+ installed
2. Navigate to the `python` directory
3. Install the required dependencies

### Running the Prover 🔄

```bash
cd python
python prover.py [block.prevrandao]
```

This takes the `block.prevrandao` value as the input of the VDF function. ⏳ Computation may take a bit of time. Once done, it'll save a `proof.json` and `proof.pickle` file. You can use this for verification with the `verifier.py` file or onchain (download the eatthepie.eth CLI app to do this). To get the values of `block.prevrandao` from the eatthepie.eth lottery game, you can use the CLI app or go to the website.

### Verifying Results ✅

```bash
python verifier.py
```

Make sure your `proof.pickle` file is in the folder - this will verify that output.

## On-chain Verification 🔗

To verify a VDF proof on-chain, you have two options:

1. Navigate to `/onchain-verification` and use the `verify.py` file. Make sure to fill out these required fields at the top:

```python
node_url = ""
contract_address = ""
abi_file = ""
proof_file = ""
```

Then install the dependencies.

2. Use the CLI app to verify proofs:
   - Download the CLI app
   - Run `eatthepie submit-proof ...` to verify proofs of ongoing games or validate proofs of past games

## License 📜

This project is licensed under the MIT License.

## Acknowledgements 🙏

This implementation is based on the Pietrzak VDF scheme. For more information on VDFs, check out:

- [Simple Verifiable Delay Functions](https://eprint.iacr.org/2018/627.pdf) by Pietrzak
