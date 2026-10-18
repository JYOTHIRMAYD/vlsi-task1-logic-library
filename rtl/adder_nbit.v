//==============================================================================
// Module  : adder_nbit
// Purpose : Parameterized N-bit ripple carry adder (generate loop)
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module adder_nbit #(
    parameter N = 8
) (
    input  wire [N-1:0] a,
    input  wire [N-1:0] b,
    input  wire         cin,
    output wire [N-1:0] sum,
    output wire         cout
);

wire [N:0] carry;          // carry[0] = cin, carry[N] = cout
assign carry[0] = cin;

genvar i;
generate
    for (i = 0; i < N; i = i + 1) begin : g_fa
        full_adder fa (
            .a   (a[i]),
            .b   (b[i]),
            .cin (carry[i]),
            .sum (sum[i]),
            .cout(carry[i+1])
        );
    end
endgenerate

assign cout = carry[N];

endmodule
