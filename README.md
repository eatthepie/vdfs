![Eat The Pie](https://github.com/eatthepie/docs/blob/main/static/img/header.png)

# Eat The Pie VDF Prover

This repository contains the VDF (Verifiable Delay Function) prover used in [Eat The Pie](https://www.eatthepie.xyz), the world lottery on Ethereum. The VDF system ensures truly random and fair number generation for the lottery. 🎲

## Overview

The VDF (Verifiable Delay Function) prover is a critical component that guarantees the fairness and randomness of the Eat The Pie lottery system. By implementing the Pietrzak VDF scheme, we ensure that lottery results cannot be manipulated or predicted in advance.

## Project Structure 📂

```
vdfs/
├── python/
│   ├── prover.py    # Generates VDF proofs
│   └── verifier.py  # Verifies VDF proofs
```

## Installation

```bash
# Install required Python packages
pip install sympy web3
```

## Usage

### Running the VDF Prover

```bash
cd python
python prover.py <G>
```

Where `G` is the input value for the VDF function.

### Running the VDF Verifier

```bash
python verifier.py
```

Note: The verifier uses the pickle file generated from the prover's results.

## Using it with Eat The Pie

### Step 1: Get the RANDAO Value

Obtain the RANDAO value for the lottery game through either:

- Web interface: Visit `eatthepie.xyz/results/[GAME_NUMBER]`
- CLI: Use the [CLI app](https://github.com/eatthepie/cli) and run:
  ```bash
  eatthepie game-info
  ```

### Step 2: Generate the VDF Proof

Using the RANDAO value from Step 1:

```bash
cd python
python prover.py [RANDAO_VALUE]
```

### Step 3: Verify and Submit

Once the proof is generated (`proof.json`), you can:

- For current games: Submit using the [CLI app](https://github.com/eatthepie/cli) and run `eatthepie submit-vdf-proof`
- For past games: Verify using the [CLI app](https://github.com/eatthepie/cli) and run `eatthepie verify-vdf`

## Technical Details

This implementation uses the Pietrzak VDF scheme, which provides:

- Verifiable computation time
- Non-parallelizable execution
- Efficient verification

## Acknowledgments

This implementation is based on the VDF prover code from [heun630/VDF-Prover-Optimization](https://github.com/heun630/VDF-Prover-Optimization/blob/main/python/pietrzak_vdf.py). We appreciate their work in optimizing the Pietrzak VDF implementation.

The project implements the Pietrzak VDF scheme, as described in: [Simple Verifiable Delay Functions](https://eprint.iacr.org/2018/627.pdf) (Krzysztof Pietrzak, 2018)

## License 📜

This project is licensed under the MIT License.
