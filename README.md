# HDL Agent

> **Status**: Work in Progress

**HDL Agent** is an experimental AI system that converts natural-language prompts into **working Verilog hardware designs**.

## Overview

The system automatically generates RTL, simulates it, analyzes waveforms, and iterates until the hardware behavior matches the intended specification.

![HDL Agent Flowchart](docs/images/flowchart.png)

The final output is a **working Verilog hardware design**, validated by simulation and waveform analysis, together with:
- A finalized behavioral specification
- Verilog RTL source code
- A simulation testbench
- Waveform evidence of correct behavior

From this point, the design can be refined, extended with additional functionality, used as a building block in larger hardware systems, or passed to downstream physical design tools (out of scope for this project).

# Quickstart

Set up a reproducible development environment:
```bash 
uv venv
source .venv/Scripts/activate   # Windows (Git Bash)
# source .venv/bin/activate     # macOS / Linux

uv pip install -e .
```
Create a local environment configuration:
```bash
cp .env.example .env
```
Then edit `.env` to add required environment variables.

# TODO

- [ ] Add REPO STRUCTURE section 

