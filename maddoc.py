#!/usr/bin/env python3
"""
MADDOC - MADLAD Documentation Generator

Walks MDLD/MADLAD source trees and generates documentation.
Based on Python's pydoc but for the Reflectology DSL.

Ring 6 Tool - Axiom 5 (Hierarchical Structuring): Ω = ⋃ᵢ Ωᵢ

Usage:
    maddoc.py <file.mdld>           # Document a single file
    maddoc.py <directory>           # Document all .mdld files
    maddoc.py --serve [port]        # Start documentation server
    maddoc.py --json <file.mdld>    # Output JSON AST

Standards:
    - ISO/IEC 14977 (EBNF)
    - Unicode 15.0 (UAX #31)
    - RFC 8259 (JSON output)
"""

import os
import sys
import json
import re
import http.server
import socketserver
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime

# ANSI colors for terminal output
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# The 40 Axioms of Reflectology (for documentation cross-reference)
AXIOMS = {
    1: ("Initial Emptiness", "Ω₀ := ∅"),
    2: ("First Structure", "Ω₁ := {∅}"),
    3: ("Recursive Encapsulation", "Ω₂ := {Ω₁}"),
    4: ("Fractal Nature", "T(Ω) = λT(Ω')"),
    5: ("Hierarchical Structuring", "Ω = ⋃ᵢ Ωᵢ"),
    6: ("Redundancy Reduction", "Ω / ~"),
    7: ("Symmetry Reduction", "Ω / G"),
    8: ("Symmetry Breaking", "S(Ω) ≠ Ω ⇒ Ω' ⊂ Ω"),
    9: ("Complexity Reduction", "C(Ω) ≥ C(Ω')"),
    10: ("Ω-Bijection Principle", "∀ωᵢ ∈ Ω', ∃f : Ω' ↔ Ω''"),
    11: ("Complex Symmetry-Flow-Force Associativity", "((θ·q)·ω)·(θ·((θ·ω)·q)) = ω"),
    12: ("Contextual Monoid", "(p·q)·r = p·((p·r)·q) = r"),
    13: ("Loss Function", "L(ω) := θ(Ωω) - Cω"),
    14: ("Canonical Selection", "ω* := argmin_{ω∈Ω} L(ω)"),
    15: ("Reflective Convergence", "lim_{n→∞} θₙ(ω) - Cₙ"),
    16: ("Normalization (Entropy)", "H(Ω) := -∑ P(ω) log P(ω)"),
    17: ("Self-Correction", "ω' := correction(ω)"),
    18: ("Nonlinear Logic Formation", "ω' := nonlinear(ω)"),
    19: ("Hyperreal Extension", "ω + ε"),
    20: ("Dimensional Consistency", "lhs = rhs"),
    21: ("Rubik's Cube Goodness Model", "G := θ(Ω) - C"),
    22: ("Information Preservation", "I(Ω) = I(T(Ω))"),
    23: ("Energy Efficiency", "E(Ω) ≥ E(Ω')"),
    24: ("Chaotic Creativity Principle", "θ(Ω') - C' > θ(Ω) - C"),
    25: ("Gradient Flow Dynamics", "dω/dt = -∇L(ω)"),
    26: ("General Dynamical System", "dω/dt = f(ω)"),
    27: ("Recursive Structure", "ω' = f(ω, f(ω))"),
    28: ("Probabilistic Convergence", "P(ω' | ω)"),
    29: ("MAD Activation", "ω(t) := f(ω(t-1))"),
    30: ("Self-Regulation", "ω(t) := F(ω(t-1))"),
    31: ("Base Transform (25th Syllogism)", "ω' = f(ω)"),
    32: ("Path Dependence", "Ω(t) = f(T(t), Ω₀)"),
    33: ("Feedback Loop", "Ω(t) = F(Ω(t-1))"),
    34: ("Non-Equilibrium Dynamics", "dΩ/dt = F(Ω, θ)"),
    35: ("Causality and Correlation", "Ω(t) = C(Ω(t-1))"),
    36: ("Judgment Paradox", "J ∈ S ⇒ J(S) = Eval(S)"),
    37: ("Student Supremacy", "L' = θ(Ωₜ) - Cₜ; T* ⊂ T; T* ≻ T"),
    38: ("Recursive Lineage", "τₙ₊₁ := θ(τₙ) - Cτ; τ* := lim_{n→∞} θₙ(τ₀) - Cₙ"),
    39: ("Internal Emergence", "θ(Ωᵣ) - Cᵣ > θ(Ωₑ) - Cₑ"),
    40: ("Reflective Conjugate Duality", "∀ω ∈ Ω, ∃ω† := C(ω)"),
}


class NodeType(Enum):
    """MDLD AST node types"""
    DOCUMENT = "document"
    STATEMENT = "statement"
    AXIOM = "axiom_stmt"
    FUNCTION = "func_decl"
    TYPE = "type_decl"
    RECORD = "record_decl"
    MODULE = "module_decl"
    CONFIG_SPACE = "config_space_decl"
    COMMENT = "comment"
    EXPRESSION = "expr"
    IMPORT = "import_stmt"
    EXPORT = "export_stmt"
    ABI = "abi_decl"
    API = "api_decl"
    IO = "io_decl"


@dataclass
class DocNode:
    """A documented node in the MDLD AST"""
    name: str
    node_type: NodeType
    line: int
    column: int
    docstring: Optional[str] = None
    signature: Optional[str] = None
    axiom_refs: List[int] = field(default_factory=list)
    children: List['DocNode'] = field(default_factory=list)
    source: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'type': self.node_type.value,
            'line': self.line,
            'column': self.column,
            'docstring': self.docstring,
            'signature': self.signature,
            'axiom_refs': self.axiom_refs,
            'children': [c.to_dict() for c in self.children],
            'source': self.source
        }


@dataclass
class MadDoc:
    """Documentation for an MDLD file"""
    filepath: str
    module_name: str
    docstring: Optional[str] = None
    nodes: List[DocNode] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    axioms_used: List[int] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'filepath': self.filepath,
            'module_name': self.module_name,
            'docstring': self.docstring,
            'nodes': [n.to_dict() for n in self.nodes],
            'imports': self.imports,
            'exports': self.exports,
            'axioms_used': sorted(set(self.axioms_used)),
            'timestamp': self.timestamp
        }


class MDLDLexer:
    """Simple lexer for MDLD source files (fallback when tree-sitter unavailable)"""
    
    # Token patterns
    PATTERNS = {
        'comment_line': r'//[^\n]*',
        'comment_block': r'/\*[\s\S]*?\*/',
        'axiom': r'\bo([1-9]|[1-3][0-9]|40)\b',
        'define': r'\bDefine\b',
        'function': r'\bfunction\b',
        'type': r'\btype\b',
        'record': r'\brecord\b',
        'module': r'\bmodule\b',
        'space': r'\bSpace\b',
        'ident': r'[a-zA-Z_][a-zA-Z0-9_]*',
        'string': r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'',
        'number': r'\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',
        'operator': r'[+\-*/=<>!&|^~@#$%]+',
        'punct': r'[(){}[\],;:.]',
        'newline': r'\n',
        'whitespace': r'[ \t]+',
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def tokenize(self) -> List[Tuple[str, str, int, int]]:
        """Tokenize the source, return list of (type, value, line, column)"""
        combined = '|'.join(f'(?P<{k}>{v})' for k, v in self.PATTERNS.items())
        pattern = re.compile(combined)
        
        for match in pattern.finditer(self.source):
            kind = match.lastgroup
            value = match.group()
            line = self.source[:match.start()].count('\n') + 1
            col = match.start() - self.source.rfind('\n', 0, match.start())
            
            if kind not in ('whitespace', 'newline'):
                self.tokens.append((kind, value, line, col))
                
        return self.tokens


class MDLDParser:
    """Simple recursive descent parser for MDLD documentation extraction"""
    
    def __init__(self, source: str, filepath: str = "<stdin>"):
        self.source = source
        self.filepath = filepath
        self.lexer = MDLDLexer(source)
        self.tokens = self.lexer.tokenize()
        self.pos = 0
        self.doc = MadDoc(
            filepath=filepath,
            module_name=Path(filepath).stem if filepath != "<stdin>" else "stdin"
        )
        self.pending_comment: Optional[str] = None
        self.pending_comment_line: int = 0
        
    def parse(self) -> MadDoc:
        """Parse the source and extract documentation"""
        # Extract module-level docstring from first comment
        if self.tokens and self.tokens[0][0] in ('comment_line', 'comment_block'):
            self.doc.docstring = self._clean_comment(self.tokens[0][1])
            
        while self.pos < len(self.tokens):
            self._parse_statement()
            
        return self.doc
    
    def _current(self) -> Optional[Tuple[str, str, int, int]]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _advance(self) -> Optional[Tuple[str, str, int, int]]:
        token = self._current()
        self.pos += 1
        return token
    
    def _clean_comment(self, comment: str) -> str:
        """Clean up comment text"""
        if comment.startswith('//'):
            return comment[2:].strip()
        elif comment.startswith('/*'):
            # Remove /* and */ and clean up
            text = comment[2:-2]
            lines = text.split('\n')
            cleaned = []
            for line in lines:
                line = line.strip()
                if line.startswith('*'):
                    line = line[1:].strip()
                cleaned.append(line)
            return '\n'.join(cleaned).strip()
        return comment
    
    def _parse_statement(self):
        """Parse a single statement"""
        token = self._current()
        if not token:
            return
            
        kind, value, line, col = token
        
        # Track comments for docstrings
        if kind in ('comment_line', 'comment_block'):
            self.pending_comment = self._clean_comment(value)
            self.pending_comment_line = line
            self._advance()
            return
            
        # Axiom statement
        if kind == 'axiom':
            self._parse_axiom(line, col, value)
            return
            
        # Function declaration
        if kind == 'function':
            self._parse_function(line, col)
            return
            
        # Type declaration
        if kind == 'type':
            self._parse_type(line, col)
            return
            
        # Record declaration
        if kind == 'record':
            self._parse_record(line, col)
            return
            
        # Module declaration
        if kind == 'module':
            self._parse_module(line, col)
            return
            
        # Configuration space
        if kind == 'define':
            self._parse_define(line, col)
            return
            
        # Skip other tokens
        self._advance()
        self.pending_comment = None
        
    def _parse_axiom(self, line: int, col: int, axiom_token: str):
        """Parse an axiom statement like o1(expr)"""
        axiom_num = int(axiom_token[1:])
        self._advance()  # consume axiom keyword
        
        # Collect source until end of statement
        source_parts = [axiom_token]
        paren_depth = 0
        
        while self._current():
            kind, value, _, _ = self._current()
            source_parts.append(value)
            
            if value == '(':
                paren_depth += 1
            elif value == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    self._advance()
                    break
            elif kind == 'punct' and value in (';', '\n') and paren_depth == 0:
                break
                
            self._advance()
        
        node = DocNode(
            name=f"Axiom {axiom_num}",
            node_type=NodeType.AXIOM,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
            signature=' '.join(source_parts),
            axiom_refs=[axiom_num],
            source=' '.join(source_parts)
        )
        
        self.doc.nodes.append(node)
        self.doc.axioms_used.append(axiom_num)
        self.pending_comment = None
        
    def _parse_function(self, line: int, col: int):
        """Parse function declaration"""
        self._advance()  # consume 'function'
        
        name = "anonymous"
        if self._current() and self._current()[0] == 'ident':
            name = self._current()[1]
            self._advance()
            
        # Collect signature
        sig_parts = [f"function {name}"]
        paren_depth = 0
        
        while self._current():
            kind, value, _, _ = self._current()
            
            if value == '(':
                paren_depth += 1
            elif value == ')':
                paren_depth -= 1
            elif value == '=' and paren_depth == 0:
                sig_parts.append(value)
                self._advance()
                break
                
            sig_parts.append(value)
            self._advance()
            
        node = DocNode(
            name=name,
            node_type=NodeType.FUNCTION,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
            signature=' '.join(sig_parts),
        )
        
        # Check for axiom references in signature
        for part in sig_parts:
            match = re.match(r'o(\d+)', part)
            if match:
                node.axiom_refs.append(int(match.group(1)))
                
        self.doc.nodes.append(node)
        self.pending_comment = None
        
    def _parse_type(self, line: int, col: int):
        """Parse type declaration"""
        self._advance()  # consume 'type'
        
        name = "anonymous"
        if self._current() and self._current()[0] == 'ident':
            name = self._current()[1]
            self._advance()
            
        node = DocNode(
            name=name,
            node_type=NodeType.TYPE,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
        )
        
        self.doc.nodes.append(node)
        self.pending_comment = None
        
    def _parse_record(self, line: int, col: int):
        """Parse record declaration"""
        self._advance()  # consume 'record'
        
        name = "anonymous"
        if self._current() and self._current()[0] == 'ident':
            name = self._current()[1]
            self._advance()
            
        # Parse fields
        fields = []
        if self._current() and self._current()[1] == '{':
            self._advance()  # consume '{'
            brace_depth = 1
            
            while self._current() and brace_depth > 0:
                kind, value, _, _ = self._current()
                if value == '{':
                    brace_depth += 1
                elif value == '}':
                    brace_depth -= 1
                elif kind == 'ident' and brace_depth == 1:
                    fields.append(value)
                self._advance()
                
        node = DocNode(
            name=name,
            node_type=NodeType.RECORD,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
            signature=f"record {name} {{ {', '.join(fields)} }}",
        )
        
        self.doc.nodes.append(node)
        self.pending_comment = None
        
    def _parse_module(self, line: int, col: int):
        """Parse module declaration"""
        self._advance()  # consume 'module'
        
        name = "anonymous"
        if self._current() and self._current()[0] == 'ident':
            name = self._current()[1]
            self._advance()
            
        node = DocNode(
            name=name,
            node_type=NodeType.MODULE,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
        )
        
        self.doc.nodes.append(node)
        self.pending_comment = None
        
    def _parse_define(self, line: int, col: int):
        """Parse Define statement (configuration space)"""
        self._advance()  # consume 'Define'
        
        # Check for 'Space' keyword
        is_space = False
        if self._current() and self._current()[1] == 'Space':
            is_space = True
            self._advance()
            
        name = "anonymous"
        if self._current() and self._current()[0] == 'ident':
            name = self._current()[1]
            self._advance()
            
        node = DocNode(
            name=name,
            node_type=NodeType.CONFIG_SPACE if is_space else NodeType.STATEMENT,
            line=line,
            column=col,
            docstring=self.pending_comment if self.pending_comment_line == line - 1 else None,
            signature=f"Define {'Space ' if is_space else ''}{name}",
        )
        
        self.doc.nodes.append(node)
        self.pending_comment = None


class DocFormatter:
    """Format documentation for output"""
    
    @staticmethod
    def to_text(doc: MadDoc, color: bool = True) -> str:
        """Format documentation as plain text"""
        lines = []
        C = Color if color else type('NoColor', (), {k: '' for k in dir(Color)})()
        
        # Header
        lines.append(f"{C.BOLD}{C.HEADER}{'=' * 70}{C.ENDC}")
        lines.append(f"{C.BOLD}Module: {doc.module_name}{C.ENDC}")
        lines.append(f"File: {doc.filepath}")
        lines.append(f"Generated: {doc.timestamp}")
        lines.append(f"{C.HEADER}{'=' * 70}{C.ENDC}")
        
        # Module docstring
        if doc.docstring:
            lines.append("")
            lines.append(f"{C.CYAN}DESCRIPTION{C.ENDC}")
            lines.append(f"    {doc.docstring}")
            
        # Axioms used
        if doc.axioms_used:
            lines.append("")
            lines.append(f"{C.YELLOW}AXIOMS USED{C.ENDC}")
            for ax in sorted(set(doc.axioms_used)):
                name, formula = AXIOMS.get(ax, ("Unknown", "?"))
                lines.append(f"    {C.GREEN}o{ax}{C.ENDC}: {name}")
                lines.append(f"        {formula}")
                
        # Functions
        functions = [n for n in doc.nodes if n.node_type == NodeType.FUNCTION]
        if functions:
            lines.append("")
            lines.append(f"{C.BLUE}FUNCTIONS{C.ENDC}")
            for func in functions:
                lines.append(f"    {C.GREEN}{func.name}{C.ENDC}")
                if func.signature:
                    lines.append(f"        {func.signature}")
                if func.docstring:
                    lines.append(f"        {C.CYAN}{func.docstring}{C.ENDC}")
                if func.axiom_refs:
                    refs = ', '.join(f'o{a}' for a in func.axiom_refs)
                    lines.append(f"        Axioms: {refs}")
                    
        # Types
        types = [n for n in doc.nodes if n.node_type == NodeType.TYPE]
        if types:
            lines.append("")
            lines.append(f"{C.BLUE}TYPES{C.ENDC}")
            for t in types:
                lines.append(f"    {C.GREEN}{t.name}{C.ENDC}")
                if t.docstring:
                    lines.append(f"        {C.CYAN}{t.docstring}{C.ENDC}")
                    
        # Records
        records = [n for n in doc.nodes if n.node_type == NodeType.RECORD]
        if records:
            lines.append("")
            lines.append(f"{C.BLUE}RECORDS{C.ENDC}")
            for r in records:
                lines.append(f"    {C.GREEN}{r.name}{C.ENDC}")
                if r.signature:
                    lines.append(f"        {r.signature}")
                if r.docstring:
                    lines.append(f"        {C.CYAN}{r.docstring}{C.ENDC}")
                    
        # Configuration Spaces
        spaces = [n for n in doc.nodes if n.node_type == NodeType.CONFIG_SPACE]
        if spaces:
            lines.append("")
            lines.append(f"{C.BLUE}CONFIGURATION SPACES{C.ENDC}")
            for s in spaces:
                lines.append(f"    {C.GREEN}{s.name}{C.ENDC} (Ω)")
                if s.signature:
                    lines.append(f"        {s.signature}")
                if s.docstring:
                    lines.append(f"        {C.CYAN}{s.docstring}{C.ENDC}")
                    
        # Axiom statements
        axioms = [n for n in doc.nodes if n.node_type == NodeType.AXIOM]
        if axioms:
            lines.append("")
            lines.append(f"{C.BLUE}AXIOM APPLICATIONS{C.ENDC}")
            for ax in axioms:
                lines.append(f"    Line {ax.line}: {C.YELLOW}{ax.source}{C.ENDC}")
                
        # Modules
        modules = [n for n in doc.nodes if n.node_type == NodeType.MODULE]
        if modules:
            lines.append("")
            lines.append(f"{C.BLUE}MODULES{C.ENDC}")
            for m in modules:
                lines.append(f"    {C.GREEN}{m.name}{C.ENDC}")
                if m.docstring:
                    lines.append(f"        {C.CYAN}{m.docstring}{C.ENDC}")
                    
        lines.append("")
        lines.append(f"{C.HEADER}{'=' * 70}{C.ENDC}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def to_html(doc: MadDoc) -> str:
        """Format documentation as HTML"""
        html = ["""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MADDOC: {module}</title>
    <style>
        :root {{
            --bg: #1a1a2e;
            --fg: #eee;
            --accent: #e94560;
            --secondary: #0f3460;
            --code-bg: #16213e;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: var(--bg);
            color: var(--fg);
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        h1 {{ color: var(--accent); border-bottom: 2px solid var(--accent); }}
        h2 {{ color: #4a9fff; margin-top: 2rem; }}
        h3 {{ color: #7fff7f; }}
        .docstring {{ 
            background: var(--secondary);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        .signature {{
            font-family: 'Fira Code', monospace;
            background: var(--code-bg);
            padding: 0.5rem 1rem;
            border-radius: 4px;
            border-left: 3px solid var(--accent);
        }}
        .axiom {{
            display: inline-block;
            background: var(--accent);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            margin: 0.2rem;
            font-size: 0.9rem;
        }}
        .axiom-desc {{
            background: var(--code-bg);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
        }}
        .node {{ 
            margin: 1rem 0;
            padding: 1rem;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }}
        .meta {{
            color: #888;
            font-size: 0.85rem;
        }}
        code {{
            font-family: 'Fira Code', monospace;
            background: var(--code-bg);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
""".format(module=doc.module_name)]

        html.append(f"<h1>📚 {doc.module_name}</h1>")
        html.append(f"<p class='meta'>File: <code>{doc.filepath}</code> | Generated: {doc.timestamp}</p>")
        
        if doc.docstring:
            html.append(f"<div class='docstring'>{doc.docstring}</div>")
            
        # Axioms used
        if doc.axioms_used:
            html.append("<h2>🔮 Axioms Used</h2>")
            for ax in sorted(set(doc.axioms_used)):
                name, formula = AXIOMS.get(ax, ("Unknown", "?"))
                html.append(f"""
                <div class='axiom-desc'>
                    <span class='axiom'>o{ax}</span> <strong>{name}</strong>
                    <br><code>{formula}</code>
                </div>
                """)
                
        # Group nodes by type
        for node_type, title, emoji in [
            (NodeType.FUNCTION, "Functions", "⚙️"),
            (NodeType.TYPE, "Types", "📐"),
            (NodeType.RECORD, "Records", "📋"),
            (NodeType.CONFIG_SPACE, "Configuration Spaces (Ω)", "🌌"),
            (NodeType.MODULE, "Modules", "📦"),
            (NodeType.AXIOM, "Axiom Applications", "✨"),
        ]:
            nodes = [n for n in doc.nodes if n.node_type == node_type]
            if nodes:
                html.append(f"<h2>{emoji} {title}</h2>")
                for node in nodes:
                    html.append("<div class='node'>")
                    html.append(f"<h3>{node.name}</h3>")
                    html.append(f"<p class='meta'>Line {node.line}</p>")
                    if node.signature:
                        html.append(f"<div class='signature'>{node.signature}</div>")
                    if node.docstring:
                        html.append(f"<div class='docstring'>{node.docstring}</div>")
                    if node.axiom_refs:
                        html.append("<p>Axioms: ")
                        for a in node.axiom_refs:
                            html.append(f"<span class='axiom'>o{a}</span>")
                        html.append("</p>")
                    html.append("</div>")
                    
        html.append("""
<footer style="margin-top: 3rem; text-align: center; color: #666;">
    <p>Generated by MADDOC - MADLAD Documentation Generator</p>
    <p>Ring 6 | Axiom 5: Ω = ⋃ᵢ Ωᵢ</p>
</footer>
</body>
</html>
""")
        return '\n'.join(html)
    
    @staticmethod
    def to_json(doc: MadDoc) -> str:
        """Format documentation as JSON"""
        return json.dumps(doc.to_dict(), indent=2)
    
    @staticmethod
    def to_markdown(doc: MadDoc) -> str:
        """Format documentation as Markdown"""
        lines = []
        
        lines.append(f"# {doc.module_name}")
        lines.append("")
        lines.append(f"**File:** `{doc.filepath}`")
        lines.append(f"**Generated:** {doc.timestamp}")
        lines.append("")
        
        if doc.docstring:
            lines.append("## Description")
            lines.append("")
            lines.append(doc.docstring)
            lines.append("")
            
        if doc.axioms_used:
            lines.append("## Axioms Used")
            lines.append("")
            for ax in sorted(set(doc.axioms_used)):
                name, formula = AXIOMS.get(ax, ("Unknown", "?"))
                lines.append(f"- **o{ax}**: {name}")
                lines.append(f"  - `{formula}`")
            lines.append("")
            
        for node_type, title in [
            (NodeType.FUNCTION, "Functions"),
            (NodeType.TYPE, "Types"),
            (NodeType.RECORD, "Records"),
            (NodeType.CONFIG_SPACE, "Configuration Spaces"),
            (NodeType.MODULE, "Modules"),
        ]:
            nodes = [n for n in doc.nodes if n.node_type == node_type]
            if nodes:
                lines.append(f"## {title}")
                lines.append("")
                for node in nodes:
                    lines.append(f"### {node.name}")
                    lines.append("")
                    if node.signature:
                        lines.append(f"```mdld")
                        lines.append(node.signature)
                        lines.append("```")
                        lines.append("")
                    if node.docstring:
                        lines.append(node.docstring)
                        lines.append("")
                    if node.axiom_refs:
                        refs = ', '.join(f'`o{a}`' for a in node.axiom_refs)
                        lines.append(f"**Axioms:** {refs}")
                        lines.append("")
                        
        return '\n'.join(lines)


def document_file(filepath: str, format: str = "text") -> str:
    """Document a single MDLD file"""
    with open(filepath, 'r') as f:
        source = f.read()
        
    parser = MDLDParser(source, filepath)
    doc = parser.parse()
    
    if format == "json":
        return DocFormatter.to_json(doc)
    elif format == "html":
        return DocFormatter.to_html(doc)
    elif format == "markdown" or format == "md":
        return DocFormatter.to_markdown(doc)
    else:
        return DocFormatter.to_text(doc)


def document_directory(dirpath: str, format: str = "text") -> Dict[str, str]:
    """Document all MDLD files in a directory"""
    results = {}
    path = Path(dirpath)
    
    for mdld_file in path.rglob("*.mdld"):
        try:
            results[str(mdld_file)] = document_file(str(mdld_file), format)
        except Exception as e:
            results[str(mdld_file)] = f"Error: {e}"
            
    return results


class DocHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for documentation server"""
    
    def __init__(self, *args, docs_dir: str = ".", **kwargs):
        self.docs_dir = docs_dir
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            # Generate index
            html = ["<html><head><title>MADDOC Index</title></head><body>"]
            html.append("<h1>MADDOC Documentation Index</h1>")
            html.append("<ul>")
            
            for mdld_file in Path(self.docs_dir).rglob("*.mdld"):
                rel_path = mdld_file.relative_to(self.docs_dir)
                html.append(f'<li><a href="/doc/{rel_path}">{rel_path}</a></li>')
                
            html.append("</ul></body></html>")
            self.wfile.write('\n'.join(html).encode())
            
        elif self.path.startswith("/doc/"):
            filepath = self.path[5:]  # Remove '/doc/'
            full_path = Path(self.docs_dir) / filepath
            
            if full_path.exists() and full_path.suffix == ".mdld":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                doc_html = document_file(str(full_path), "html")
                self.wfile.write(doc_html.encode())
            else:
                self.send_error(404, "File not found")
        else:
            super().do_GET()


def serve_docs(directory: str = ".", port: int = 8080):
    """Start a documentation server"""
    handler = lambda *args, **kwargs: DocHandler(*args, docs_dir=directory, **kwargs)
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"MADDOC Server running at http://localhost:{port}")
        print(f"Serving documentation for: {directory}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MADDOC - MADLAD Documentation Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    maddoc example.mdld              # Document a file
    maddoc src/                      # Document a directory
    maddoc --format html example.mdld # Generate HTML
    maddoc --serve 8080              # Start doc server
    maddoc --json example.mdld       # Output JSON AST
    
Ring 6 Tool | Axiom 5: Ω = ⋃ᵢ Ωᵢ
"""
    )
    
    parser.add_argument("path", nargs="?", default=".",
                       help="File or directory to document")
    parser.add_argument("--format", "-f", choices=["text", "html", "json", "markdown", "md"],
                       default="text", help="Output format")
    parser.add_argument("--json", action="store_true",
                       help="Shortcut for --format json")
    parser.add_argument("--html", action="store_true",
                       help="Shortcut for --format html")
    parser.add_argument("--serve", "-s", type=int, nargs="?", const=8080, metavar="PORT",
                       help="Start documentation server")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")
    parser.add_argument("--version", "-v", action="version",
                       version="MADDOC 1.0.0 (Ring 6)")
    parser.add_argument("--axiom", "-a", type=int,
                       help="Show axiom documentation")
    
    args = parser.parse_args()
    
    # Show axiom documentation
    if args.axiom:
        if args.axiom in AXIOMS:
            name, formula = AXIOMS[args.axiom]
            print(f"{Color.BOLD}Axiom {args.axiom}: {name}{Color.ENDC}")
            print(f"{Color.CYAN}{formula}{Color.ENDC}")
        else:
            print(f"Unknown axiom: {args.axiom}")
        return
    
    # Start server
    if args.serve:
        serve_docs(args.path, args.serve)
        return
        
    # Determine format
    format = args.format
    if args.json:
        format = "json"
    elif args.html:
        format = "html"
        
    # Document file or directory
    path = Path(args.path)
    
    if path.is_file():
        result = document_file(str(path), format)
    elif path.is_dir():
        results = document_directory(str(path), format)
        result = '\n\n'.join(f"# {f}\n{r}" for f, r in results.items())
    else:
        # Try to read from stdin
        if sys.stdin.isatty():
            parser.print_help()
            return
        source = sys.stdin.read()
        doc_parser = MDLDParser(source, "<stdin>")
        doc = doc_parser.parse()
        if format == "json":
            result = DocFormatter.to_json(doc)
        elif format == "html":
            result = DocFormatter.to_html(doc)
        elif format in ("markdown", "md"):
            result = DocFormatter.to_markdown(doc)
        else:
            result = DocFormatter.to_text(doc, not args.no_color)
            
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Documentation written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
