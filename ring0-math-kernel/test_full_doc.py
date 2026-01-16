#!/usr/bin/env python3
"""Test a full MDLD document"""
import sys
sys.path.insert(0, '/Users/bbfrmbk/Desktop/scaffold/Python/ring_python/webidl/MADLAD')
from antlr4 import InputStream, CommonTokenStream
from mdldParser import mdldParser
from mdldLexer import mdldLexer

def test(code, label):
    lexer = mdldLexer(InputStream(code))
    parser = mdldParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    class E:
        n = 0
        msg = ''
        def syntaxError(self, rec, sym, line, col, msg, e): 
            self.n += 1
            self.msg = f'L{line}:{col} {msg}'
        def reportAmbiguity(self, *a): pass
        def reportAttemptingFullContext(self, *a): pass
        def reportContextSensitivity(self, *a): pass
    e = E()
    parser.addErrorListener(e)
    parser.document()
    if e.n == 0:
        print(f'OK {label}')
    else:
        print(f'ERR {label}: {e.msg[:80]}')

# Single statements
test('x = 1', 'single assign')
test('o1(omega0)', 'o1 axiom')
test('Define s = emptyset', 'Define')

# Multi-line
test('x = 1\ny = 2', 'two lines')
test('o1(x)\no2(y)', 'two axioms')
test('x = 1\no1(y)\nDefine s = emptyset', 'mixed')

# Semicolon separated
test('x = 1; y = 2; z = 3', 'semicolons')
test('o1(a); o2(b); o3(c)', 'axioms with ;')

# Complex
test('function f(x: Int) : Int = x + 1', 'function')
test('record Point { field x : Int }', 'record Point')
test('record MyRec { field x : Int }', 'record MyRec')
test('module M = struct { x = 1 }', 'module')

# Test P conflict (P is a token for probability)
test('record P { field x : Int }', 'record P (should fail - P is keyword)')

# Full program
full_prog = """o1(omega0)
o21(x)
Define space = emptyset
x = loss(y)
function add(a: Int, b: Int) : Int = a + b"""
test(full_prog, 'FULL PROGRAM')
