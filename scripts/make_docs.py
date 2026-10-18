import itertools, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent

# ---------------- truth tables
def tbl(h, rows): 
    s = "| " + " | ".join(h) + " |\n|" + "---|"*len(h) + "\n"
    return s + "".join("| " + " | ".join(map(str,r)) + " |\n" for r in rows)
t = "# Truth Tables\n\nAll tables are exhaustive and match the self-checking testbenches in `tb/`.\n\n"
r2 = list(itertools.product((0,1),repeat=2))
t += "## 2-input gates\n\n" + tbl(["A","B","AND","OR","XOR","NAND","NOR","XNOR"],
     [(a,b,a&b,a|b,a^b,1-(a&b),1-(a|b),1-(a^b)) for a,b in r2])
t += "\n## NOT\n\n" + tbl(["A","Y = A'"],[(0,1),(1,0)])
t += "\n## Half adder\n\n" + tbl(["A","B","SUM = A^B","CARRY = A&B"],[(a,b,a^b,a&b) for a,b in r2])
t += "\n## Full adder\n\n" + tbl(["A","B","Cin","SUM","COUT"],[(a,b,c,(a+b+c)&1,(a+b+c)>>1) for a,b,c in itertools.product((0,1),repeat=3)])
t += "\n## 2:1 multiplexer (Y = SEL ? B : A)\n\n" + tbl(["SEL","A","B","Y"],[(s,a,b,b if s else a) for s,a,b in itertools.product((0,1),repeat=3)])
t += "\n## 4:1 multiplexer\n\n" + tbl(["SEL[1:0]","Y"],[("00","D0"),("01","D1"),("10","D2"),("11","D3")])
t += "\n## 4-bit ripple carry adder - sample vectors (testbench covers all 512)\n\n" + tbl(["A","B","Cin","SUM","COUT","A+B+Cin"],
     [(a,b,c,(a+b+c)&15,(a+b+c)>>4,a+b+c) for a,b,c in [(0,0,0),(5,3,0),(9,6,1),(15,1,0),(15,15,1),(7,8,0)]])
(root/"docs/truth_tables.md").write_text(t)

# ---------------- K-map solutions
k = """# Karnaugh Map Solutions

Gray-code ordering is used on both axes. Each figure is in `docs/diagrams/`.

## 1. Full adder - SUM  (`kmap_fa_sum.png`)
Minterms: m(1,2,4,7). All four 1-cells are isolated (checkerboard) so no grouping is possible.
`SUM = A'B'Cin + A'BCin' + AB'Cin' + ABCin = A XOR B XOR Cin`

## 2. Full adder - COUT  (`kmap_fa_cout.png`)
Minterms: m(3,5,6,7). Three pairs: `AB` (m6,m7), `A.Cin` (m5,m7), `B.Cin` (m3,m7).
`COUT = AB + A.Cin + B.Cin`  (majority function)  
Equivalent form used in RTL: `COUT = AB + Cin.(A XOR B)`

## 3. 2:1 multiplexer  (`kmap_mux2.png`)
Variables (S,A,B), Y = S ? B : A. Minterms: m(2,3,5,7).
Pairs: `S'.A` (m2,m3) and `S.B` (m5,m7). The consensus term `A.B` (m3,m7) is redundant (it only removes a static-1 hazard).
`Y = S'A + SB`

## 4. BCD-invalid detector  (`kmap_bcd_invalid.png`)
Output is 1 when the 4-bit input is not a valid BCD digit (10-15). Minterms: m(10,11,12,13,14,15).
Quad `A.B` (m12-15) and quad `A.C` (m10,11,14,15).
`F = AB + AC = A(B + C)`

## 5. Half adder (2 variables - no map needed)
`SUM = A'B + AB' = A XOR B`, `CARRY = AB`

All four simplified expressions above were checked against their truth tables for every input
combination by `scripts/verify_model.py`.
"""
(root/"docs/karnaugh_maps.md").write_text(k)

# ---------------- Linux report
log = (root/"reports/linux_command_log.txt").read_text()
rep = """# Linux Command Practice Report  (Exercise 6)

**Environment used to capture the log below:** Ubuntu 24.04 LTS (Linux x86_64 terminal).
> Re-run `bash scripts/linux_practice.sh` on *your own* Ubuntu/WSL machine and paste your own output
> into the "Captured session" section before submitting. The script is non-destructive (works only in `/tmp/vlsi_practice`).

## Commands practised

| Command | Purpose | Example used |
|---|---|---|
| `pwd` | print current working directory | `pwd` |
| `ls` / `ls -l` / `ls -a` / `ls -F` | list files (long, hidden, type markers) | `ls -l rtl docs` |
| `cd` | change directory | `cd /tmp/vlsi_practice` |
| `mkdir -p` | create (nested) directories | `mkdir -p rtl tb sim docs scripts` |
| `cp` | copy a file | `cp rtl/demo.v rtl/demo_backup.v` |
| `mv` | move / rename a file | `mv rtl/demo_backup.v docs/demo_copy.v` |
| `rm` / `rm -r` | delete file / directory tree | `rm docs/demo_copy.v` |
| `cat` | print file contents | `cat rtl/demo.v` |
| `nano` | terminal text editor (interactive: `nano rtl/demo.v`, Ctrl+O save, Ctrl+X exit) | not scriptable - practise by hand |
| `chmod` | change permissions | `chmod +x scripts/hello.sh`, `chmod 644 rtl/demo.v` |
| `wc`, `grep` | count lines, search text | `grep -n module rtl/demo.v` |

## Permission notes
`-rw-r--r--` = owner read/write, group read, others read (octal 644).  
`chmod +x` adds the execute bit -> `-rwxr-xr-x` (octal 755), required to run a script as `./hello.sh`.

## Project workspace layout created for this task
```
vlsi_task1_logic_library/
|-- rtl/      synthesizable Verilog modules
|-- tb/       testbenches
|-- sim/      compiled .vvp and .vcd waveforms (git-ignored)
|-- docs/     diagrams, truth tables, K-maps, PDF documentation
|-- scripts/  setup + automation scripts
`-- reports/  simulation logs, Linux report, progress log
```

## Captured session
```text
""" + log.strip() + "\n```\n"
(root/"reports/linux_command_practice_report.md").write_text(rep)

# ---------------- daily log template
plan = [("Day 1","Semiconductor fundamentals, ASIC vs FPGA, VLSI design flow; install Ubuntu / configure WSL"),
 ("Day 2","Number systems, Boolean algebra, logic gates, truth tables, K-maps; solve logic problems"),
 ("Day 3","Linux commands; install Icarus Verilog + GTKWave; configure VS Code"),
 ("Day 4","Verilog syntax, modules, operators, procedural blocks; write basic gate modules"),
 ("Day 5","Half/Full adder, multiplexers; write testbenches and simulate"),
 ("Day 6","Analyse waveforms in GTKWave; improve RTL quality; document observations"),
 ("Day 7","Mini project (4-bit RCA, N-bit adder), GitHub repo, documentation, final checks")]
d = "# Daily Progress Log\n\n**Name:** T R JYOTHIRMAY DIKSHITH  **Intern ID:** SG 2884  **Task:** VLSI Design Internship - Task 1\n\n"
d += "> The *Planned activity* column is pre-filled from the 7-day plan. Fill in the remaining columns honestly each day.\n\n"
d += "| Day | Date | Planned activity | Hours | What I actually did | Problems faced / how solved | Tomorrow |\n|---|---|---|---|---|---|---|\n"
for a,b in plan: d += f"| {a} | | {b} | | | | |\n"
(root/"reports/daily_progress_log.md").write_text(d)
print("docs written")
