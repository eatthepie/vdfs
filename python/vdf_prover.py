# vdf_prover.py

import hashlib
import time
import json
from typing import Dict, List, Tuple

class VDFProver:
    N = 14901995024560329904961350434753246183585009359863918037600291689447425867236233280234158146280526361619483655084377817580307380713779960796538243284679321655995122337644690241899724673620138350577731488123546542205271115215104758591923818947441465813939827252468298458501512274934213283394474929252890272815322072728121545402142127571518643073412545552919444768620193923721115040874821490498192845163014782819480348378252338278631734877270049886059699056015701542491308767095812631609792009922308416690626638089323812382387729710604396893335711577183169675469709449341880762946125460470722355849832821059916566355909
    T = 2 ** 20

    def __init__(self, g: int):
        self.g = g

    def vdf(self) -> Tuple[int, List[int]]:
        exp_list = [self.g]
        g = self.g
        for _ in range(self.T):
            g = (g * g) % self.N
            exp_list.append(g)
        return g, exp_list

    @staticmethod
    def evaluate(exp_list: List[int], exp: int, n: int) -> int:
        res = 1
        i = 0
        while exp > 0:
            if exp & 1:
                res = (res * exp_list[i]) % n
            exp >>= 1
            i += 1
        return res

    @staticmethod
    def hash_eth_128(*args: int) -> int:
        h = hashlib.sha3_256()
        for arg in args:
            h.update(arg.to_bytes((arg.bit_length() + 7) // 8, 'big'))
        return int.from_bytes(h.digest()[:16], 'big')

    def gen_single_halving_proof(self, claim: Tuple[int, int, int, int, int]) -> Tuple[int, int, int, int, int]:
        n, x, y, T, v = claim
        r = self.hash_eth_128(x, y, v)
        x_prime = pow(x, r, n) * v % n
        y_prime = pow(v, r, n) * y % n
        T_half = (T + 1) // 2 if T % 2 else T // 2
        v = self.evaluate(self.vdf()[1], pow(2, T_half), n)
        return (n, x_prime, y_prime, T_half, v)

    def gen_recursive_halving_proof(self, claim: Tuple[int, int, int, int, int]) -> List[Tuple[int, int, int, int, int]]:
        proof_list = [claim]
        while claim[3] > 1:
            claim = self.gen_single_halving_proof(claim)
            proof_list.append(claim)
        return proof_list

    def generate_proof(self) -> List[Tuple[int, int, int, int, int]]:
        y, exp_list = self.vdf()
        T_half = (self.T + 1) // 2 if self.T % 2 else self.T // 2
        v = self.evaluate(exp_list, pow(2, T_half), self.N)
        claim = (self.N, self.g, y, self.T, v)
        return self.gen_recursive_halving_proof(claim)

    def generate_proof(self) -> Dict:
        y, exp_list = self.vdf()
        T_half = (self.T + 1) // 2 if self.T % 2 else self.T // 2
        v = self.evaluate(exp_list, pow(2, T_half), self.N)
        claim = (self.N, self.g, y, self.T, v)
        proof_list = self.gen_recursive_halving_proof(claim)
        
        return self.format_proof_for_onchain(proof_list)

    def format_proof_for_onchain(self, proof_list: List[Tuple[int, int, int, int, int]]) -> Dict:
        proof_data = {
            "n": {
                "val": hex(self.N),
                "bitlen": self.N.bit_length()
            },
            "x": {
                "val": hex(self.g),
                "bitlen": self.g.bit_length()
            },
            "y": {
                "val": hex(proof_list[0][2]),
                "bitlen": proof_list[0][2].bit_length()
            },
            "T": self.T,
            "v": []
        }

        for proof in proof_list[:-1]:  # Exclude the last proof (base case)
            proof_data["v"].append({
                "v": {
                    "val": hex(proof[4]),
                    "bitlen": proof[4].bit_length()
                }
            })

        return proof_data

def main():
    # Example usage
    g = 2702608519755635878385320996194610791442298388087698459044354793170875406089102944208228897289234467866935860388679875443893545529554466363689608332379411342297088895328433512853915563930540281202658854965180942641321964738112144788639457955979237709811724908275386797159050672018353503846816144798133930123748117553972278601687176377164166082122222343096089655297954001896904931170987004646968232225410249512300600847730961776536544804567518739034725203121423156686985987754942333378456987899405303956315178985033112973699885750499423186910017346183705830610146945539653233129271006104510030972052573668194938717513
    
    prover = VDFProver(g)
    
    start_time = time.time()
    proof = prover.generate_proof()
    end_time = time.time()
    
    print(f"Proof generated in {end_time - start_time:.2f} seconds")
    
    # Save proof to JSON file
    with open('proof.json', 'w') as f:
        json.dump(proof, f, indent=2)
    
    print("Proof saved to proof.json")

if __name__ == "__main__":
    main()
