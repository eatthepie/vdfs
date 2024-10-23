![Eat The Pie](https://github.com/eatthepie/docs/blob/main/static/img/header.png)

# Eat The Pie VDF Prover

This repository contains the VDF (Verifiable Delay Function) prover used in [Eat The Pie](https://www.eatthepie.xyz), the world lottery on Ethereum. The VDF system ensures truly random and fair number generation for our lottery game. 🎲

## What is a VDF?

Verifiable Delay Functions (VDFs) are cryptographic primitives that require a specified amount of sequential computation time to evaluate, even with parallel computing resources. In Eat The Pie, this time-locked property ensures that lottery numbers cannot be manipulated or predicted in advance, guaranteeing a fair game for all players.

## Using the VDF Prover with Eat The Pie 🎯

### Prerequisites

- Python 3.7+
- [Eat The Pie CLI app](https://github.com/eatthepie/cli) (`npm install -g eatthepie`)

### Step-by-Step Guide

1. **Get the RANDAO Value**

   - Option A: Visit [eatthepie.xyz](https://www.eatthepie.xyz) and find the RANDAO value for a game
   - Option B: Use the CLI app:
     ```bash
     eatthepie game-info [game-number]
     ```

2. **Generate the VDF Proof**

   ```bash
   cd python
   python prover.py [RANDAO_VALUE]
   ```

   This will generate two files:

   - `proof.json` - Used for submitting to the game
   - `proof.pickle` - Used for local verification

3. **Submit/Verify the Proof**
   - For active games, submit the proof with the CLI app:
     ```bash
     eatthepie submit-vdf-proof
     ```
   - For past games, verify a proof with the CLI app:
     ```bash
     eatthepie verify-vdf
     ```

### Local Verification (Optional)

To verify your proof locally before submission:

```bash
python verifier.py
```

Make sure your `proof.pickle` file is in the same directory.

## Project Structure 📂

```
vdfs/
├── python/
│   ├── prover.py
│   └── verifier.py
```

## Technical Details

This implementation uses the Pietrzak VDF scheme. For more information:

- [Simple Verifiable Delay Functions](https://eprint.iacr.org/2018/627.pdf) by Pietrzak

## License 📜

This project is licensed under the MIT License.
