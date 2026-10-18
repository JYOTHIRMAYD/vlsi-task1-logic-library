#!/usr/bin/env python3
"""Golden-model self-check (pure Python, no simulator needed).
Mirrors the RTL structure (half adder -> full adder -> RCA -> N-bit adder) and checks
(1) all gate/mux/adder behaviour, (2) every simplified K-map expression vs. its truth table.
This does NOT replace the Verilog simulation - it validates the *logic* behind it."""
import itertools, random

def half_adder(a,b):          return a ^ b, a & b
def full_adder(a,b,cin):
    s1,c1 = half_adder(a,b); s,c2 = half_adder(s1,cin); return s, c1 | c2
def rca(a,b,cin,n):
    carry, out = cin, 0
    for i in range(n):
        s, carry = full_adder((a>>i)&1,(b>>i)&1,carry); out |= s<<i
    return out, carry
def mux2(a,b,sel): return b if sel else a
def mux4(d,sel):   return d[sel]

n_checks = 0
def ok(cond, msg):
    global n_checks; n_checks += 1
    assert cond, msg

for a,b in itertools.product((0,1),repeat=2):
    s,c = half_adder(a,b); ok(s==(a^b) and c==(a&b),"HA")
for a,b,c in itertools.product((0,1),repeat=3):
    s,co = full_adder(a,b,c); ok(2*co+s==a+b+c,"FA")
    ok(mux2(a,b,c)==(b if c else a),"MUX2")
for d in itertools.product((0,1),repeat=4):
    for sel in range(4): ok(mux4(d,sel)==d[sel],"MUX4")
for a,b,c in itertools.product(range(16),range(16),(0,1)):
    s,co = rca(a,b,c,4); ok((co<<4)|s==a+b+c,"RCA4")
for n in (1,4,8,16):
    for _ in range(2000):
        a,b,c = random.getrandbits(n),random.getrandbits(n),random.getrandbits(1)
        s,co = rca(a,b,c,n); ok((co<<n)|s==a+b+c,f"RCA{n}")

# ---- K-map simplifications -------------------------------------------------
NOT = lambda x: 1-x
kmaps = {
 "FA_sum":  (3, [1,2,4,7],      lambda A,B,C:   A^B^C),
 "FA_cout": (3, [3,5,6,7],      lambda A,B,C:   (A&B)|(A&C)|(B&C)),
 "MUX2_y":  (3, [2,3,5,7],      lambda S,A,B:   (NOT(S)&A)|(S&B)),
 "BCD_inv": (4, list(range(10,16)), lambda A,B,C,D: (A&B)|(A&C)),
}
for name,(nv,ms,f) in kmaps.items():
    for idx in range(2**nv):
        bits = [(idx>>(nv-1-k))&1 for k in range(nv)]
        ok(f(*bits)==(1 if idx in ms else 0), f"{name} m{idx}")
print(f"ALL {n_checks} MODEL CHECKS PASSED")
