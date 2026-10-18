//==============================================================================
// Module  : mux4to1
// Purpose : 4:1 multiplexer using a combinational always block
// Style   : Verilog-2001, synthesizable, no delays in RTL
//==============================================================================
`timescale 1ns/1ps

module mux4to1 (
    input  wire       d0,
    input  wire       d1,
    input  wire       d2,
    input  wire       d3,
    input  wire [1:0] sel,
    output reg        y
);

// Full sensitivity list (@*) and default branch -> no inferred latch
always @(*) begin
    case (sel)
        2'b00:   y = d0;
        2'b01:   y = d1;
        2'b10:   y = d2;
        2'b11:   y = d3;
        default: y = 1'bx;
    endcase
end

endmodule
