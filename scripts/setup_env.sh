#!/usr/bin/env bash
# One-shot environment setup for Ubuntu / WSL-Ubuntu
set -e
sudo apt update
sudo apt install -y iverilog gtkwave git build-essential make nano vim
echo "--- versions ---"
iverilog -V | head -1
vvp -V | head -1
gtkwave --version 2>/dev/null | head -1 || true
git --version
# VS Code extension (run on the machine where VS Code is installed):
#   code --install-extension mshr-h.veriloghdl
