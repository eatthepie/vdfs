// File: go/cmd/vdf_prover.go

package main

import (
	"encoding/json"
	"fmt"
	"math/big"
	"os"
	"time"

	"github.com/eatthepie/vdfs/go/pkg/vdf"
	"github.com/eatthepie/vdfs/go/pkg/util"
)

type ProofData struct {
	N struct {
		Val    string `json:"val"`
		Bitlen int    `json:"bitlen"`
	} `json:"n"`
	X struct {
		Val    string `json:"val"`
		Bitlen int    `json:"bitlen"`
	} `json:"x"`
	Y struct {
		Val    string `json:"val"`
		Bitlen int    `json:"bitlen"`
	} `json:"y"`
	T int       `json:"T"`
	V []VProof `json:"v"`
}

type VProof struct {
	V struct {
		Val    string `json:"val"`
		Bitlen int    `json:"bitlen"`
	} `json:"v"`
}

func formatProofForOnchain(proofList []vdf.Claim) ProofData {
	proof := ProofData{}
	proof.N.Val = "0x" + proofList[0].N.Text(16)
	proof.N.Bitlen = proofList[0].N.BitLen()
	proof.X.Val = "0x" + proofList[0].X.Text(16)
	proof.X.Bitlen = proofList[0].X.BitLen()
	proof.Y.Val = "0x" + proofList[0].Y.Text(16)
	proof.Y.Bitlen = proofList[0].Y.BitLen()
	proof.T = proofList[0].T

	for _, p := range proofList[:len(proofList)-1] { // Exclude the last proof (base case)
		vProof := VProof{}
		vProof.V.Val = "0x" + p.V.Text(16)
		vProof.V.Bitlen = p.V.BitLen()
		proof.V = append(proof.V, vProof)
	}

	return proof
}

func main() {
	g, _ := new(big.Int).SetString("2702608519755635878385320996194610791442298388087698459044354793170875406089102944208228897289234467866935860388679875443893545529554466363689608332379411342297088895328433512853915563930540281202658854965180942641321964738112144788639457955979237709811724908275386797159050672018353503846816144798133930123748117553972278601687176377164166082122222343096089655297954001896904931170987004646968232225410249512300600847730961776536544804567518739034725203121423156686985987754942333378456987899405303956315178985033112973699885750499423186910017346183705830610146945539653233129271006104510030972052573668194938717513", 10)

	start := time.Now()

	y, expList := vdf.VDF(g)
	tHalf := util.CalTHalf(vdf.T)
	v := vdf.Evaluate(expList, new(big.Int).Exp(big.NewInt(2), big.NewInt(int64(tHalf)), nil), vdf.N)

	claim := vdf.Claim{
		N: vdf.N,
		X: g,
		Y: y,
		T: vdf.T,
		V: v,
	}

	proofList := vdf.GenRecursiveHalvingProof(claim)

	duration := time.Since(start)

	fmt.Printf("Proof generated in %s\n", duration)

	proof := formatProofForOnchain(proofList)

	// Save proof to JSON file
	file, _ := json.MarshalIndent(proof, "", " ")
	_ = os.WriteFile("proof.json", file, 0644)

	fmt.Println("Proof saved to proof.json")
}