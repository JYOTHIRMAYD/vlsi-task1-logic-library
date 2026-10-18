# Digital Arithmetic Logic Circuit Library Using Verilog HDL

**VLSI Design & Semiconductor Engineering Internship - Task 1 (Sumerix Global)**
Author: **T R JYOTHIRMAY DIKSHITH** | Intern ID: **SG 2884** | Date: **18 October 2026**

A reusable library of basic combinational digital circuits written in synthesizable Verilog-2001, each with a
self-checking testbench, simulated with **Icarus Verilog** and inspected in **GTKWave**.
These modules are the building blocks for the later ALU / RISC-processor tasks.

## Library contents

| Module | File | Description | Testbench |
|---|---|---|---|
| `and_gate`, `or_gate`, `xor_gate`, `nand_gate`, `nor_gate`, `xnor_gate`, `not_gate` | `rtl/*_gate.v` | Basic gates | `tb_logic_gates.v` |
| `half_adder` | `rtl/half_adder.v` | sum = a^b, carry = a&b | `tb_half_adder.v` |
| `full_adder` | `rtl/full_adder.v` | Built from 2 half adders + OR | `tb_full_adder.v` |
| `mux2to1` | `rtl/mux2to1.v` | `y = sel ? b : a` (continuous assign) | `tb_mux2to1.v` |
| `mux4to1` | `rtl/mux4to1.v` | `always @(*)` + `case` | `tb_mux4to1.v` |
| `ripple_carry_adder_4bit` | `rtl/ripple_carry_adder_4bit.v` | 4 chained full adders | `tb_ripple_carry_adder_4bit.v` (all 512 vectors) |
| `adder_nbit #(N)` | `rtl/adder_nbit.v` | Parameterized N-bit adder using `generate` | `tb_adder_nbit.v` (N=8, N=16, directed + random) |

## Repository structure
```
.
|-- rtl/        Verilog design files
|-- tb/         Testbenches (self-checking: print PASS/FAIL)
|-- sim/        Generated .vvp / .vcd files (git-ignored)
|-- docs/       Diagrams, truth tables, K-maps, Project_Documentation.pdf, screenshots/
|-- scripts/    setup_env.sh, run_all.sh, linux_practice.sh, verify_model.py, figure/doc generators
|-- reports/    Simulation logs, Linux command report, daily progress log
|-- Makefile
`-- README.md
```

## Setup (Ubuntu 22.04/24.04 or WSL-Ubuntu)
```bash
bash scripts/setup_env.sh        # installs iverilog, gtkwave, git, make
iverilog -V | head -1            # verify
```

## Run the simulations
```bash
make                              # compile + run all 7 testbenches
make run T=tb_full_adder          # run one
make wave T=tb_ripple_carry_adder_4bit   # simulate, then open GTKWave
# or without make:
bash scripts/run_all.sh           # logs go to reports/, summary in reports/simulation_summary.txt
```
Manual flow for any testbench:
```bash
iverilog -g2005 -Wall -o sim/tb_full_adder.vvp tb/tb_full_adder.v rtl/*.v
vvp sim/tb_full_adder.vvp
gtkwave sim/tb_full_adder.vcd
```
Expected console result for every testbench: a final line `RESULT: <tb_name> PASSED`.

## Verification approach
* Every testbench is **self-checking** - outputs are compared against a behavioural expected value with `!==`
  (so `x`/`z` also count as failures) and an error counter is reported.
* Gates, half adder, full adder, 2:1 and 4:1 mux and the 4-bit RCA are tested **exhaustively**.
* The parameterized adder is tested at two widths with corner cases (0, all-ones, carry-out) plus 200 random vectors each.
* `scripts/verify_model.py` is an independent Python golden model of the same structures (no simulator needed).

## Design notes / coding standards followed
* Verilog-2001, ANSI port style, one module per file, file name = module name.
* `assign` for combinational logic; `always @(*)` with a `default` branch (no latches); blocking `=` in combinational code.
* No `#delay` or `initial` in RTL - those appear only in testbenches.
* Lower-case `snake_case` names, `_nbit` suffix for parameterized blocks.

## Documentation
See `docs/Project_Documentation.pdf` (ASIC vs FPGA, digital fundamentals, K-maps, gate diagrams, RTL block diagram,
simulation workflow, results) and `docs/truth_tables.md`, `docs/karnaugh_maps.md`.

## Results
| Testbench | Result |
|---|---|
| tb_logic_gates | PASSED |
| tb_half_adder | PASSED |
| tb_full_adder | PASSED |
| tb_mux2to1 | PASSED |
| tb_mux4to1 | PASSED |
| tb_ripple_carry_adder_4bit | PASSED |
| tb_adder_nbit | PASSED |

GTKWave screenshots: `docs/screenshots/`

## Future work
Building blocks for Task 2+ (sequential design, FSM, ALU) and the 32-bit RISC processor capstone.
