`timescale 1ns/1ps
module tb_mux4to1;

reg  [3:0] d;
reg  [1:0] sel;
wire       y;
integer i, errors;

mux4to1 dut (.d0(d[0]), .d1(d[1]), .d2(d[2]), .d3(d[3]), .sel(sel), .y(y));

initial begin
    $dumpfile("sim/tb_mux4to1.vcd");
    $dumpvars(0, tb_mux4to1);
    errors = 0;
    $display(" sel  d3d2d1d0 | y");
    for (i = 0; i < 64; i = i + 1) begin      // all 4 select values x 16 data patterns
        {sel, d} = i[5:0];
        #10;
        if (i % 5 == 0) $display("  %b   %b  | %b", sel, d, y);
        if (y !== d[sel]) begin
            errors = errors + 1;
            $display("  FAIL: sel=%b d=%b y=%b expected=%b", sel, d, y, d[sel]);
        end
    end
    if (errors == 0) $display("RESULT: tb_mux4to1 PASSED");
    else             $display("RESULT: tb_mux4to1 FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
