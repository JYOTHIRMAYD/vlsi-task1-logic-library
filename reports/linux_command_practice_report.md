# Linux Command Practice Report  (Exercise 6)

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
$ pwd
/home/t-r-jyothirmay-dikshith/vlsi_task1_logic_library

$ mkdir -p /tmp/vlsi_practice

$ cd /tmp/vlsi_practice && pwd
/tmp/vlsi_practice

$ mkdir -p rtl tb sim docs scripts

$ ls
docs
rtl
scripts
sim
tb

$ echo 'module demo; endmodule' > rtl/demo.v

$ cat rtl/demo.v
module demo; endmodule

$ cp rtl/demo.v rtl/demo_backup.v

$ mv rtl/demo_backup.v docs/demo_copy.v

$ ls -l rtl docs
docs:
total 4
-rw-rw-r-- 1 t-r-jyothirmay-dikshith t-r-jyothirmay-dikshith 23 Oct 18 21:20 demo_copy.v

rtl:
total 4
-rw-rw-r-- 1 t-r-jyothirmay-dikshith t-r-jyothirmay-dikshith 23 Oct 18 21:20 demo.v

$ echo '#!/bin/bash' > scripts/hello.sh && echo 'echo Hello VLSI' >> scripts/hello.sh

$ ls -l scripts/hello.sh
-rw-rw-r-- 1 t-r-jyothirmay-dikshith t-r-jyothirmay-dikshith 28 Oct 18 21:20 scripts/hello.sh

$ chmod +x scripts/hello.sh

$ ls -l scripts/hello.sh
-rwxrwxr-x 1 t-r-jyothirmay-dikshith t-r-jyothirmay-dikshith 28 Oct 18 21:20 scripts/hello.sh

$ ./scripts/hello.sh
Hello VLSI

$ chmod 644 rtl/demo.v && ls -l rtl/demo.v
-rw-r--r-- 1 t-r-jyothirmay-dikshith t-r-jyothirmay-dikshith 23 Oct 18 21:20 rtl/demo.v

$ rm docs/demo_copy.v

$ ls docs

$ rm -r scripts

$ ls -F
docs/
rtl/
sim/
tb/

$ ls -a
.
..
docs
rtl
sim
tb

$ wc -l rtl/demo.v
1 rtl/demo.v

$ grep -n module rtl/demo.v
1:module demo; endmodule

$ cd /tmp && rm -r vlsi_practice && ls -d vlsi_practice 2>&1 | head -1
ls: cannot access 'vlsi_practice': No such file or directory
```
