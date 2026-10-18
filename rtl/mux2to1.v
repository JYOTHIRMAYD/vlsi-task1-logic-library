//==============================================================================
// Module  : mux2to1
// Purpose : 2:1 multiplexer  (y = sel ? b : a)
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module mux2to1 (
    input  wire a,      // selected when sel = 0
    input  wire b,      // selected when sel = 1
    input  wire sel,
    output wire y
);

assign y = sel ? b : a;

endmodule
