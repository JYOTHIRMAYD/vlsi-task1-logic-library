//==============================================================================
// Testbench : tb_logic_gates  (AND, OR, XOR, NAND, NOR, XNOR, NOT)
// Method    : exhaustive stimulus + self-checking comparison with !==
//==============================================================================
`timescale 1ns/1ps
module tb_logic_gates;

reg  a, b;
wire y_and, y_or, y_xor, y_nand, y_nor, y_xnor, y_not;

integer i;
integer errors;

and_gate  u_and  (.a(a), .b(b), .y(y_and));
or_gate   u_or   (.a(a), .b(b), .y(y_or));
xor_gate  u_xor  (.a(a), .b(b), .y(y_xor));
nand_gate u_nand (.a(a), .b(b), .y(y_nand));
nor_gate  u_nor  (.a(a), .b(b), .y(y_nor));
xnor_gate u_xnor (.a(a), .b(b), .y(y_xnor));
not_gate  u_not  (.a(a),         .y(y_not));

task check;
    input        actual;
    input        expected;
    input [47:0] name;       // up to 6 ASCII characters
    begin
        if (actual !== expected) begin
            $display("  FAIL %0s: a=%b b=%b got=%b expected=%b", name, a, b, actual, expected);
            errors = errors + 1;
        end
    end
endtask

initial begin
    $dumpfile("sim/tb_logic_gates.vcd");
    $dumpvars(0, tb_logic_gates);
    errors = 0;
    $display(" a b | AND OR XOR NAND NOR XNOR | NOT(a)");
    for (i = 0; i < 4; i = i + 1) begin
        {a, b} = i[1:0];
        #10;
        $display(" %b %b |  %b   %b   %b    %b    %b    %b   |   %b",
                 a, b, y_and, y_or, y_xor, y_nand, y_nor, y_xnor, y_not);
        check(y_and,  a & b,     "AND");
        check(y_or,   a | b,     "OR");
        check(y_xor,  a ^ b,     "XOR");
        check(y_nand, ~(a & b),  "NAND");
        check(y_nor,  ~(a | b),  "NOR");
        check(y_xnor, ~(a ^ b),  "XNOR");
        check(y_not,  ~a,        "NOT");
    end
    if (errors == 0) $display("RESULT: tb_logic_gates PASSED");
    else             $display("RESULT: tb_logic_gates FAILED (%0d errors)", errors);
    #10 $finish;
end

endmodule
