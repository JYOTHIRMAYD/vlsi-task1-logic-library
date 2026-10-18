//==============================================================================
// Testbench : tb_adder_nbit  - same RTL, two different widths (N = 8, N = 16)
//==============================================================================
`timescale 1ns/1ps
module tb_adder_nbit;

reg  [7:0]  a8,  b8;   reg c8;   wire [7:0]  s8;   wire co8;
reg  [15:0] a16, b16;  reg c16;  wire [15:0] s16;  wire co16;
reg  [8:0]  exp8;
reg  [16:0] exp16;
integer i, errors;

adder_nbit #(.N(8))  u8  (.a(a8),  .b(b8),  .cin(c8),  .sum(s8),  .cout(co8));
adder_nbit #(.N(16)) u16 (.a(a16), .b(b16), .cin(c16), .sum(s16), .cout(co16));

task check8;
    begin
        #5;
        exp8 = a8 + b8 + c8;
        if ({co8, s8} !== exp8) begin
            errors = errors + 1;
            $display("  FAIL N=8 : %0d + %0d + %0d -> %0d (expected %0d)", a8, b8, c8, {co8, s8}, exp8);
        end
    end
endtask

task check16;
    begin
        #5;
        exp16 = a16 + b16 + c16;
        if ({co16, s16} !== exp16) begin
            errors = errors + 1;
            $display("  FAIL N=16: %0d + %0d + %0d -> %0d (expected %0d)", a16, b16, c16, {co16, s16}, exp16);
        end
    end
endtask

initial begin
    $dumpfile("sim/tb_adder_nbit.vcd");
    $dumpvars(0, tb_adder_nbit);
    errors = 0;

    // ---- Directed corner cases ----
    a8 = 8'd0;   b8 = 8'd0;   c8 = 0; check8;
    a8 = 8'd255; b8 = 8'd1;   c8 = 0; check8;   // overflow -> carry out
    a8 = 8'd255; b8 = 8'd255; c8 = 1; check8;   // max
    a8 = 8'd100; b8 = 8'd27;  c8 = 1; check8;
    a16 = 16'd0;      b16 = 16'd0;      c16 = 0; check16;
    a16 = 16'hFFFF;   b16 = 16'd1;      c16 = 0; check16;
    a16 = 16'hFFFF;   b16 = 16'hFFFF;   c16 = 1; check16;
    a16 = 16'h1234;   b16 = 16'h4321;   c16 = 1; check16;

    // ---- Random cases ----
    for (i = 0; i < 200; i = i + 1) begin
        a8  = $random; b8  = $random; c8  = $random; check8;
        a16 = $random; b16 = $random; c16 = $random; check16;
    end

    if (errors == 0) $display("RESULT: tb_adder_nbit PASSED");
    else             $display("RESULT: tb_adder_nbit FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
