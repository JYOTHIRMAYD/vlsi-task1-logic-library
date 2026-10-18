#!/usr/bin/env python3
"""Generates all figures in docs/ (gate symbols, circuits, block diagrams, K-maps, reference waveforms)."""
import os, itertools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle, Rectangle, FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
D, W = f"{OUT}/diagrams", f"{OUT}/waveforms_reference"
LW, INK = 1.8, "#1b2a41"

# ---------------------------------------------------------------- gate symbols
def gate(ax, kind, x, y, sx=1.3, sy=1.0):
    """Draw gate with lower-left at (x,y). Returns (in_top, in_bot, out) pin coords."""
    M, L, C = Path.MOVETO, Path.LINETO, Path.CURVE3
    def P(verts, codes, close=True):
        v = [(x+px*sx, y+py*sy) for px,py in verts]
        ax.add_patch(PathPatch(Path(v, codes), fc="white", ec=INK, lw=LW, zorder=3))
    base = kind.replace("N","",1) if kind in ("NAND","NOR") else kind
    base = {"XNOR":"XOR"}.get(kind, base)
    tip = 1.0
    if kind == "NOT":
        P([(0,0),(0,1),(0.85,0.5),(0,0)], [M,L,L,L]); tip = 0.85
    elif base == "AND":
        n = 20; import math
        pts = [(0,0),(0,1),(0.5,1)] + [(0.5+0.5*math.sin(math.pi*t/n), 0.5+0.5*math.cos(math.pi*t/n)) for t in range(1,n+1)] + [(0.5,0)]
        P(pts+[(0,0)], [M]+[L]*(len(pts)))
    else:  # OR / XOR shield
        P([(0,0),(0.5,0),(0.8,0.1),(1,0.5),(0.8,0.9),(0.5,1),(0,1),(0.25,0.5),(0,0)],
          [M,L,C,C,C,C,L,C,C])
        if base == "XOR":
            P([(-0.15,0),(0.10,0.5),(-0.15,1)], [M,C,C])
    out_x = x + tip*sx
    if kind in ("NAND","NOR","XNOR","NOT"):
        r = 0.07*sy; ax.add_patch(Circle((out_x+r, y+0.5*sy), r, fc="white", ec=INK, lw=LW, zorder=4)); out_x += 2*r
    in_x = x - (0.15*sx if base=="XOR" and kind!="NOT" else 0)
    if kind == "NOT": return (x, y+0.5*sy), None, (out_x, y+0.5*sy)
    px = x + (0.09*sx if base=="XOR" else 0)
    return (px, y+0.75*sy), (px, y+0.25*sy), (out_x, y+0.5*sy)

def wire(ax, pts, **k): ax.plot(*zip(*pts), color=INK, lw=LW-0.4, solid_capstyle="round", zorder=2, **k)
def dot(ax, p): ax.add_patch(Circle(p, 0.06, fc=INK, ec=INK, zorder=5))
def label(ax, p, t, ha="right", **k): ax.text(p[0], p[1], t, ha=ha, va="center", fontsize=11, color=INK, **k)
def stub(ax, pin, name, length=0.5):
    wire(ax, [(pin[0]-length, pin[1]), pin]); label(ax, (pin[0]-length-0.06, pin[1]), name)
def out_stub(ax, pin, name, length=0.5):
    wire(ax, [pin, (pin[0]+length, pin[1])]); label(ax, (pin[0]+length+0.06, pin[1]), name, ha="left")
def elbow(ax, p0, p1, xm=None):
    xm = xm if xm is not None else (p0[0]+p1[0])/2
    wire(ax, [p0, (xm, p0[1]), (xm, p1[1]), p1])
def canvas(w, h, title):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=13, weight="bold", color=INK)
    return fig, ax
def save(fig, path): fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)

# ---- 1. all basic gates with truth tables
fig, axes = plt.subplots(2, 4, figsize=(15, 7.2))
specs = [("AND","Y = A·B",lambda a,b:a&b),("OR","Y = A+B",lambda a,b:a|b),("XOR","Y = A⊕B",lambda a,b:a^b),("NOT","Y = A'",None),
         ("NAND","Y = (A·B)'",lambda a,b:1-(a&b)),("NOR","Y = (A+B)'",lambda a,b:1-(a|b)),("XNOR","Y = (A⊕B)'",lambda a,b:1-(a^b))]
for ax, (k, expr, f) in zip(axes.flat, specs):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.4, 3.6); ax.set_ylim(-3.3, 1.6)
    a,b,o = gate(ax, k, 0.4, 0.2)
    if b: stub(ax,a,"A",0.7); stub(ax,b,"B",0.7)
    else: stub(ax,a,"A",0.7)
    out_stub(ax,o,"Y",0.6)
    ax.text(1.1, 1.45, k, ha="center", fontsize=13, weight="bold", color=INK)
    ax.text(1.1, -0.3, expr, ha="center", fontsize=11, color=INK)
    rows = [(a_,b_) for a_ in (0,1) for b_ in (0,1)] if f else [(0,),(1,)]
    hdr = "A B | Y" if f else "A | Y"
    ax.text(1.1, -0.8, hdr, ha="center", va="top", fontsize=10, family="monospace", weight="bold")
    for i,r in enumerate(rows):
        yv = f(*r) if f else 1-r[0]
        ax.text(1.1, -1.25-0.42*i, " ".join(map(str,r))+f" | {yv}", ha="center", va="top", fontsize=10, family="monospace")
axes.flat[-1].axis("off")
fig.suptitle("Basic Logic Gates - Symbols, Expressions and Truth Tables", fontsize=15, weight="bold", color=INK)
save(fig, f"{D}/logic_gates.png")

# ---- 2. half adder
fig, ax = canvas(7.5, 4.2, "Half Adder - Gate Level")
x1,x2,o1 = gate(ax,"XOR",2,2.0); stub(ax,x1,"A"); stub(ax,x2,"B"); out_stub(ax,o1,"SUM = A⊕B")
a1,a2,o2 = gate(ax,"AND",2,0.2); stub(ax,a1,"A"); stub(ax,a2,"B"); out_stub(ax,o2,"CARRY = A·B")
save(fig, f"{D}/half_adder.png")

# ---- 3. full adder
fig, ax = canvas(11, 5.6, "Full Adder - Gate Level (two half adders + OR)")
p1,p2,po = gate(ax,"XOR",1.5,3.8); stub(ax,p1,"A"); stub(ax,p2,"B")
q1,q2,qo = gate(ax,"XOR",5.0,3.8); out_stub(ax,qo,"SUM",0.7); stub(ax,q2,"Cin",0.5)
elbow(ax,po,q1,po[0]+0.6); ax.text(po[0]+0.62, po[1]+0.18, "S1", fontsize=10, color=INK)
s1,s2,so = gate(ax,"AND",5.0,1.9)                         # (S1 . Cin)
elbow(ax,po,s1,po[0]+0.6); dot(ax,(po[0]+0.6,po[1])); stub(ax,s2,"Cin",0.5)
r1,r2,ro = gate(ax,"AND",1.5,0.2); stub(ax,r1,"A"); stub(ax,r2,"B")   # (A . B)
t1,t2,to = gate(ax,"OR",8.2,0.95); out_stub(ax,to,"COUT",0.7)
elbow(ax,so,t1,so[0]+0.6); elbow(ax,ro,t2,so[0]+0.6)
ax.text(so[0]+0.08, so[1]+0.18, "C2 = S1·Cin", fontsize=10, color=INK); ax.text(ro[0]+0.08, ro[1]+0.18, "C1 = A·B", fontsize=10, color=INK)
save(fig, f"{D}/full_adder.png")

# ---- 4. 2:1 mux
fig, ax = canvas(9, 4.5, "2:1 Multiplexer - Gate Level   (Y = S'·A + S·B)")
n_in,_,n_out = gate(ax,"NOT",1.0,2.3,sx=0.9,sy=0.8); stub(ax,n_in,"S",0.5)
g1a,g1b,g1o = gate(ax,"AND",3.3,1.7); g2a,g2b,g2o = gate(ax,"AND",3.3,0.0)
stub(ax,g1a,"A"); elbow(ax,n_out,g1b,n_out[0]+0.3)
stub(ax,g2a,"B"); stub(ax,g2b,"S")
o1,o2,oo = gate(ax,"OR",6.2,0.85); elbow(ax,g1o,o1,g1o[0]+0.5); elbow(ax,g2o,o2,g2o[0]+0.5); out_stub(ax,oo,"Y",0.6)
save(fig, f"{D}/mux2to1.png")

# ---- 5. RTL block diagram of the 4-bit RCA
fig, ax = plt.subplots(figsize=(13, 5.4)); ax.axis("off"); ax.set_xlim(-0.5, 15); ax.set_ylim(-1.7, 5.6)
ax.set_title("RTL Block Diagram - 4-bit Ripple Carry Adder (ripple_carry_adder_4bit)", fontsize=13, weight="bold", color=INK)
xs = [10.3, 7.1, 3.9, 0.7]
for i,x in enumerate(xs):
    ax.add_patch(FancyBboxPatch((x,1.4),2.2,1.7,boxstyle="round,pad=0.05",fc="#dbe9ff",ec=INK,lw=LW))
    ax.text(x+1.1,2.25,f"full_adder\nfa{i}",ha="center",va="center",fontsize=11,color=INK,weight="bold")
    ax.annotate("",xy=(x+0.55,3.1),xytext=(x+0.55,4.3),arrowprops=dict(arrowstyle="->",color=INK,lw=1.5))
    ax.annotate("",xy=(x+1.65,3.1),xytext=(x+1.65,4.3),arrowprops=dict(arrowstyle="->",color=INK,lw=1.5))
    ax.text(x+0.55,4.5,f"a[{i}]",ha="center",fontsize=11); ax.text(x+1.65,4.5,f"b[{i}]",ha="center",fontsize=11)
    ax.annotate("",xy=(x+1.1,0.2),xytext=(x+1.1,1.4),arrowprops=dict(arrowstyle="->",color=INK,lw=1.5))
    ax.text(x+1.1,-0.1,f"sum[{i}]",ha="center",va="top",fontsize=11)
    if i<3:
        ax.annotate("",xy=(x+2.2,2.25),xytext=(x+3.2-0.0,2.25),arrowprops=dict(arrowstyle="->",color="#b3261e",lw=1.8))
        ax.text(x+2.7,2.45,f"c{i+1}",ha="center",color="#b3261e",fontsize=11,weight="bold")
ax.annotate("",xy=(12.5,2.25),xytext=(14.3,2.25),arrowprops=dict(arrowstyle="->",color="#b3261e",lw=1.8)); ax.text(14.4,2.25,"cin",va="center",fontsize=11,weight="bold",color="#b3261e")
ax.annotate("",xy=(-0.5,2.25),xytext=(0.7,2.25),arrowprops=dict(arrowstyle="->",color="#b3261e",lw=1.8)); ax.text(-0.45,2.55,"cout",fontsize=11,weight="bold",color="#b3261e")
ax.text(7.2,-1.3,"Carry ripples from fa0 (right, LSB) to fa3 (left, MSB). Critical path = 4 x (full-adder carry delay).",ha="center",fontsize=10,style="italic",color=INK)
save(fig, f"{D}/rca4_block_diagram.png")

# ---- 6. generic flow boxes
def flow(path, title, steps, colors=None, w=14, cols=None):
    n = len(steps); fig, ax = plt.subplots(figsize=(w, 2.6)); ax.axis("off"); ax.set_xlim(0, n*2.6); ax.set_ylim(0,2.4)
    ax.set_title(title, fontsize=13, weight="bold", color=INK)
    for i,s in enumerate(steps):
        ax.add_patch(FancyBboxPatch((i*2.6+0.15,0.5),2.0,1.3,boxstyle="round,pad=0.04",fc=(cols or ["#dbe9ff"]*n)[i],ec=INK,lw=LW))
        ax.text(i*2.6+1.15,1.15,s,ha="center",va="center",fontsize=10,color=INK,weight="bold")
        if i<n-1: ax.annotate("",xy=(i*2.6+2.75,1.15),xytext=(i*2.6+2.17,1.15),arrowprops=dict(arrowstyle="->",color=INK,lw=1.8))
    save(fig, path)
flow(f"{D}/vlsi_design_flow.png","VLSI Design Flow (specification to chip)",
     ["System\nSpecification","RTL Design\n(Verilog)","Functional\nVerification","Logic\nSynthesis","Floorplan\nPlace & Route","Timing\nSign-off","Fabrication\n(Tape-out)"],
     ["#fff3cd"]+["#dbe9ff"]*3+["#d9f2d9"]*2+["#f3d9f2"], w=16)
flow(f"{D}/simulation_workflow.png","Simulation Workflow (Icarus Verilog + GTKWave)",
     ["Write RTL\nrtl/*.v","Write Testbench\ntb/*.v","Compile\niverilog -o","Simulate\nvvp  ->  .vcd","View Waves\ngtkwave","Debug / Fix\n& repeat"],
     ["#dbe9ff","#dbe9ff","#fff3cd","#fff3cd","#d9f2d9","#f8d7da"], w=14)

# ---- 7. K-maps
GRAY = [0,1,3,2]
def kmap(path, title, nv, minterms, groups, vars_, expr):
    fig, ax = plt.subplots(figsize=(5.6, 4.4)); ax.axis("off"); ax.set_aspect("equal")
    rows = 2 if nv==3 else 4; cols = 4; cw = 1.0
    ax.set_xlim(-2.2, 5.0); ax.set_ylim(-rows-1.2, 2.2)
    rlab = {2:["0","1"], 4:["00","01","11","10"]}[rows]; clab = ["00","01","11","10"]
    rn = vars_[0] if nv==3 else vars_[0]+vars_[1]; cn = vars_[1]+vars_[2] if nv==3 else vars_[2]+vars_[3]
    for r in range(rows):
        for c in range(cols):
            m = (r*4+GRAY[c]) if nv==3 else (GRAY[r]*4+GRAY[c])
            ax.add_patch(Rectangle((c,-r-1),1,1,fc="white",ec=INK,lw=1.2))
            ax.text(c+0.5,-r-0.5,str(1 if m in minterms else 0),ha="center",va="center",fontsize=15,weight="bold" if m in minterms else "normal",color="#b3261e" if m in minterms else "#888")
            ax.text(c+0.9,-r-0.9,f"m{m}",ha="right",va="bottom",fontsize=7,color="#666")
    for c in range(cols): ax.text(c+0.5,0.25,clab[c],ha="center",fontsize=11)
    for r in range(rows): ax.text(-0.2,-r-0.5,rlab[r],ha="right",va="center",fontsize=11)
    ax.text(-1.2 if nv==3 else -1.35,0.55,f"{rn} \\ {cn}",ha="center",fontsize=11,weight="bold")
    pal = ["#1565c0","#2e7d32","#ef6c00","#6a1b9a"]
    for i,(r0,r1,c0,c1,sty,lab) in enumerate(groups):
        pad = 0.08+0.05*i
        ax.add_patch(FancyBboxPatch((c0+pad,-r1-1+pad),c1-c0+1-2*pad,r1-r0+1-2*pad,boxstyle="round,pad=0.0,rounding_size=0.25",fc="none",ec=pal[i%4],lw=2.4,ls=sty))
    leg_y = -rows-0.55
    for i,(r0,r1,c0,c1,sty,lab) in enumerate(groups):
        ax.text(-1.9+ (i%2)*3.4, leg_y-0.4*(i//2), "■ "+lab, color=pal[i%4], fontsize=10, va="center")
    ax.set_title(title, fontsize=12, weight="bold", color=INK); ax.text(2.0, 1.6, expr, ha="center", fontsize=11.5, color=INK, weight="bold")
    save(fig, path)
kmap(f"{D}/kmap_fa_sum.png","K-map: Full Adder SUM  (m1,m2,m4,m7)",3,[1,2,4,7],
     [(0,0,1,1,"-","m1"),(0,0,3,3,"-","m2"),(1,1,0,0,"-","m4"),(1,1,2,2,"-","m7")],"ABC","No grouping possible (checkerboard):  SUM = A⊕B⊕Cin")
kmap(f"{D}/kmap_fa_cout.png","K-map: Full Adder COUT  (m3,m5,m6,m7)",3,[3,5,6,7],
     [(1,1,2,3,"-","A·B"),(1,1,1,2,"-","A·Cin"),(0,1,2,2,"-","B·Cin")],"ABC","COUT = A·B + A·Cin + B·Cin")
kmap(f"{D}/kmap_mux2.png","K-map: 2:1 MUX  Y(S,A,B)  (m2,m3,m5,m7)",3,[2,3,5,7],
     [(0,0,2,3,"-","S'·A"),(1,1,1,2,"-","S·B"),(0,1,2,2,":","A·B (redundant)")],"SAB","Y = S'·A + S·B   (A·B term is redundant)")
kmap(f"{D}/kmap_bcd_invalid.png","K-map: BCD-invalid detector  F(A,B,C,D) = Σm(10..15)",4,list(range(10,16)),
     [(2,2,0,3,"-","A·B"),(2,3,2,3,"-","A·C")],"ABCD","F = A·B + A·C")

# ---- 8. reference waveforms (from golden model, NOT from GTKWave)
def wave(path, title, sigs, step=10, bus=()):
    n = len(sigs); fig, axs = plt.subplots(n,1,figsize=(11,0.75*n+0.9),sharex=True)
    fig.suptitle(title+"   [reference plot from Python golden model - replace with your GTKWave screenshot]", fontsize=10.5, weight="bold", color=INK)
    for ax,(name,vals) in zip(axs,sigs):
        t = list(range(len(vals)+1)); 
        if name in bus:
            ax.set_ylim(0,1); ax.axis("off")
            for i,v in enumerate(vals):
                ax.add_patch(Rectangle((i*step,0.15),step,0.7,fc="#e8f5e9",ec="#2e7d32",lw=1.2)); ax.text(i*step+step/2,0.5,f"{v:X}" if isinstance(v,int) else v,ha="center",va="center",fontsize=10,family="monospace")
            ax.set_xlim(0,len(vals)*step); ax.text(-0.01*len(vals)*step,0.5,name,ha="right",va="center",fontsize=10,family="monospace")
        else:
            ax.step([i*step for i in range(len(vals)+1)],vals+[vals[-1]],where="post",color="#1565c0",lw=1.8); ax.set_ylim(-0.3,1.4); ax.set_yticks([]); 
            for s in ("top","right","left","bottom"): ax.spines[s].set_visible(False)
            ax.text(-0.01*len(vals)*step,0.5,name,ha="right",va="center",fontsize=10,family="monospace",transform=ax.transData)
            ax.set_xlim(0,len(vals)*step)
    axs[-1].set_xlabel("time (ns)")
    for ax in axs[:-1]: ax.tick_params(labelbottom=False)
    fig.subplots_adjust(left=0.12); save(fig, path)
combos = list(itertools.product((0,1),repeat=2))
wave(f"{W}/wave_half_adder.png","tb_half_adder",[("a",[c[0] for c in combos]),("b",[c[1] for c in combos]),("sum",[c[0]^c[1] for c in combos]),("carry",[c[0]&c[1] for c in combos])])
c3 = list(itertools.product((0,1),repeat=3))
wave(f"{W}/wave_full_adder.png","tb_full_adder",[("a",[c[0] for c in c3]),("b",[c[1] for c in c3]),("cin",[c[2] for c in c3]),
     ("sum",[(sum(c))&1 for c in c3]),("cout",[1 if sum(c)>=2 else 0 for c in c3])])
wave(f"{W}/wave_mux2to1.png","tb_mux2to1",[("sel",[c[0] for c in c3]),("a",[c[1] for c in c3]),("b",[c[2] for c in c3]),("y",[c[2] if c[0] else c[1] for c in c3])])
wave(f"{W}/wave_logic_gates.png","tb_logic_gates",[("a",[c[0] for c in combos]),("b",[c[1] for c in combos]),
     ("y_and",[c[0]&c[1] for c in combos]),("y_or",[c[0]|c[1] for c in combos]),("y_xor",[c[0]^c[1] for c in combos]),
     ("y_nand",[1-(c[0]&c[1]) for c in combos]),("y_nor",[1-(c[0]|c[1]) for c in combos]),("y_xnor",[1-(c[0]^c[1]) for c in combos]),("y_not",[1-c[0] for c in combos])])
vec = [(0,0,0),(5,3,0),(9,6,1),(15,1,0),(15,15,1),(7,8,0)]
wave(f"{W}/wave_rca4.png","tb_ripple_carry_adder_4bit",[("a[3:0]",[v[0] for v in vec]),("b[3:0]",[v[1] for v in vec]),("cin",[v[2] for v in vec]),
     ("sum[3:0]",[(v[0]+v[1]+v[2])&15 for v in vec]),("cout",[(v[0]+v[1]+v[2])>>4 for v in vec])],bus=("a[3:0]","b[3:0]","sum[3:0]"))
print("figures written")
