// File: go/pkg/vdf/vdf.go

package vdf

import (
	"crypto/sha3"
	"math/big"
	"github.com/your-username/vdfs/go/pkg/util"
)

var (
	N, _ = new(big.Int).SetString("14901995024560329904961350434753246183585009359863918037600291689447425867236233280234158146280526361619483655084377817580307380713779960796538243284679321655995122337644690241899724673620138350577731488123546542205271115215104758591923818947441465813939827252468298458501512274934213283394474929252890272815322072728121545402142127571518643073412545552919444768620193923721115040874821490498192845163014782819480348378252338278631734877270049886059699056015701542491308767095812631609792009922308416690626638089323812382387729710604396893335711577183169675469709449341880762946125460470722355849832821059916566355909", 10)
	T    = 1048576 // 2^20
)

type Claim struct {
	N, X, Y, V *big.Int
	T          int
}

func VDF(g *big.Int) (*big.Int, []*big.Int) {
	expList := []*big.Int{new(big.Int).Set(g)}
	y := new(big.Int).Set(g)
	two := big.NewInt(2)

	for i := 0; i < T; i++ {
		y.Exp(y, two, N)
		expList = append(expList, new(big.Int).Set(y))
	}

	return y, expList
}

func Evaluate(expList []*big.Int, exp, n *big.Int) *big.Int {
	res := big.NewInt(1)
	i := 0
	zero := big.NewInt(0)
	one := big.NewInt(1)

	for exp.Cmp(zero) > 0 {
		if exp.Bit(0) == 1 {
			res.Mul(res, expList[i])
			res.Mod(res, n)
		}
		exp.Rsh(exp, 1)
		i++
	}

	return res
}

func HashETH128(args ...*big.Int) *big.Int {
	h := sha3.New256()
	for _, arg := range args {
		h.Write(arg.Bytes())
	}
	return new(big.Int).SetBytes(h.Sum(nil)[:16])
}

func GenSingleHalvingProof(claim Claim) Claim {
	r := HashETH128(claim.X, claim.Y, claim.V)
	xPrime := new(big.Int).Exp(claim.X, r, claim.N)
	xPrime.Mul(xPrime, claim.V)
	xPrime.Mod(xPrime, claim.N)

	yPrime := new(big.Int).Exp(claim.V, r, claim.N)
	yPrime.Mul(yPrime, claim.Y)
	yPrime.Mod(yPrime, claim.N)

	tHalf := util.CalTHalf(claim.T)
	v := util.CalV(claim.N, xPrime, tHalf)

	return Claim{
		N: claim.N,
		X: xPrime,
		Y: yPrime,
		T: tHalf,
		V: v,
	}
}

func GenRecursiveHalvingProof(claim Claim) []Claim {
	proofList := []Claim{claim}

	for claim.T > 1 {
		claim = GenSingleHalvingProof(claim)
		proofList = append(proofList, claim)
	}

	return proofList
}