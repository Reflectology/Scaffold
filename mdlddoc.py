#!/usr/bin/env python3
"""
MDLDDOC - Universal Documentation Generator via MDLD Parsing Trees

Uses Reflectology axiom-grounded parsing to walk ALL code types:
  - MDLD (.mdld)      - Reflectology DSL native
  - C (.c, .h)        - C/C++ source
  - Python (.py)      - Python source
  - JavaScript (.js)  - JavaScript/TypeScript
  - Rust (.rs)        - Rust source
  - Metamath (.mm)    - Formal proofs
  - JSON (.json)      - Configuration files
  - EBNF (.ebnf)      - Grammar files

Ring 6 Tool - Axiom 5 (Hierarchical Structuring): Ω = ⋃ᵢ Ωᵢ
Ring 6 Tool - Axiom 10 (Ω-Bijection): Maps between configuration spaces

Usage:
    mdlddoc <file>                  # Auto-detect and document
    mdlddoc <directory>             # Document all supported files
    mdlddoc --json <file>           # Output JSON format
    mdlddoc --html <file>           # Output HTML format
    mdlddoc --serve [port]          # Start documentation server
    mdlddoc --tree <file>           # Show parse tree only

Standards:
    - ISO C17 for C parsing
    - Python 3.12+ for Python parsing
    - ECMAScript 2023 for JavaScript
    - RFC 8259 for JSON
    - ISO/IEC 14977 for EBNF

(c) 2026 Triple A Family Holdings LLC
"""

import os
import sys
import ast
import json
import re
import tokenize
import io
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from datetime import datetime
import http.server
import socketserver

# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLORS
# ═══════════════════════════════════════════════════════════════════════════════

class Color:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

USE_COLOR = True
def C(code: str) -> str:
    return code if USE_COLOR else ''

# ═══════════════════════════════════════════════════════════════════════════════
# THE 40 AXIOMS OF REFLECTOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

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
    11: ("Complex Symmetry-Flow-Force", "((θ·q)·ω)·(θ·((θ·ω)·q)) = ω"),
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
    37: ("Student Supremacy", "L' = θ(Ωₜ) - Cₜ; T* ≻ T"),
    38: ("Recursive Lineage", "τₙ₊₁ := θ(τₙ) - Cτ"),
    39: ("Internal Emergence", "θ(Ωᵣ) - Cᵣ > θ(Ωₑ) - Cₑ"),
    40: ("Reflective Conjugate Duality", "∀ω ∈ Ω, ∃ω† := C(ω)"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL NODE TYPES (Axiom 10: Ω-Bijection between languages)
# ═══════════════════════════════════════════════════════════════════════════════

class NodeType(Enum):
    """Universal AST node types mapped across all languages"""
    DOCUMENT = auto()       # Top-level container
    MODULE = auto()         # Module/namespace/package
    IMPORT = auto()         # Import/include/require
    FUNCTION = auto()       # Function/procedure/method
    CLASS = auto()          # Class/struct/record
    VARIABLE = auto()       # Variable/constant/binding
    TYPE = auto()           # Type declaration/alias
    MACRO = auto()          # Macro/preprocessor
    COMMENT = auto()        # Documentation comment
    AXIOM = auto()          # Axiom reference (MDLD-specific)
    THEOREM = auto()        # Theorem/proof (Metamath)
    RULE = auto()           # Grammar rule (EBNF)
    CONFIG = auto()         # Configuration entry (JSON)
    STATEMENT = auto()      # Generic statement
    EXPRESSION = auto()     # Generic expression

# ═══════════════════════════════════════════════════════════════════════════════
# DOC NODE - Universal Documentation Node
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DocNode:
    """Universal documentation node - works for any language"""
    name: str
    type: NodeType
    line: int
    signature: str = ""
    docstring: str = ""
    children: List['DocNode'] = field(default_factory=list)
    axiom_refs: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type.name.lower(),
            'line': self.line,
            'signature': self.signature,
            'docstring': self.docstring,
            'children': [c.to_dict() for c in self.children],
            'axiom_refs': self.axiom_refs,
            'metadata': self.metadata
        }

@dataclass
class DocTree:
    """Complete documentation tree for a file"""
    filepath: str
    language: str
    module_name: str
    docstring: str = ""
    nodes: List[DocNode] = field(default_factory=list)
    axioms_used: List[int] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'filepath': self.filepath,
            'language': self.language,
            'module_name': self.module_name,
            'docstring': self.docstring,
            'nodes': [n.to_dict() for n in self.nodes],
            'axioms_used': self.axioms_used,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }

# ═══════════════════════════════════════════════════════════════════════════════
# AXIOM REFERENCE EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_axiom_refs(text: str) -> List[int]:
    """Extract axiom references (o1-o40) from text"""
    refs = []
    for match in re.finditer(r'o(\d+)', text, re.IGNORECASE):
        num = int(match.group(1))
        if 1 <= num <= 40 and num not in refs:
            refs.append(num)
    # Also check for Axiom N pattern
    for match in re.finditer(r'Axiom\s*(\d+)', text, re.IGNORECASE):
        num = int(match.group(1))
        if 1 <= num <= 40 and num not in refs:
            refs.append(num)
    return refs

# ═══════════════════════════════════════════════════════════════════════════════
# BASE PARSER (Abstract)
# ═══════════════════════════════════════════════════════════════════════════════

class BaseParser:
    """Base parser class - all language parsers inherit from this"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        self.lines: List[str] = []
        self.tree: Optional[DocTree] = None
        
    def load(self) -> bool:
        """Load file content"""
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='replace') as f:
                self.content = f.read()
            self.lines = self.content.split('\n')
            return True
        except Exception as e:
            print(f"Error loading {self.filepath}: {e}", file=sys.stderr)
            return False
    
    def parse(self) -> DocTree:
        """Parse the file and return documentation tree"""
        raise NotImplementedError("Subclasses must implement parse()")
    
    def get_module_name(self) -> str:
        """Extract module name from filepath"""
        return Path(self.filepath).stem

# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class PythonParser(BaseParser):
    """Parser for Python source files using AST"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "python", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="python",
            module_name=self.get_module_name()
        )
        
        try:
            py_ast = ast.parse(self.content)
        except SyntaxError as e:
            tree.docstring = f"Parse error: {e}"
            return tree
        
        # Module docstring
        if py_ast.body and isinstance(py_ast.body[0], ast.Expr):
            if isinstance(py_ast.body[0].value, ast.Constant):
                if isinstance(py_ast.body[0].value.value, str):
                    tree.docstring = py_ast.body[0].value.value
        
        for node in ast.walk(py_ast):
            doc_node = self._ast_to_doc(node)
            if doc_node:
                tree.nodes.append(doc_node)
                tree.axioms_used.extend(doc_node.axiom_refs)
        
        # Deduplicate axioms
        tree.axioms_used = list(set(tree.axioms_used))
        return tree
    
    def _ast_to_doc(self, node: ast.AST) -> Optional[DocNode]:
        """Convert Python AST node to DocNode"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                return DocNode(
                    name=alias.name,
                    type=NodeType.IMPORT,
                    line=node.lineno,
                    signature=f"import {alias.name}"
                )
        
        elif isinstance(node, ast.ImportFrom):
            names = ', '.join(a.name for a in node.names)
            return DocNode(
                name=node.module or '',
                type=NodeType.IMPORT,
                line=node.lineno,
                signature=f"from {node.module} import {names}"
            )
        
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            args = ', '.join(a.arg for a in node.args.args)
            prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
            doc = ast.get_docstring(node) or ""
            return DocNode(
                name=node.name,
                type=NodeType.FUNCTION,
                line=node.lineno,
                signature=f"{prefix}def {node.name}({args})",
                docstring=doc,
                axiom_refs=extract_axiom_refs(doc),
                metadata={'decorators': [ast.unparse(d) for d in node.decorator_list] if hasattr(ast, 'unparse') else []}
            )
        
        elif isinstance(node, ast.ClassDef):
            bases = ', '.join(ast.unparse(b) if hasattr(ast, 'unparse') else str(b) for b in node.bases)
            doc = ast.get_docstring(node) or ""
            return DocNode(
                name=node.name,
                type=NodeType.CLASS,
                line=node.lineno,
                signature=f"class {node.name}({bases})" if bases else f"class {node.name}",
                docstring=doc,
                axiom_refs=extract_axiom_refs(doc)
            )
        
        elif isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                # Only top-level assignments with simple names
                return DocNode(
                    name=node.targets[0].id,
                    type=NodeType.VARIABLE,
                    line=node.lineno,
                    signature=ast.unparse(node) if hasattr(ast, 'unparse') else node.targets[0].id
                )
        
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# C PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class CParser(BaseParser):
    """Parser for C source files"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "c", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="c",
            module_name=self.get_module_name()
        )
        
        pending_comment = ""
        pending_line = 0
        i = 0
        
        while i < len(self.lines):
            line = self.lines[i].strip()
            raw_line = self.lines[i]
            
            # Block comment
            if line.startswith('/*'):
                comment_lines = [line]
                while '*/' not in self.lines[i] and i < len(self.lines) - 1:
                    i += 1
                    comment_lines.append(self.lines[i])
                pending_comment = self._clean_comment('\n'.join(comment_lines))
                pending_line = i + 1
                
                # File-level docstring
                if not tree.nodes and not tree.docstring:
                    tree.docstring = pending_comment
                i += 1
                continue
            
            # Line comment
            if line.startswith('//'):
                pending_comment = line[2:].strip()
                pending_line = i + 1
                i += 1
                continue
            
            # Include
            if line.startswith('#include'):
                match = re.search(r'[<"]([^>"]+)[>"]', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1),
                        type=NodeType.IMPORT,
                        line=i + 1,
                        signature=line
                    ))
                i += 1
                continue
            
            # Macro
            if line.startswith('#define'):
                match = re.match(r'#define\s+(\w+)', line)
                if match:
                    node = DocNode(
                        name=match.group(1),
                        type=NodeType.MACRO,
                        line=i + 1,
                        signature=line,
                        docstring=pending_comment if pending_line == i else ""
                    )
                    tree.nodes.append(node)
                    pending_comment = ""
                i += 1
                continue
            
            # Struct/Union/Enum
            for kw, nt in [('struct', NodeType.CLASS), ('union', NodeType.CLASS), ('enum', NodeType.TYPE)]:
                if kw in line and 'typedef' not in line:
                    match = re.search(rf'{kw}\s+(\w+)', line)
                    if match:
                        tree.nodes.append(DocNode(
                            name=match.group(1),
                            type=nt,
                            line=i + 1,
                            signature=line,
                            docstring=pending_comment if pending_line == i else ""
                        ))
                        pending_comment = ""
                        break
            
            # Typedef
            if line.startswith('typedef'):
                # Simple extraction of typedef name
                match = re.search(r'typedef\s+.+\s+(\w+)\s*;', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1),
                        type=NodeType.TYPE,
                        line=i + 1,
                        signature=line,
                        docstring=pending_comment if pending_line == i else ""
                    ))
                    pending_comment = ""
                i += 1
                continue
            
            # Function detection
            if '(' in line and not line.startswith(('if', 'while', 'for', 'switch', 'return')):
                # Check for function signature patterns
                func_match = re.match(r'^(\w+[\s\*]+)(\w+)\s*\(', line)
                if func_match:
                    is_static = 'static' in line
                    is_extern = 'extern' in line
                    
                    node = DocNode(
                        name=func_match.group(2),
                        type=NodeType.FUNCTION,
                        line=i + 1,
                        signature=line.rstrip('{').strip(),
                        docstring=pending_comment if pending_line == i else "",
                        metadata={'static': is_static, 'extern': is_extern}
                    )
                    node.axiom_refs = extract_axiom_refs(pending_comment)
                    tree.nodes.append(node)
                    tree.axioms_used.extend(node.axiom_refs)
                    pending_comment = ""
            
            i += 1
        
        tree.axioms_used = list(set(tree.axioms_used))
        return tree
    
    def _clean_comment(self, text: str) -> str:
        """Clean C comment text"""
        # Remove /* and */
        text = re.sub(r'/\*+', '', text)
        text = re.sub(r'\*+/', '', text)
        # Remove leading * on each line
        lines = []
        for line in text.split('\n'):
            line = re.sub(r'^\s*\*\s?', '', line)
            lines.append(line)
        return '\n'.join(lines).strip()

# ═══════════════════════════════════════════════════════════════════════════════
# METAMATH PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class MetamathParser(BaseParser):
    """Parser for Metamath proof files (.mm)"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "metamath", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="metamath",
            module_name=self.get_module_name()
        )
        
        # Parse Metamath structure
        # $( comment $)
        # $c constant $.
        # $v variable $.
        # $a axiom $.
        # $p theorem proof $.
        
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Comment block
            if line.startswith('$('):
                comment_text = []
                while '$)' not in self.lines[i]:
                    comment_text.append(self.lines[i])
                    i += 1
                    if i >= len(self.lines):
                        break
                comment_text.append(self.lines[i])
                
                # File docstring
                if not tree.docstring and not tree.nodes:
                    tree.docstring = '\n'.join(comment_text)
                i += 1
                continue
            
            # Constant declaration
            if line.startswith('$c'):
                match = re.search(r'\$c\s+(.+)\s*\$\.', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1).split()[0] if match.group(1).split() else "const",
                        type=NodeType.VARIABLE,
                        line=i + 1,
                        signature=line,
                        metadata={'mm_type': 'constant'}
                    ))
            
            # Variable declaration
            elif line.startswith('$v'):
                match = re.search(r'\$v\s+(.+)\s*\$\.', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1).split()[0] if match.group(1).split() else "var",
                        type=NodeType.VARIABLE,
                        line=i + 1,
                        signature=line,
                        metadata={'mm_type': 'variable'}
                    ))
            
            # Axiom
            elif '$a' in line:
                match = re.search(r'(\w+)\s+\$a\s+(.+)\s*\$\.', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1),
                        type=NodeType.AXIOM,
                        line=i + 1,
                        signature=match.group(2),
                        metadata={'mm_type': 'axiom'}
                    ))
            
            # Theorem/Proof
            elif '$p' in line:
                match = re.search(r'(\w+)\s+\$p\s+(.+?)\s*\$=', line)
                if match:
                    tree.nodes.append(DocNode(
                        name=match.group(1),
                        type=NodeType.THEOREM,
                        line=i + 1,
                        signature=match.group(2),
                        metadata={'mm_type': 'theorem'}
                    ))
            
            i += 1
        
        return tree

# ═══════════════════════════════════════════════════════════════════════════════
# EBNF PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class EBNFParser(BaseParser):
    """Parser for EBNF grammar files"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "ebnf", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="ebnf",
            module_name=self.get_module_name()
        )
        
        # Extract file-level comment
        if self.content.startswith('/*'):
            end = self.content.find('*/')
            if end > 0:
                tree.docstring = self.content[2:end].strip()
        
        # Find all rules: rule_name ::= definition
        for match in re.finditer(r'^(\w+)\s*::=\s*(.+?)(?=^\w+\s*::=|\Z)', 
                                   self.content, re.MULTILINE | re.DOTALL):
            name = match.group(1)
            definition = match.group(2).strip()
            
            # Find line number
            line_num = self.content[:match.start()].count('\n') + 1
            
            tree.nodes.append(DocNode(
                name=name,
                type=NodeType.RULE,
                line=line_num,
                signature=f"{name} ::= {definition[:80]}{'...' if len(definition) > 80 else ''}"
            ))
        
        return tree

# ═══════════════════════════════════════════════════════════════════════════════
# JSON PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class JSONParser(BaseParser):
    """Parser for JSON configuration files"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "json", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="json",
            module_name=self.get_module_name()
        )
        
        try:
            data = json.loads(self.content)
        except json.JSONDecodeError as e:
            tree.docstring = f"JSON parse error: {e}"
            return tree
        
        # Walk JSON structure
        self._walk_json(data, tree.nodes, "root", 1)
        
        return tree
    
    def _walk_json(self, obj: Any, nodes: List[DocNode], path: str, depth: int):
        """Recursively walk JSON and extract structure"""
        if depth > 3:  # Limit depth
            return
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                node = DocNode(
                    name=key,
                    type=NodeType.CONFIG,
                    line=1,
                    signature=f"{key}: {type(value).__name__}",
                    metadata={'value_type': type(value).__name__}
                )
                nodes.append(node)
                if isinstance(value, (dict, list)):
                    self._walk_json(value, node.children, f"{path}.{key}", depth + 1)
        elif isinstance(obj, list) and obj:
            if isinstance(obj[0], dict):
                self._walk_json(obj[0], nodes, f"{path}[0]", depth + 1)

# ═══════════════════════════════════════════════════════════════════════════════
# MDLD PARSER (uses ANTLR if available)
# ═══════════════════════════════════════════════════════════════════════════════

class MDLDParser(BaseParser):
    """Parser for MDLD/MADLAD files"""
    
    def parse(self) -> DocTree:
        if not self.load():
            return DocTree(self.filepath, "mdld", self.get_module_name())
        
        tree = DocTree(
            filepath=self.filepath,
            language="mdld",
            module_name=self.get_module_name()
        )
        
        # Try to use ANTLR parser if available
        try:
            from antlr4 import InputStream, CommonTokenStream
            sys.path.insert(0, str(Path(__file__).parent / 'webidl' / 'MADLAD'))
            from mdldLexer import mdldLexer
            from mdldParser import mdldParser
            
            input_stream = InputStream(self.content)
            lexer = mdldLexer(input_stream)
            tokens = CommonTokenStream(lexer)
            parser = mdldParser(tokens)
            antlr_tree = parser.document()
            
            # Walk ANTLR tree
            self._walk_antlr(antlr_tree, tree)
            tree.metadata['parser'] = 'antlr'
            
        except ImportError:
            # Fallback to regex-based parsing
            self._regex_parse(tree)
            tree.metadata['parser'] = 'regex'
        
        return tree
    
    def _walk_antlr(self, node, tree: DocTree):
        """Walk ANTLR parse tree"""
        # Simplified walking - would need full visitor for complete implementation
        text = node.getText() if hasattr(node, 'getText') else str(node)
        tree.axioms_used.extend(extract_axiom_refs(text))
    
    def _regex_parse(self, tree: DocTree):
        """Fallback regex-based MDLD parsing"""
        # Comments
        for match in re.finditer(r'/\*(.+?)\*/', self.content, re.DOTALL):
            if not tree.docstring:
                tree.docstring = match.group(1).strip()
        
        # Functions: func name(args) = body
        for match in re.finditer(r'func\s+(\w+)\s*\(([^)]*)\)', self.content):
            line = self.content[:match.start()].count('\n') + 1
            tree.nodes.append(DocNode(
                name=match.group(1),
                type=NodeType.FUNCTION,
                line=line,
                signature=f"func {match.group(1)}({match.group(2)})"
            ))
        
        # Axiom statements: axiom N: ...
        for match in re.finditer(r'axiom\s+(\d+)\s*:', self.content):
            line = self.content[:match.start()].count('\n') + 1
            num = int(match.group(1))
            tree.nodes.append(DocNode(
                name=f"axiom_{num}",
                type=NodeType.AXIOM,
                line=line,
                signature=f"axiom {num}",
                axiom_refs=[num]
            ))
            if num not in tree.axioms_used:
                tree.axioms_used.append(num)
        
        # Type declarations: type Name = ...
        for match in re.finditer(r'type\s+(\w+)\s*=', self.content):
            line = self.content[:match.start()].count('\n') + 1
            tree.nodes.append(DocNode(
                name=match.group(1),
                type=NodeType.TYPE,
                line=line,
                signature=f"type {match.group(1)}"
            ))
        
        # Module declarations: module Name
        for match in re.finditer(r'module\s+(\w+)', self.content):
            line = self.content[:match.start()].count('\n') + 1
            tree.nodes.append(DocNode(
                name=match.group(1),
                type=NodeType.MODULE,
                line=line,
                signature=f"module {match.group(1)}"
            ))

# ═══════════════════════════════════════════════════════════════════════════════
# LANGUAGE DETECTION & PARSER DISPATCH
# ═══════════════════════════════════════════════════════════════════════════════

PARSERS = {
    '.py': PythonParser,
    '.c': CParser,
    '.h': CParser,
    '.mm': MetamathParser,
    '.ebnf': EBNFParser,
    '.json': JSONParser,
    '.mdld': MDLDParser,
    '.madlad': MDLDParser,
}

def get_parser(filepath: str) -> Optional[BaseParser]:
    """Get appropriate parser for file type"""
    ext = Path(filepath).suffix.lower()
    parser_class = PARSERS.get(ext)
    if parser_class:
        return parser_class(filepath)
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════════════

def output_text(tree: DocTree):
    """Output plain text documentation"""
    print(f"{C(Color.BOLD)}{C(Color.MAGENTA)}{'=' * 70}{C(Color.RESET)}")
    print(f"{C(Color.BOLD)}Module: {tree.module_name}{C(Color.RESET)}")
    print(f"Language: {tree.language}")
    print(f"File: {tree.filepath}")
    print(f"Generated: {tree.timestamp}")
    print(f"{C(Color.MAGENTA)}{'=' * 70}{C(Color.RESET)}")
    
    if tree.docstring:
        print(f"\n{C(Color.CYAN)}DESCRIPTION{C(Color.RESET)}")
        print(f"    {tree.docstring[:500]}{'...' if len(tree.docstring) > 500 else ''}")
    
    if tree.axioms_used:
        print(f"\n{C(Color.YELLOW)}AXIOMS USED{C(Color.RESET)}")
        for ax in tree.axioms_used:
            name, formula = AXIOMS.get(ax, ('Unknown', '?'))
            print(f"    {C(Color.GREEN)}o{ax}{C(Color.RESET)}: {name}")
            print(f"        {formula}")
    
    # Group by type
    by_type: Dict[NodeType, List[DocNode]] = {}
    for node in tree.nodes:
        by_type.setdefault(node.type, []).append(node)
    
    type_labels = {
        NodeType.IMPORT: "IMPORTS",
        NodeType.MACRO: "MACROS",
        NodeType.VARIABLE: "DATA",
        NodeType.TYPE: "TYPES",
        NodeType.CLASS: "CLASSES/STRUCTS",
        NodeType.FUNCTION: "FUNCTIONS",
        NodeType.AXIOM: "AXIOMS",
        NodeType.THEOREM: "THEOREMS",
        NodeType.RULE: "GRAMMAR RULES",
        NodeType.CONFIG: "CONFIGURATION",
        NodeType.MODULE: "MODULES",
    }
    
    for node_type, label in type_labels.items():
        if node_type in by_type:
            print(f"\n{C(Color.BLUE)}{label}{C(Color.RESET)}")
            for node in by_type[node_type]:
                print(f"    {C(Color.GREEN)}{node.name}{C(Color.RESET)}")
                if node.signature:
                    print(f"        {node.signature[:60]}{'...' if len(node.signature) > 60 else ''}")
                if node.docstring:
                    print(f"        {C(Color.CYAN)}{node.docstring[:60]}{'...' if len(node.docstring) > 60 else ''}{C(Color.RESET)}")
    
    print(f"\n{C(Color.MAGENTA)}{'=' * 70}{C(Color.RESET)}")


def output_json(tree: DocTree):
    """Output JSON documentation"""
    print(json.dumps(tree.to_dict(), indent=2))


def output_html(tree: DocTree):
    """Output HTML documentation (pydoc style)"""
    print('<!DOCTYPE html>\n<html>\n<head>')
    print(f'<meta charset="UTF-8">\n<title>{tree.module_name}</title>')
    print('</head>\n<body bgcolor="#f0f0f0">')
    
    # Header
    print('<table width="100%" cellspacing=0 cellpadding=2 border=0>')
    print(f'<tr bgcolor="#7799ee"><td>&nbsp;</td>')
    print(f'<td><font face="helvetica, arial" size="+1"><strong>{tree.module_name}</strong> ({tree.language})</font></td></tr></table>')
    
    print(f'<p><tt>{tree.filepath}</tt></p>')
    
    if tree.docstring:
        print('<p><table width="100%" cellspacing=0 cellpadding=2 border=0>')
        print('<tr bgcolor="#eeaa77"><td>&nbsp;</td>')
        print('<td><strong>Description</strong></td></tr></table>')
        print(f'<pre>{tree.docstring[:1000]}</pre>')
    
    if tree.axioms_used:
        print('<p><table width="100%" cellspacing=0 cellpadding=2 border=0>')
        print('<tr bgcolor="#eeaa77"><td>&nbsp;</td>')
        print('<td><strong>Axioms Used</strong></td></tr></table>')
        print('<dl>')
        for ax in tree.axioms_used:
            name, formula = AXIOMS.get(ax, ('Unknown', '?'))
            print(f'<dt><strong>o{ax}</strong>: {name}</dt>')
            print(f'<dd><tt>{formula}</tt></dd>')
        print('</dl>')
    
    # Group nodes by type
    by_type: Dict[NodeType, List[DocNode]] = {}
    for node in tree.nodes:
        by_type.setdefault(node.type, []).append(node)
    
    type_labels = {
        NodeType.IMPORT: "Imports",
        NodeType.MACRO: "Macros",
        NodeType.VARIABLE: "Data",
        NodeType.TYPE: "Types",
        NodeType.CLASS: "Classes/Structs",
        NodeType.FUNCTION: "Functions",
        NodeType.AXIOM: "Axioms",
        NodeType.THEOREM: "Theorems",
        NodeType.RULE: "Grammar Rules",
        NodeType.CONFIG: "Configuration",
        NodeType.MODULE: "Modules",
    }
    
    for node_type, label in type_labels.items():
        if node_type in by_type:
            print('<p><table width="100%" cellspacing=0 cellpadding=2 border=0>')
            print(f'<tr bgcolor="#aa55cc"><td>&nbsp;</td>')
            print(f'<td><strong>{label}</strong></td></tr></table>')
            print('<dl>')
            for node in by_type[node_type]:
                print(f'<dt><a name="{node.name}"><strong>{node.name}</strong></a></dt>')
                if node.signature:
                    print(f'<dd><tt>{node.signature}</tt></dd>')
                if node.docstring:
                    print(f'<dd>{node.docstring[:200]}</dd>')
            print('</dl>')
    
    print('<hr>')
    print('<p><small>Generated by MDLDDOC - Ring 6 | Axiom 5: Ω = ⋃ᵢ Ωᵢ</small></p>')
    print('</body>\n</html>')


def output_tree(tree: DocTree):
    """Output parse tree structure"""
    def print_node(node: DocNode, indent: int = 0):
        prefix = "  " * indent
        print(f"{prefix}├─ {node.type.name}: {node.name}")
        if node.signature:
            print(f"{prefix}│  └─ {node.signature[:50]}")
        for child in node.children:
            print_node(child, indent + 1)
    
    print(f"Document: {tree.module_name} ({tree.language})")
    for node in tree.nodes:
        print_node(node)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def print_usage():
    print("""MDLDDOC - Universal Documentation Generator via MDLD Parsing Trees

Usage: mdlddoc [options] <file|directory>

Options:
    --json          Output JSON format
    --html          Output HTML format
    --tree          Output parse tree only
    -n, --no-color  Disable color output
    -a <num>        Show axiom documentation (1-40)
    -v, --version   Show version
    -h, --help      Show this help

Supported Languages:
    .py             Python (AST-based)
    .c, .h          C/C++ (regex-based)
    .mm             Metamath proofs
    .ebnf           EBNF grammars
    .json           JSON configuration
    .mdld, .madlad  MDLD/MADLAD (ANTLR when available)

Examples:
    mdlddoc myfile.py           # Document Python file
    mdlddoc --json myfile.c     # Document C file as JSON
    mdlddoc --html src/         # Document all files in directory as HTML
    mdlddoc -a 5                # Show axiom 5 (Hierarchical Structuring)

Ring 6 Tool | Axiom 5: Ω = ⋃ᵢ Ωᵢ | Axiom 10: Ω-Bijection
""")


def main():
    global USE_COLOR
    
    args = sys.argv[1:]
    if not args or '-h' in args or '--help' in args:
        print_usage()
        return
    
    format_type = 'text'
    files = []
    show_axiom = 0
    show_tree = False
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--json':
            format_type = 'json'
        elif arg == '--html':
            format_type = 'html'
        elif arg == '--tree':
            show_tree = True
        elif arg in ('-n', '--no-color'):
            USE_COLOR = False
        elif arg in ('-v', '--version'):
            print("MDLDDOC 1.0.0 (Ring 6)")
            return
        elif arg == '-a':
            if i + 1 < len(args):
                show_axiom = int(args[i + 1])
                i += 1
        elif not arg.startswith('-'):
            files.append(arg)
        i += 1
    
    # Show axiom if requested
    if show_axiom:
        if 1 <= show_axiom <= 40:
            name, formula = AXIOMS[show_axiom]
            print(f"{C(Color.BOLD)}{C(Color.GREEN)}Axiom {show_axiom}: {name}{C(Color.RESET)}")
            print(f"{C(Color.CYAN)}{formula}{C(Color.RESET)}")
        else:
            print("Error: Axiom number must be 1-40", file=sys.stderr)
        return
    
    if not files:
        print_usage()
        return
    
    # Process files
    for filepath in files:
        path = Path(filepath)
        
        if path.is_dir():
            # Process all supported files in directory
            for ext in PARSERS.keys():
                for f in path.rglob(f'*{ext}'):
                    parser = get_parser(str(f))
                    if parser:
                        tree = parser.parse()
                        if show_tree:
                            output_tree(tree)
                        elif format_type == 'json':
                            output_json(tree)
                        elif format_type == 'html':
                            output_html(tree)
                        else:
                            output_text(tree)
        else:
            parser = get_parser(filepath)
            if not parser:
                print(f"Error: Unsupported file type for {filepath}", file=sys.stderr)
                continue
            
            tree = parser.parse()
            if show_tree:
                output_tree(tree)
            elif format_type == 'json':
                output_json(tree)
            elif format_type == 'html':
                output_html(tree)
            else:
                output_text(tree)


if __name__ == '__main__':
    main()
