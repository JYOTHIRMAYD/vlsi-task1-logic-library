#!/usr/bin/env bash
# Exercise 6 - Linux command practice. Creates a workspace in /tmp and echoes every command.
run() { echo; echo "\$ $*"; eval "$@"; }
rm -rf /tmp/vlsi_practice
run "pwd"
run "mkdir -p /tmp/vlsi_practice"
run "cd /tmp/vlsi_practice && pwd"
cd /tmp/vlsi_practice
run "mkdir -p rtl tb sim docs scripts"
run "ls"
run "echo 'module demo; endmodule' > rtl/demo.v"
run "cat rtl/demo.v"
run "cp rtl/demo.v rtl/demo_backup.v"
run "mv rtl/demo_backup.v docs/demo_copy.v"
run "ls -l rtl docs"
run "echo '#!/bin/bash' > scripts/hello.sh && echo 'echo Hello VLSI' >> scripts/hello.sh"
run "ls -l scripts/hello.sh"
run "chmod +x scripts/hello.sh"
run "ls -l scripts/hello.sh"
run "./scripts/hello.sh"
run "chmod 644 rtl/demo.v && ls -l rtl/demo.v"
run "rm docs/demo_copy.v"
run "ls docs"
run "rm -r scripts"
run "ls -F"
run "ls -a"
run "wc -l rtl/demo.v"
run "grep -n module rtl/demo.v"
run "cd /tmp && rm -r vlsi_practice && ls -d vlsi_practice 2>&1 | head -1"
