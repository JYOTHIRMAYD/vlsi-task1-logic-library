//==============================================================================
// Module  : half_adder
// Purpose : Half adder: sum = a^b, carry = a&b
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module half_adder (
    input  wire a,
    input  wire b,
    output wire sum,
    output wire carry
);

assign sum   = a ^ b;
assign carry = a & b;

endmodule
