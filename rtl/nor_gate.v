//==============================================================================
// Module  : nor_gate
// Purpose : 2-input NOR gate  (y = ~(a | b))
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module nor_gate (
    input  wire a,
    input  wire b,
    output wire y
);

assign y = ~(a | b);

endmodule
