`timescale 1ns/1ps
module tb_full_adder;

reg  a, b, cin;
wire sum, cout;
reg  [1:0] expected;     // {cout, sum}
integer i, errors;

full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

initial begin
    $dumpfile("sim/tb_full_adder.vcd");
    $dumpvars(0, tb_full_adder);
    errors = 0;
    $display(" a b cin | sum cout");
    for (i = 0; i < 8; i = i + 1) begin
        {a, b, cin} = i[2:0];
        #10;
        expected = a + b + cin;            // 2-bit context -> no overflow
        $display(" %b %b  %b  |  %b    %b", a, b, cin, sum, cout);
        if ({cout, sum} !== expected) begin
            errors = errors + 1;
            $display("  FAIL: got {cout,sum}=%b expected=%b", {cout, sum}, expected);
        end
    end
    if (errors == 0) $display("RESULT: tb_full_adder PASSED");
    else             $display("RESULT: tb_full_adder FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
