// File: go/pkg/util/util.go

package util

import (
	"math/big"
)

func CalTHalf(T int) int {
	if T%2 == 0 {
		return T / 2
	}
	return (T + 1) / 2
}

func CalV(N, x *big.Int, tHalf int) *big.Int {
	exp := new(big.Int).Exp(big.NewInt(2), big.NewInt(int64(tHalf)), nil)
	return new(big.Int).Exp(x, exp, N)
}