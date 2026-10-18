`timescale 1ns/1ps
module tb_half_adder;

reg  a, b;
wire sum, carry;
integer i, errors;

half_adder dut (.a(a), .b(b), .sum(sum), .carry(carry));

initial begin
    $dumpfile("sim/tb_half_adder.vcd");
    $dumpvars(0, tb_half_adder);
    errors = 0;
    $display(" a b | sum carry");
    for (i = 0; i < 4; i = i + 1) begin
        {a, b} = i[1:0];
        #10;
        $display(" %b %b |  %b    %b", a, b, sum, carry);
        if (sum   !== (a ^ b)) begin errors = errors + 1; $display("  FAIL sum");   end
        if (carry !== (a & b)) begin errors = errors + 1; $display("  FAIL carry"); end
    end
    if (errors == 0) $display("RESULT: tb_half_adder PASSED");
    else             $display("RESULT: tb_half_adder FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
