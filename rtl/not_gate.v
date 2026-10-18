//==============================================================================
// Module  : not_gate
// Purpose : Inverter (y = ~a)
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module not_gate (
    input  wire a,
    output wire y
);

assign y = ~a;

endmodule
