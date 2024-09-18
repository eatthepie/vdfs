# Eat The Pie VDF Proof Verifier

This repository contains scripts to verify VDF proofs for [Eat The Pie Lottery](https://www.eatthepie.xyz). The ability for anyone to compute and verify these proofs are central to the integrity of the lottery. The scripts are available in Go and Python.

## Prerequisites

- Go (version X.X or higher)
- Python (version 3.X or higher)

## Installation

1. Clone the repository:

## Usage

### Go

To verify a VDF proof using the Go script, run the following command:

```bash
go run vdf.go <proof> <challenge> <output>
```

Where:

- `<proof>` is the proof to verify
- `<challenge>` is the challenge used to generate the proof
- `<output>` is the output of the VDF

### Python

To verify a VDF proof using the Python script, run the following command:

```bash
python vdf.py <proof> <challenge> <output>
```

Where:

- `<proof>` is the proof to verify
- `<challenge>` is the challenge used to generate the proof
- `<output>` is the output of the VDF

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
