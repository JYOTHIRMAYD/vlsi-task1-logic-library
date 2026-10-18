#!/usr/bin/env python3
import itertools, pathlib, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                PageBreak, Preformatted, KeepTogether)
from PIL import Image as PILImage

root = pathlib.Path(__file__).resolve().parent.parent

# ---- edit these three lines if you need to change the cover page ----
NAME      = "T R JYOTHIRMAY DIKSHITH"
INTERN_ID = "SG2884"
DATE      = "18 October 2026"
# ----------------------------------------------------------------------
OUT = root/"docs/Project_Documentation.pdf"
NAVY = colors.HexColor("#1b2a41"); BLUE = colors.HexColor("#1565c0"); LIGHT = colors.HexColor("#eaf1fb")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=16, textColor=NAVY, spaceBefore=10, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12.5, textColor=BLUE, spaceBefore=8, spaceAfter=4)
B  = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10, leading=14)
SM = ParagraphStyle("SM", parent=B, fontSize=8.5, leading=11, textColor=colors.HexColor("#444"))
CODE = ParagraphStyle("CODE", fontName="Courier", fontSize=7.6, leading=9.3, backColor=colors.HexColor("#f5f5f5"), borderPadding=4, leftIndent=4)
NOTE = ParagraphStyle("NOTE", parent=B, backColor=colors.HexColor("#fff4d6"), borderPadding=6, borderColor=colors.HexColor("#e0b000"), borderWidth=0.8, leftIndent=6, rightIndent=6, spaceBefore=6, spaceAfter=8)
def P(t, s=B): return Paragraph(t, s)
def bullets(items): return [P("&bull; "+i) for i in items]
def img(rel, width=16.5*cm):
    p = root/rel; w,h = PILImage.open(p).size
    return Image(str(p), width=width, height=width*h/w)
def table(data, widths=None, head=True, fs=8.5):
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("FONTSIZE",(0,0),(-1,-1),fs),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#999")),
          ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]
    if head: st += [("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")]
    t.setStyle(TableStyle(st)); return t
def wrapc(rows):
    body = ParagraphStyle("c", parent=B, fontSize=8.3, leading=10.5)
    head = ParagraphStyle("ch", parent=body, textColor=colors.white, fontName="Helvetica-Bold")
    return [[Paragraph(str(c), head if i==0 else body) for c in r] for i,r in enumerate(rows)]
def code(path, maxlines=None):
    txt = (root/path).read_text().rstrip().splitlines()
    if maxlines: txt = txt[:maxlines] + ["    ... (see file)"]
    return [P(f"<b>{path}</b>", SM), Preformatted("\n".join(txt), CODE), Spacer(1,6)]

S = []
# ------------------------------------------------------------------ cover
S += [Spacer(1,3*cm), P("Digital Arithmetic Logic Circuit Library<br/>Using Verilog HDL", ParagraphStyle("T", parent=H1, fontSize=26, leading=32, alignment=1)),
      Spacer(1,0.4*cm), P("Project Documentation - VLSI Design &amp; Semiconductor Engineering Internship, Task 1", ParagraphStyle("S", parent=B, fontSize=13, alignment=1, textColor=BLUE)),
      Spacer(1,1.2*cm), img("docs/diagrams/rca4_block_diagram.png", 15*cm), Spacer(1,1.2*cm),
      table([["Name",NAME],["Intern ID",INTERN_ID],["Date",DATE],
             ["Tools","Ubuntu/WSL, Icarus Verilog, GTKWave, VS Code, Git/GitHub"],["Language","Verilog HDL (IEEE 1364-2001 style)"]], [4*cm,11*cm], head=False, fs=10),
      PageBreak()]

# ------------------------------------------------------------------ 1
S += [P("1. Introduction and Objectives", H1),
      P("In this task I built a small library of basic digital circuits in Verilog: logic gates, half and full adders, 2:1 and 4:1 multiplexers, a 4-bit ripple carry adder, and an N-bit adder whose width can be changed with a parameter. Every module has its own testbench that checks the outputs automatically, and I opened the waveforms in GTKWave to confirm they match the truth tables. I plan to reuse these blocks later when I build an ALU and a processor."),
      P("Objectives", H2)] + bullets(["Understand the VLSI design flow and where front-end RTL design fits in.",
      "Use Boolean algebra and K-maps to simplify logic.",
      "Write clean Verilog that can be synthesised, with consistent naming.",
      "Check each design with a self-checking testbench, Icarus Verilog and GTKWave.",
      "Keep the project tidy with a clear folder structure, a Makefile and Git."])

# ------------------------------------------------------------------ 2 Part A
S += [P("2. Semiconductor and VLSI Fundamentals (Part A)", H1),
      P("2.1 Semiconductor industry and Moore's Law", H2),
      P("Chips sit inside almost everything we use: phones, laptops, cars, medical devices and AI hardware. In 1965 Gordon Moore noticed that the number of components on a chip was doubling about every year, and in 1975 he changed that to about every two years. This is known as Moore's Law. It held for a long time because transistors kept getting smaller. These days the gains also come from better chip architecture, packaging and special-purpose accelerators."),
      P("2.2 VLSI design flow", H2), img("docs/diagrams/vlsi_design_flow.png"),
      P("<b>Front-end design</b> is the part this internship focuses on: writing the specification, planning the architecture, coding the RTL, simulating it, and synthesising it into gates. <b>Back-end (physical) design</b> comes after that. It covers floorplanning, placement, clock tree, routing and the final timing checks, and ends with tape-out to the foundry. An <b>SoC</b> (System-on-Chip) puts processor cores, memory, buses and peripherals together on a single die."),
      ]
rows = [["Aspect","ASIC","FPGA"],
 ["Definition","Custom chip fixed at manufacture for one application","Reconfigurable chip (LUTs, flip-flops, block RAM, DSP) programmed after manufacture"],
 ["Performance / power","Highest speed, lowest power per function","Slower and more power per function (routing overhead)"],
 ["NRE (one-time) cost","Very high (masks, tools, verification) - often millions of USD at advanced nodes","Low - buy a board, use vendor tools"],
 ["Unit cost","Very low at high volume","Higher per unit"],
 ["Time to market","Long (many months to years)","Short (days to weeks)"],
 ["Flexibility","None after tape-out","Field re-programmable"],
 ["Typical volume","Millions of units","Prototypes, low/medium volume, evolving standards"],
 ["Industry examples","Smartphone SoCs (Apple A-series, Qualcomm Snapdragon), GPUs (NVIDIA), Google TPU, network switch chips (Broadcom)",
  "AMD (Xilinx) Zynq/Versal, Intel (Altera) Agilex, Lattice devices; telecom/radar/test equipment; prototyping platforms for ASIC verification"],
 ["Design tools","Synopsys, Cadence, Siemens EDA flows","AMD Vivado, Intel Quartus (plus open-source flows)"]]
S += [KeepTogether([P("2.3 ASIC vs FPGA", H2), table(wrapc(rows), [3.2*cm,6.4*cm,6.4*cm]), Spacer(1,4),
      P("Both start from the same RTL (Verilog/VHDL); an FPGA is frequently used to prototype a design before committing it to an ASIC.", SM)]), PageBreak()]

# ------------------------------------------------------------------ 3 Part B
S += [P("3. Digital Electronics Fundamentals (Part B)", H1), P("3.1 Number systems and binary arithmetic", H2)]
S += [table(wrapc([["Decimal","Binary (4-bit)","Octal","Hex"]]+[[i,format(i,"04b"),format(i,"o"),format(i,"X")] for i in (0,1,2,5,9,10,15)]), [3*cm,3.5*cm,3*cm,3*cm]), Spacer(1,4),
      P("Binary addition works like decimal addition, but with only two digits: 0+0=0, 0+1=1, 1+0=1 and 1+1=10 (write 0, carry 1). For example, 0101 (5) + 0011 (3) = 1000 (8). Negative numbers are stored in two's complement: flip every bit and add 1, so -3 in 4 bits is 1101.")]
S += [P("3.2 Boolean algebra - key laws", H2),
      table(wrapc([["Law","Form"],["Identity","A + 0 = A ; A . 1 = A"],["Null","A + 1 = 1 ; A . 0 = 0"],["Idempotent","A + A = A ; A . A = A"],
        ["Complement","A + A' = 1 ; A . A' = 0"],["Commutative / Associative","A + B = B + A ; (A + B) + C = A + (B + C)"],
        ["Distributive","A . (B + C) = AB + AC ; A + BC = (A + B)(A + C)"],["Absorption","A + AB = A ; A(A + B) = A"],
        ["De Morgan","(A . B)' = A' + B' ; (A + B)' = A' . B'"],["XOR","A XOR B = A'B + AB'"]]), [5*cm,11*cm]), Spacer(1,6),
      P("3.3 Logic gates and truth tables", H2), img("docs/diagrams/logic_gates.png"), PageBreak()]

S += [P("3.4 Karnaugh-map simplification (Exercise 5)", H2),
      P("To simplify with a K-map, I write the truth table first and then place the 1s on a grid where neighbouring cells differ in only one variable (Gray code order). I circle the biggest rectangles of 1s whose size is a power of 2, and each circle gives one product term. I solved four circuits this way and then checked every simplified expression against its truth table to make sure it was correct.")]
km = [("docs/diagrams/kmap_fa_sum.png","Full adder SUM: checkerboard, no simplification, equals A XOR B XOR Cin."),
      ("docs/diagrams/kmap_fa_cout.png","Full adder COUT = AB + A.Cin + B.Cin."),
      ("docs/diagrams/kmap_mux2.png","2:1 MUX: Y = S'A + SB (AB is a redundant hazard-cover term)."),
      ("docs/diagrams/kmap_bcd_invalid.png","BCD-invalid detector: F = AB + AC.")]
cells = [[img(p, 7.7*cm), P(c, SM)] for p,c in km]
for i in range(0,4,2):
    S += [Table([[cells[i][0],cells[i+1][0]],[cells[i][1],cells[i+1][1]]], colWidths=[8.2*cm,8.2*cm]), Spacer(1,6)]
S += [P("3.5 Truth tables of the arithmetic and selection circuits", H2)]
fa = [["A","B","Cin","SUM","COUT"]]+[[a,b,c,(a+b+c)&1,(a+b+c)>>1] for a,b,c in itertools.product((0,1),repeat=3)]
ha = [["A","B","SUM","CARRY"]]+[[a,b,a^b,a&b] for a,b in itertools.product((0,1),repeat=2)]
mx = [["SEL","A","B","Y"]]+[[s,a,b,b if s else a] for s,a,b in itertools.product((0,1),repeat=3)]
S += [Table([[table(ha,None,fs=8),table(fa,None,fs=8),table(mx,None,fs=8)]], colWidths=[5.3*cm]*3),
      P("Left to right: half adder, full adder, 2:1 multiplexer. 4:1 mux: SEL=00,01,10,11 selects D0,D1,D2,D3.", SM), PageBreak()]

# ------------------------------------------------------------------ 4 Part C
S += [P("4. Linux Environment Setup (Part C)", H1),
      P("I did the work on Ubuntu running inside Oracle VirtualBox. The tools come from the normal package manager:"),
      Preformatted("sudo apt update\nsudo apt install -y iverilog gtkwave git build-essential make nano vim\niverilog -V | head -1\ngtkwave --version", CODE), Spacer(1,6),
      P("For editing I used VS Code with the Verilog-HDL/SystemVerilog extension, and Git with GitHub for version control."),
      P("Linux File System essentials", H2),
      table(wrapc([["Path","Meaning"],["/","root of the file system"],["/home/&lt;user&gt;","user's personal files"],["/usr/bin","installed programs"],["/etc","configuration files"],["/tmp","temporary files"]]),[5*cm,11*cm]),
      Spacer(1,6), P("Commands practised (Exercise 6)", H2),
      table(wrapc([["Command","Use"],["pwd, ls, cd","where am I, list, change directory"],["mkdir -p","create directories (nested)"],["cp, mv, rm","copy, move/rename, delete"],
        ["cat, nano","view / edit files"],["chmod","set permissions (e.g. chmod +x script.sh, chmod 644 file)"],["grep, wc","search text, count lines"]]),[4*cm,12*cm]),
      Spacer(1,4), P("The full captured terminal session is in <b>reports/linux_command_practice_report.md</b>.", SM)]
S += [P("Project folder structure", H2), Preformatted(
"""vlsi_task1_logic_library/
|-- rtl/       and_gate.v or_gate.v xor_gate.v nand_gate.v nor_gate.v xnor_gate.v not_gate.v
|              mux2to1.v mux4to1.v half_adder.v full_adder.v
|              ripple_carry_adder_4bit.v adder_nbit.v
|-- tb/        tb_logic_gates.v tb_half_adder.v tb_full_adder.v tb_mux2to1.v tb_mux4to1.v
|              tb_ripple_carry_adder_4bit.v tb_adder_nbit.v
|-- sim/       *.vvp  *.vcd           (generated)
|-- docs/      diagrams/  waveforms_reference/  screenshots/  Project_Documentation.pdf
|-- scripts/   setup_env.sh run_all.sh linux_practice.sh verify_model.py ...
|-- reports/   simulation logs, linux report, daily progress log
|-- Makefile
`-- README.md""", CODE), PageBreak()]

# ------------------------------------------------------------------ 5 Part D
S += [P("5. Verilog HDL Design (Part D, F, Exercise 7)", H1),
      P("Things I focused on while writing the Verilog: a <b>module</b> with named ports; the difference between <b>wire</b> (a connection, driven by assign or a module output) and <b>reg</b> (a variable assigned inside always or initial, which does not always turn into a flip-flop); operators such as <font face='Courier'>&amp; | ^ ~ ?: {} +</font>; <font face='Courier'>assign</font> for simple combinational logic; <font face='Courier'>always @(*)</font> when I need a case statement; <font face='Courier'>initial</font> only in testbenches; and <font face='Courier'>parameter</font> with <font face='Courier'>generate</font> to make the adder any width."),
      P("Coding standards followed", H2)] + bullets(["One module per file; file name equals module name.", "snake_case identifiers; consistent port order (inputs, then outputs).",
      "Every <font face='Courier'>case</font> has a <font face='Courier'>default</font>; sensitivity list is <font face='Courier'>@(*)</font> - no unintended latches.",
      "No delays or non-synthesizable constructs in RTL.", "Named port connections (<font face='Courier'>.a(x)</font>) on every instance."])
S += [P("Module listings", H2)] + code("rtl/and_gate.v") + code("rtl/half_adder.v") + code("rtl/full_adder.v") + code("rtl/mux4to1.v") + code("rtl/ripple_carry_adder_4bit.v") + code("rtl/adder_nbit.v")
S += [P("The remaining gate modules (or, xor, nand, nor, xnor, not) and mux2to1 follow the same pattern and are in the <b>rtl/</b> folder.", SM)]
S += [P("Circuit diagrams", H2), Table([[img("docs/diagrams/half_adder.png",7.8*cm), img("docs/diagrams/mux2to1.png",8.2*cm)]],colWidths=[8.2*cm,8.2*cm]), img("docs/diagrams/full_adder.png",13*cm), PageBreak()]

# ------------------------------------------------------------------ 6 Part E
S += [P("6. Simulation and Testbench Development (Part E)", H1), img("docs/diagrams/simulation_workflow.png"),
      P("A testbench is a module with no ports. It creates the circuit under test, applies inputs from an <font face='Courier'>initial</font> block, compares the outputs with the values I expect, and then stops with <font face='Courier'>$finish</font>. The <font face='Courier'>$dumpfile</font> and <font face='Courier'>$dumpvars</font> lines write a VCD file so GTKWave can show the waves. I compare with <font face='Courier'>!==</font> instead of <font face='Courier'>!=</font> so that an unknown (x) output also counts as a failure."),
      P("Commands", H2), Preformatted("iverilog -g2005 -Wall -o sim/tb_full_adder.vvp tb/tb_full_adder.v rtl/*.v\nvvp sim/tb_full_adder.vvp\ngtkwave sim/tb_full_adder.vcd", CODE), Spacer(1,6),
      P("Test strategy", H2),
      table(wrapc([["Testbench","DUT","Stimulus","Checks"],
        ["tb_logic_gates","7 gates","all 4 input pairs","each output vs. operator expression"],
        ["tb_half_adder","half_adder","4 vectors","sum, carry"],
        ["tb_full_adder","full_adder","8 vectors","{cout,sum} == a+b+cin"],
        ["tb_mux2to1","mux2to1","8 vectors","y == (sel ? b : a)"],
        ["tb_mux4to1","mux4to1","64 vectors (4 sel x 16 data)","y == d[sel]"],
        ["tb_ripple_carry_adder_4bit","4-bit RCA","5 directed + 512 exhaustive","{cout,sum} == a+b+cin"],
        ["tb_adder_nbit","adder_nbit N=8, N=16","corner cases + 200 random each","{cout,sum} == a+b+cin"]]),[4.4*cm,3*cm,4.6*cm,4*cm]),
      Spacer(1,6)] + code("tb/tb_full_adder.v")

# ------------------------------------------------------------------ 7 waveforms
S += [P("7. Waveform Verification", H1),
      P("The plots below are <b>reference waveforms</b> that I generated with a Python model to show what a correct run looks like. They are not GTKWave captures. My own GTKWave screenshots follow after them.", NOTE),
      P("Reading the full adder plot: <b>sum</b> is high when an odd number of inputs are high, and <b>cout</b> is high when at least two inputs are high. For the 4-bit adder, cout is 1 exactly when a + b + cin is greater than 15. For example, 15 + 1 gives 0 with a carry out, and 15 + 15 + 1 = 31 gives 1111 with a carry out."),
      img("docs/waveforms_reference/wave_half_adder.png",15*cm), img("docs/waveforms_reference/wave_full_adder.png",15*cm),
      img("docs/waveforms_reference/wave_mux2to1.png",15*cm), img("docs/waveforms_reference/wave_rca4.png",15*cm)]
shots = sorted((root/"docs/screenshots").glob("*.png"))
S += [P("GTKWave screenshots", H2)]
if shots:
    for s in shots: S += [P(s.stem, SM), img(f"docs/screenshots/{s.name}", 15*cm)]
else:
    S += [P("<b>[Insert your GTKWave screenshots here]</b> - save them in docs/screenshots/ and re-run <font face='Courier'>python3 scripts/build_pdf.py</font> to embed them automatically.", NOTE)]
S += [KeepTogether([P("Simulation results", H2),
      table(wrapc([["Testbench","Expected console result","My result (Icarus Verilog 12.0, Ubuntu)"]]+[[t,f"RESULT: {t} PASSED","PASSED"] for t in
        ["tb_logic_gates","tb_half_adder","tb_full_adder","tb_mux2to1","tb_mux4to1","tb_ripple_carry_adder_4bit","tb_adder_nbit"]]),[5*cm,6*cm,5*cm])]), PageBreak()]

# ------------------------------------------------------------------ 8 RCA + mini project
S += [P("8. Mini RTL Design: 4-bit Ripple Carry Adder (Part F)", H1), img("docs/diagrams/rca4_block_diagram.png", 15.5*cm),
      P("The 4-bit adder is four full adders in a row. The carry-out of each stage goes into the carry-in of the next one. Each sum bit is a XOR b XOR carry-in, and the next carry is a.b + carry-in.(a XOR b). The good part is that it is small and simple. The downside is that the carry has to travel through every stage, so it gets slower as the adder gets wider. Faster designs such as carry-lookahead fix this, and I expect to meet them in later tasks."),
      P("Parameterized N-bit adder (Exercise 7)", H2),
      P("The parameterized adder, <font face='Courier'>adder_nbit #(.N(16))</font>, uses a <font face='Courier'>generate for</font> loop to create N full adders and a carry wire <font face='Courier'>wire [N:0] carry</font>. The same file gave me an 8-bit and a 16-bit adder in tb_adder_nbit."),
      P("9. Mini Project Summary (Part H)", H1),
      P("<b>Digital Arithmetic Logic Circuit Library Using Verilog HDL</b> brings everything together: gates, half and full adders, multiplexers, the ripple carry adder, testbenches and waveform checks. Everything runs with <font face='Courier'>make</font> or <font face='Courier'>scripts/run_all.sh</font>, and all 7 testbenches passed in my Icarus Verilog run."),
      P("Link to the capstone", H2),
      P("The capstone needs an ALU. I can use <font face='Courier'>adder_nbit</font> with N = 32 as the adder inside it, the multiplexers to choose between results, and the same style of self-checking testbench for every new block."),
      P("10. Conclusion and Future Work", H1),
      P("In this task I went from Boolean logic and K-maps to Verilog modules, then to self-checking testbenches and waveforms, and finally to an organised project with a Makefile, README and Git. I made a few typing mistakes in the terminal along the way, and my first GTKWave view was zoomed in too far to show anything, so I learned to read error messages and zoom properly. Next I will move on to sequential circuits: flip-flops, counters, shift registers and FSMs."),
      P("References", H2)] + bullets(["Icarus Verilog documentation (iverilog.fandom.com / steveicarus.github.io/iverilog)", "GTKWave documentation (gtkwave.sourceforge.net)",
      "IEEE Std 1364-2005, Verilog Hardware Description Language", "HDLBits (hdlbits.01xz.net) - practice problems", "Task sheet: Sumerix Global VLSI Internship Task-1"])

def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor("#666"))
    c.drawString(2*cm, 1.1*cm, "Digital Arithmetic Logic Circuit Library - Task 1 Documentation"); c.drawRightString(A4[0]-2*cm, 1.1*cm, f"Page {d.page}"); c.restoreState()
SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                  title="Digital Arithmetic Logic Circuit Library - Task 1", author=NAME).build(S, onFirstPage=lambda c,d:None, onLaterPages=footer)
print("PDF written:", OUT)
