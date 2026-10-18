//==============================================================================
// Testbench : tb_ripple_carry_adder_4bit
// Method    : exhaustive (16 x 16 x 2 = 512 vectors) + self-check
//==============================================================================
`timescale 1ns/1ps
module tb_ripple_carry_adder_4bit;

reg  [3:0] a, b;
reg        cin;
wire [3:0] sum;
wire       cout;
reg  [4:0] expected;
integer ia, ib, ic, errors, count;

ripple_carry_adder_4bit dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

initial begin
    $dumpfile("sim/tb_ripple_carry_adder_4bit.vcd");
    $dumpvars(0, tb_ripple_carry_adder_4bit);
    errors = 0;
    count  = 0;
    // A few directed vectors first so the waveform is easy to read
    a = 4'd0;  b = 4'd0;  cin = 1'b0; #10;
    a = 4'd5;  b = 4'd3;  cin = 1'b0; #10;
    a = 4'd9;  b = 4'd6;  cin = 1'b1; #10;
    a = 4'd15; b = 4'd1;  cin = 1'b0; #10;   // carry out
    a = 4'd15; b = 4'd15; cin = 1'b1; #10;   // max: 31

    // Exhaustive sweep
    for (ia = 0; ia < 16; ia = ia + 1)
        for (ib = 0; ib < 16; ib = ib + 1)
            for (ic = 0; ic < 2; ic = ic + 1) begin
                a = ia; b = ib; cin = ic;
                #5;
                expected = a + b + cin;
                count = count + 1;
                if ({cout, sum} !== expected) begin
                    errors = errors + 1;
                    $display("  FAIL: %0d + %0d + %0d -> got %0d expected %0d",
                             a, b, cin, {cout, sum}, expected);
                end
            end

    $display("Vectors applied: %0d", count);
    if (errors == 0) $display("RESULT: tb_ripple_carry_adder_4bit PASSED");
    else             $display("RESULT: tb_ripple_carry_adder_4bit FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
