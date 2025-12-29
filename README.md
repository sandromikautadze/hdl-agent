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
Then edit `.env` to add required environment variables (e.g. API keys).

# Repo Structure 






## Intuitive Example

### Input

*“Make a chip that is efficient at inference for a convolutional neural network.”*

### Specification Inference

The agent interprets the prompt as a request for a **streaming, stateful compute block** suitable for CNN inference and derives a reasonable initial specification, for example:

- The design is **clocked** and deterministic  
- Inputs are provided as a **stream of data** (e.g. feature map values)  
- The block performs a **fixed convolution operation**, with weights stored internally  
- Computation is **multi-cycle**, with a fixed latency  
- Outputs are produced as a **stream** after the pipeline fills  
- A reset initializes internal state and buffers  

The inferred specification is presented to the user, who can refine it in plain language
(e.g. kernel size, bitwidths, throughput vs latency, or pipelined vs combinational behavior).

### RTL, Testbench Generation, and Simulation

Once the specification is accepted, the agent generates:

- A **Verilog module** implementing the convolution datapath  
  (registers, combinational arithmetic, internal storage, and control logic)
- A **testbench** that feeds input data over time and checks output values after the expected latency

The design is then compiled and simulated automatically.

- Compilation or simulation errors trigger automatic RTL or testbench fixes.
- Successful simulations produce a **waveform (VCD)** capturing the full dataflow over time.

### Functional Verification

Correctness is verified by checking that:

- Outputs appear **only after the expected latency**
- Output values match the convolution of the provided inputs and internal weights
- Internal state updates occur **only on clock edges**
- Streaming behavior is consistent across multiple input samples

Verification can be performed:
- **Automatically**, via waveform analysis against an internal reference model, or
- **Manually**, by inspecting the waveform to confirm timing and dataflow behavior

If mismatches are detected, the agent updates the design and repeats the loop.