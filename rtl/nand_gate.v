//==============================================================================
// Module  : nand_gate
// Purpose : 2-input NAND gate  (y = ~(a & b))
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module nand_gate (
    input  wire a,
    input  wire b,
    output wire y
);

assign y = ~(a & b);

endmodule
