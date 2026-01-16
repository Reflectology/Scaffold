#!/usr/bin/env python3
"""Test what the generated mdldParser actually accepts"""

import sys
sys.path.insert(0, 'webidl/MADLAD')
from antlr4 import InputStream, CommonTokenStream
from mdldParser import mdldParser
from mdldLexer import mdldLexer

def test_parse(code, label):
    input_stream = InputStream(code)
    lexer = mdldLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = mdldParser(token_stream)
    parser.removeErrorListeners()
    
    class Counter:
        errors = 0
        def syntaxError(self, *args): self.errors += 1
        def reportAmbiguity(self, *a): pass
        def reportAttemptingFullContext(self, *a): pass
        def reportContextSensitivity(self, *a): pass
    
    c = Counter()
    parser.addErrorListener(c)
    tree = parser.document()
    status = "✅" if c.errors == 0 else f"❌ ({c.errors} err)"
    print(f"{status} {label}")
    return c.errors == 0

print("=== Single Expressions ===")
test_parse("loss(x)", "loss(x)")
test_parse("goodness(omega)", "goodness(omega)")
test_parse("gradient(f)", "gradient(f)")
test_parse("dual(state)", "dual(state)")
test_parse("entropy(dist)", "entropy(dist)")
test_parse("converge(seq)", "converge(seq)")

print("\n=== Axiom Keywords ===")
test_parse("o1(omega0)", "o1(omega0)")
test_parse("o21(x)", "o21(x)")
test_parse("o40(state)", "o40(state)")

print("\n=== Config Spaces ===")
test_parse("emptyset", "emptyset")
test_parse("omega", "omega")
test_parse("omega0", "omega0")

print("\n=== Let Bindings ===")
test_parse("let x = 1 in x", "let x = 1 in x")
test_parse("let f x = x in f(1)", "let f x = x in f(1)")

print("\n=== Assignments/Equations ===")
test_parse("x = 5", "x = 5")
test_parse("1 + 2", "1 + 2")
test_parse("a = b = c", "a = b = c (equation)")

print("\n=== Quantified ===")
test_parse("forall x : P(x)", "forall x : P(x)")
test_parse("exists y : Q(y)", "exists y : Q(y)")

print("\n=== Multi-statement (newline sep) ===")
test_parse("x = 1\ny = 2", "x=1 newline y=2")
test_parse("loss(a)\ngoodness(b)", "loss newline goodness")

print("\n=== Multi-statement (semicolon sep) ===")
test_parse("x = 1; y = 2", "x=1 ; y=2")
test_parse("loss(a); goodness(b)", "loss ; goodness")

print("\n=== Match Expression ===")
test_parse("match x with | A -> 1 | B -> 2", "match with pipes")

print("\n=== If Expression ===")
test_parse("if x then 1 else 2", "if-then-else")

print("\n=== Function Decl ===")
test_parse("function add(x: Int, y: Int) : Int = x + y", "function decl")

print("\n=== Record Decl ===")
test_parse("record Point { field x : Int field y : Int }", "record decl")

print("\n=== What works pattern ===")
# Axiom keywords work
test_parse("o1(emptyset)", "o1(emptyset)")
test_parse("o13(x)", "o13 loss axiom")
test_parse("o21(state)", "o21 goodness axiom")
test_parse("o25(f)", "o25 gradient axiom")

# Reflectology statements
test_parse("Define omega_space = emptyset", "Define space")
test_parse("Reduce x", "Reduce")
test_parse("Compute x", "Compute")
test_parse("Optimize x", "Optimize")
test_parse("IRE(config)", "IRE")
test_parse("DualSymmetry(a, b)", "DualSymmetry")

# More expressions
test_parse("calculate_theta(x)", "calculate_theta")
test_parse("apply_reflectology(state)", "apply_reflectology")

print("\n=== Standalone calls vs statements ===")
test_parse("simplify(x)", "simplify as stmt")
test_parse("y = simplify(x)", "y = simplify(x)")
test_parse("compose(f, g)", "compose")
test_parse("z = compose(f, g)", "z = compose")

print("\n=== Type decl ===")
test_parse("type MyType = Int", "type alias")

print("\n=== Module ===")
test_parse("open Foo", "open module")
test_parse("module M = struct { x = 1 }", "module struct")
