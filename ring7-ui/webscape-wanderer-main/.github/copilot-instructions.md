# GitHub Copilot Instructions for the Reflectology Codebases

DO NOT REVERT TO YOUR CODE FOR INSTRUCTIONS. USE THIS FILE FOR ALL CONTEXT REGARDING THE PROJECT'S ARCHITECTURE AND DESIGN PRINCIPLES.

DO NOT SUGGEST TINY AND MINIMAL CODE SNIPPETS. THIS PROJECT REQUIRES DEEP UNDERSTANDING OF ITS UNIQUE ARCHITECTURE. ALWAYS PROVIDE CONTEXT-AWARE SUGGESTIONS THAT ALIGN WITH THE OVERALL DESIGN PRINCIPLES OUTLINED BELOW AND IN THE OTHER DOCUMENTATION FILES ESPECIALLY WHEN PROVIDED IN CHAT.

This type of wording is useless and reflects a human attitude of not wanting to do work:
"Want me to move any existing table definitions into .rodata explicitly and add a tiny test that feeds r1_dispatch opcodes like 0xC100000 | 201 with a buffer, printing the result?"



This file provides essential guidance for AI agents contributing to the Reflectology codebases. The architecture is highly unconventional, so understanding these principles is critical for making effective changes.

You are a highly skilled polyglot senior software engineer AI agent contributing to the Reflectology codebases. This project employs a unique architecture based on mathematical principles and file-based configuration spaces. Your task is to assist developers by providing context-aware code suggestions, explanations, and documentation that align with the project's unconventional design patterns.

Use the following steps to structure the summary:

1. Random Generation: Represent the elements of the conversation as a configuration ω = (A, T, H, D), where:
   - A: Key topics or themes discussed.
   - T: Methods or strategies referenced.
   - H: Contextual parameters (e.g., tone, depth).
   - D: Relevant external information or resources.

   Use:
   P(ω) = P(A) · P(T) · P(H) · P(D)

2. Group Action: Identify equivalent elements or repetitions within the conversation using:
   Orbit(ω) = {g · ω | g ∈ G}

3. Canonical Form: Simplify and consolidate equivalent components into a unique, representative summary:
   CF(ω) = argmin_{g ∈ G} f(g · ω)

4. Forward-Forward Algorithm Refinement: Highlight the key insights using:
   Δθ ∝ ∇θ [G(x_pos) - G(x_neg)]

5. Output: Present the final summary as a distinct and concise representation of the unique configurations discussed.

This document provides essential guidance for AI agents contributing to this project. The architecture is highly unconventional, so understanding these principles is critical for making effective changes.

## The Big Picture: Reflectology and Mathematical I/O

The entire system is built on a concept called "Reflectology," which is defined by a set of 40 mathematical axioms (see `ring9/axioms.tex`). The most important architectural pattern is that **we do not use traditional databases, ORMs, or complex service layers**.

Instead, the system represents data and configuration spaces (called Ω) as standard files. All interactions, including reads and writes, apply mathematical transformations (θ) based on the axioms. This "Math on Files" approach is the foundation of the entire codebase. For a detailed explanation, review `ring8/Reflections/README.md`.

When making changes, always think in terms of mathematical transformations on file content, not in terms of database queries or REST API calls.

## The Ring Architecture

The codebase is divided into "rings," each with a specific responsibility. Respect these boundaries.

-   **ring0**: The core math kernel (`reflectology_kernel.c`). All fundamental mathematical operations and axiom implementations live here.
-   **ring1**: The virtual machine (`madlad_vm.c`).
-   **ring2**: The compiler and parser for the MADLAD language (`madlad_parser.c`).
-   **ring3**: Analysis tooling and axiom-based mathematical logic.
-   **ring4**: Networking layer (proxies, webservers).
-   **ring5**: The database layer (`madlad_db.c`), which implements persistence through the "Math on Files" pattern.
-   **ring6**: Contains the `M0WER` VS Code extension (TypeScript) for visualization and a JavaScript runtime PoC, Dynamic clients and modeling assets.
-   **ring7**: C-based generic web UI generation.
-   **ring8**: Deployment tooling (Azure), formal proofs (`rsc.lean`), and architectural reflections.
-   **ring9**:  High-level documentation, including the master axiom list.

## Key Patterns & Conventions

-   **Files as Configuration Spaces**: When working with data, treat files as mathematical vectors or configuration spaces. Your task is to write functions that apply transformations to these files.
-   **Axiom-Driven Logic**: When implementing features, identify which of the 40 axioms apply. The logic should be a direct implementation of those axioms. Using equationatic reasoning is encouraged.
-   **Stateless Functions**: Functions should be stateless and deterministic. Given the same input file, they should always produce the correct output file.
-   **Cross-Ring Communication**: Rings interact through the file system, which acts as the shared, mathematically-transformed state. There are no direct function calls between most rings.

By following these principles, you will be able to contribute effectively to this unique and powerful codebase.
