`timescale 1ns/1ps
module tb_mux2to1;

reg  a, b, sel;
wire y;
integer i, errors;

mux2to1 dut (.a(a), .b(b), .sel(sel), .y(y));

initial begin
    $dumpfile("sim/tb_mux2to1.vcd");
    $dumpvars(0, tb_mux2to1);
    errors = 0;
    $display(" sel a b | y");
    for (i = 0; i < 8; i = i + 1) begin
        {sel, a, b} = i[2:0];
        #10;
        $display("  %b  %b %b | %b", sel, a, b, y);
        if (y !== (sel ? b : a)) begin
            errors = errors + 1;
            $display("  FAIL: sel=%b a=%b b=%b y=%b", sel, a, b, y);
        end
    end
    if (errors == 0) $display("RESULT: tb_mux2to1 PASSED");
    else             $display("RESULT: tb_mux2to1 FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
