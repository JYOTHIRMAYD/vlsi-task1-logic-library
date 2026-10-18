# Digital Arithmetic Logic Circuit Library - build & simulation flow
# Usage:  make            -> run every testbench
#         make run T=tb_full_adder
#         make wave T=tb_ripple_carry_adder_4bit   (opens GTKWave)
#         make clean

IVERILOG ?= iverilog
VVP      ?= vvp
RTL      := $(wildcard rtl/*.v)
TESTS    := tb_logic_gates tb_half_adder tb_full_adder tb_mux2to1 tb_mux4to1 \
            tb_ripple_carry_adder_4bit tb_adder_nbit

.PHONY: all run wave clean lint
all: $(addprefix run_,$(TESTS))

sim/%.vvp: tb/%.v $(RTL)
	@mkdir -p sim
	$(IVERILOG) -g2005 -Wall -o $@ $< $(RTL)

run_%: sim/%.vvp
	$(VVP) $<

run: sim/$(T).vvp
	$(VVP) $<

wave: run
	gtkwave sim/$(T).vcd &

lint:
	$(IVERILOG) -g2005 -Wall -o /dev/null $(RTL)

clean:
	rm -f sim/*.vvp sim/*.vcd
