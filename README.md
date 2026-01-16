# Scaffold: MADLAD / MDLD Reflectology Stack

Scaffold is a multi-ring implementation of the MADLAD/MDLD reflectology stack. It includes a Reflectology kernel, a virtual machine, a compiler, an interpreter for the MDLD DSL, and documentation tooling for both MDLD/MADLAD and general source trees. It is intended for everyone: researchers, engineers, and curious builders who want to explore or extend the ring architecture.

## Purpose

Scaffold provides a reference implementation of the MADLAD/MDLD stack, with a runnable interpreter, proof-generation hooks, and supporting tooling. Use it to execute MDLD programs, inspect ring behavior, generate documentation, and experiment with the reflectology axiom set.

## Highlights

- **Ring 0 Reflectology Kernel** with a full axiom set and a TX/RX bus for cross-ring coordination.
- **Ring 1 Virtual Machine** that executes opcodes and dispatches commands into the kernel.
- **Ring 2 Compiler/Parser** that tokenizes, parses, optimizes, and emits VM instructions.
- **Ring 3 Analytical Engine** with symbolic and numeric analysis utilities.
- **Ring 4 Networking** to support transport, messaging, and ring connectivity patterns.
- **Ring 5 Storage** for persistence helpers and file-backed workflows.
- **Ring 6 Visualization** for docs, diagrams, and visualization tooling.
- **Ring 7 UI** for human-facing interfaces and interactive surfaces.
- **Ring 8 Deployment** for packaging, deployment, and ops artifacts.
- **Ring 9 Experiments** for integration work and incubated capabilities.
- **MDLD Interpreter** for executing `.mdld` programs with optional Metamath proof certificate output.
- **Documentation generators** for MDLD/MADLAD (MADDOC) and multi-language codebases (MDLDDOC).
- **Metamath tooling** via `mmverify.py` and supporting proof artifacts.

## Quick start

### Install prerequisites

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Note: this repository currently uses `requirements.txt` rather than a `pyproject.toml`.

### Run the MDLD interpreter

```bash
python3 mdld_interpreter.py test_e2e.mdld
```

To emit Metamath proof certificates:

```bash
python3 mdld_interpreter.py --proof test_e2e.mdld
```

### Generate documentation

**MDLD/MADLAD-only docs (MADDOC):**

```bash
python3 maddoc.py test_e2e.mdld
python3 maddoc.py --json test_e2e.mdld
python3 maddoc.py --serve 8080
```

**Universal docs for multiple languages (MDLDDOC):**

```bash
python3 mdlddoc.py test_e2e.mdld
python3 mdlddoc.py --html test_e2e.mdld
python3 mdlddoc.py --serve 8080
```

### Run tests

```bash
python3 ring0-math-kernel/test_mdld.py
python3 ring0-math-kernel/test_full_doc.py
python3 test_deployment_viz.py
python3 madlad_e2e.py
```

## Architecture overview

Scaffold uses a ring-based architecture, with each ring contributing a focused capability:

| Ring | Area | Description |
| --- | --- | --- |
| Ring 0 | `ring0-math-kernel` | Reflectology kernel implementing the axiom set and the TX/RX bus. |
| Ring 1 | `ring1-virtual-machine` | VM runtime that executes opcodes and dispatches kernel commands. |
| Ring 2 | `ring2-compiler-parser` | Compiler/lexer/parser, AST, optimizer, and bytecode emission. |
| Ring 3 | `ring3-analysis-logic` | Analytical engine for symbolic/numeric routines. |
| Ring 4 | `ring4-networking` | Networking and transport concerns. |
| Ring 5 | `ring5-storage` | Storage subsystems and persistence helpers. |
| Ring 6 | `ring6-visualization` | Visualization and documentation tooling. |
| Ring 7 | `ring7-ui` | UI surfaces for interacting with MADLAD/MDLD artifacts. |
| Ring 8 | `ring8-deployment` | Packaging and deployment assets. |
| Ring 9 | `ring9` | Additional experiments and integration work. |

## High-level architecture

- **Interpreter:** `mdld_interpreter.py` parses `.mdld` sources via the ANTLR-generated lexer/parser and executes the program using visitor-based evaluation.
- **Proof generator:** In `--proof` mode, the interpreter emits Metamath proof certificates that can be checked with `mmverify.py`.
- **Ring bus:** The Ring 0 kernel exposes a TX/RX bus used to coordinate message passing between rings.

## Key scripts and entry points

- `mdld_interpreter.py` — executes `.mdld` programs and can emit Metamath proof certificates.
- `mdld_interpreter.py` (proof mode) — emits proof certificates that can be verified with `mmverify.py`.
- `mdlddoc.py` — universal documentation generator that parses MDLD and mainstream languages.
- `maddoc.py` — MDLD/MADLAD documentation generator.
- `mmverify.py` — Metamath proof verification helper.
- `ring0-math-kernel/ring0_kernel.py` — core axiom implementation and ring bus.
- `ring1-virtual-machine/ring1_vm.py` — opcode execution and kernel command dispatch.
- `ring2-compiler-parser/ring2_compiler.py` — compiler pipeline from tokenization to codegen.
- `ring3-analysis-logic/ring3_analysis.py` — analytical engine routines.
- `ring4-networking/` — networking and transport modules for ring communication.
- `ring5-storage/` — storage adapters and persistence utilities.
- `ring6-visualization/` — visualization tooling and documentation assets.
- `ring7-ui/` — UI projects and interactive experiences.
- `ring8-deployment/` — deployment and packaging configuration.
- `ring9/` — experimental and integration workspaces.

## Repository layout

```
.
├── ring0-math-kernel/
├── ring1-virtual-machine/
├── ring2-compiler-parser/
├── ring3-analysis-logic/
├── ring4-networking/
├── ring5-storage/
├── ring6-visualization/
├── ring7-ui/
├── ring8-deployment/
├── ring9/
├── mdld_interpreter.py
├── mdlddoc.py
├── maddoc.py
└── test_e2e.mdld
```

## MDLD language specification and inputs

- **Language spec:** The MDLD grammar and language definition are captured in the ANTLR artifacts (`mdldLexer.py`, `mdldParser.py`, `mdldVisitor.py`) that define the parser and visitor APIs used by the interpreter.
- **Input files:** Provide `.mdld` files (for example, `test_e2e.mdld`) to the interpreter via `python3 mdld_interpreter.py path/to/file.mdld`. The interpreter accepts any valid MDLD input file on disk.

## Development notes

- The MDLD interpreter accepts a `.mdld` file path and can be run in proof mode with `--proof`.
- Documentation tools have their own CLI flags for JSON and HTML output, along with a lightweight server.
- The stack is intentionally modular: the ring bus in Ring 0 is used to coordinate ring-to-ring calls.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
