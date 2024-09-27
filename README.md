# Eat The Pie VDF Prover and Verifier

This repository is used to generate and verify proofs for Eat The Pie. It contains both Python and Go implementations of the VDF prover and an on-chain verifier script.

## Project Structure

```
vdfs/
├── python/
│   ├── vdf_prover.py
├── go/
│   ├── cmd/
│   │   └── vdf_prover.go
│   └── pkg/
│       ├── vdf/
│       │   └── vdf.go
│       └── util/
│           └── util.go
├── verifier/
│   ├── vdf_onchain_verifier.py
├── README.md
└── .gitignore
```

## Installation

### Python

1. Ensure you have Python 3.7+ installed.
2. Navigate to the `python` directory.
3. Install the required dependencies

### Go

1. Ensure you have Go 1.16+ installed.
2. Navigate to the `go` directory.
3. Install the required dependencies:
   ```
   go mod tidy
   ```

## Generating Proof for On-chain Verification

Both Python and Go implementations now generate a `proof.json` file that can be used for on-chain verification.

### Python

Run the VDF prover:

```
python vdf_prover.py
```

### Go

Build and run the VDF prover:

```
go build -o vdf_prover go/cmd/vdf_prover.go
./vdf_prover
```

Both implementations will generate a `proof.json` file in the current directory. This file contains the proof in the correct format for on-chain verification.

You can use this `proof.json` file with the `vdf_onchain_verifier.py` script to verify the proof on-chain.

## On-chain Verification

To verify a VDF proof on-chain:

1. Ensure you have the `web3` library installed:

   ```
   pip install web3
   ```

2. Run the on-chain verifier script:

   ```
   python vdf_onchain_verifier.py
   ```

3. You will be prompted to enter the following information:
   - Ethereum node URL
   - Contract address
   - Path to the proof JSON file
   - Path to the ABI JSON file
   - Delta value

The script will then attempt to verify the proof on-chain and display the result.

Make sure you have a valid Ethereum node URL, the correct contract address, and properly formatted proof and ABI JSON files before running the verification.

## License

This project is licensed under the MIT License.

## Acknowledgements

This implementation is based on the Pietrzak VDF scheme. For more information on VDFs, refer to the following resources:

- [Simple Verifiable Delay Functions](https://eprint.iacr.org/2018/627.pdf) by Pietrzak
