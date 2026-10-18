#!/usr/bin/env bash
# Compile and run every testbench, save logs to reports/, print a PASS/FAIL summary.
set -u
cd "$(dirname "$0")/.."
mkdir -p sim reports
TESTS="tb_logic_gates tb_half_adder tb_full_adder tb_mux2to1 tb_mux4to1 tb_ripple_carry_adder_4bit tb_adder_nbit"
: > reports/simulation_summary.txt
for t in $TESTS; do
    iverilog -g2005 -Wall -o sim/$t.vvp tb/$t.v rtl/*.v || { echo "COMPILE ERROR in $t"; exit 1; }
    vvp sim/$t.vvp | tee reports/$t.log
    grep "RESULT" reports/$t.log >> reports/simulation_summary.txt
done
echo; echo "================ SUMMARY ================"
cat reports/simulation_summary.txt
