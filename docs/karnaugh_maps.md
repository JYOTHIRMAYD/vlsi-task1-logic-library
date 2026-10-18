# Karnaugh Map Solutions

Gray-code ordering is used on both axes. Each figure is in `docs/diagrams/`.

## 1. Full adder - SUM  (`kmap_fa_sum.png`)
Minterms: m(1,2,4,7). All four 1-cells are isolated (checkerboard) so no grouping is possible.
`SUM = A'B'Cin + A'BCin' + AB'Cin' + ABCin = A XOR B XOR Cin`

## 2. Full adder - COUT  (`kmap_fa_cout.png`)
Minterms: m(3,5,6,7). Three pairs: `AB` (m6,m7), `A.Cin` (m5,m7), `B.Cin` (m3,m7).
`COUT = AB + A.Cin + B.Cin`  (majority function)  
Equivalent form used in RTL: `COUT = AB + Cin.(A XOR B)`

## 3. 2:1 multiplexer  (`kmap_mux2.png`)
Variables (S,A,B), Y = S ? B : A. Minterms: m(2,3,5,7).
Pairs: `S'.A` (m2,m3) and `S.B` (m5,m7). The consensus term `A.B` (m3,m7) is redundant (it only removes a static-1 hazard).
`Y = S'A + SB`

## 4. BCD-invalid detector  (`kmap_bcd_invalid.png`)
Output is 1 when the 4-bit input is not a valid BCD digit (10-15). Minterms: m(10,11,12,13,14,15).
Quad `A.B` (m12-15) and quad `A.C` (m10,11,14,15).
`F = AB + AC = A(B + C)`

## 5. Half adder (2 variables - no map needed)
`SUM = A'B + AB' = A XOR B`, `CARRY = AB`

All four simplified expressions above were checked against their truth tables for every input
combination by `scripts/verify_model.py`.
