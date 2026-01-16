#!/usr/bin/env python3
"""
MADLAD End-to-End Integration
Wires all 9 rings together with the ANTLR parser and interpreter

Usage:
    python3 madlad_e2e.py <file.mdld>             # Execute MDLD file
    python3 madlad_e2e.py --repl                  # Interactive REPL
    python3 madlad_e2e.py --test                  # Run test suite
"""

import sys
import os
from pathlib import Path

# Add ring directories to path
sys.path.insert(0, str(Path(__file__).parent / "ring0-math-kernel"))
sys.path.insert(0, str(Path(__file__).parent / "ring1-virtual-machine"))
sys.path.insert(0, str(Path(__file__).parent / "ring2-compiler-parser"))
sys.path.insert(0, str(Path(__file__).parent / "ring3-analysis-logic"))
sys.path.insert(0, str(Path(__file__).parent / "ring4-networking"))
sys.path.insert(0, str(Path(__file__).parent / "ring5-storage"))
sys.path.insert(0, str(Path(__file__).parent / "ring6-visualization"))
sys.path.insert(0, str(Path(__file__).parent / "ring7-ui"))
sys.path.insert(0, str(Path(__file__).parent / "ring8-deployment"))

from antlr4 import InputStream, CommonTokenStream
from mdldLexer import mdldLexer
from mdldParser import mdldParser
from mdld_interpreter import MdldInterpreter

# Import all rings with correct class names
from ring0_kernel import ReflectologyKernel
from ring1_vm import MadladVM
from ring2_compiler import MadladCompiler
from ring3_analysis import AnalyticalEngine
from ring4_network import ConsensusNetworkNode
from ring5_database import GenericDB
from ring6_extension import WebscapeWanderer
from ring7_webui import ReflectologyWebGUI
from ring8_deployment import AzureDeployment


class MadladRuntime:
    """Complete MADLAD runtime with all 9 rings integrated"""
    
    def __init__(self):
        print("🔄 Initializing MADLAD Runtime...")
        
        # Ring 0: Mathematical kernel
        self.kernel = ReflectologyKernel()
        print("✅ Ring 0: Reflectology Kernel loaded (40 axioms)")
        
        # Ring 1: Virtual machine
        self.vm = MadladVM()
        print("✅ Ring 1: Virtual Machine loaded")
        
        # Ring 2: Compiler
        self.compiler = MadladCompiler()
        print("✅ Ring 2: Compiler loaded")
        
        # Ring 3: Analysis
        self.analyzer = AnalyticalEngine()
        print("✅ Ring 3: Analytical Engine loaded")
        
        # Ring 4: Networking
        self.network = ConsensusNetworkNode("localhost", 5000)
        print("✅ Ring 4: Consensus Network Node loaded")
        
        # Ring 5: Database
        self.db = GenericDB("madlad_db")
        print("✅ Ring 5: Generic Database loaded")
        
        # Ring 6: Visualization
        self.viz = WebscapeWanderer()
        print("✅ Ring 6: Webscape Wanderer loaded")
        
        # Ring 7: Web UI
        self.webui = ReflectologyWebGUI()
        print("✅ Ring 7: Reflectology Web GUI loaded")
        
        # Ring 8: Deployment
        self.deploy = AzureDeployment()
        print("✅ Ring 8: Azure Deployment loaded")
        
        # Wire rings together
        self._wire_rings()
        print("✅ All rings wired end-to-end\n")
    
    def _wire_rings(self):
        """Connect rings to each other"""
        # Ring 1 -> Ring 0: VM calls kernel
        self.vm.kernel = self.kernel
        
        # Ring 2 -> Ring 1: Compiler emits bytecode for VM
        self.compiler.vm = self.vm
        
        # Ring 3 -> Ring 0: Analyzer uses kernel
        self.analyzer.kernel = self.kernel
        
        # Ring 4 -> Ring 0: Network transforms via kernel
        self.network.kernel = self.kernel
        
        # Ring 5 -> Ring 0: DB persists via kernel transformations
        self.db.kernel = self.kernel
        
        # Ring 6 -> Ring 0: Viz renders configuration spaces
        self.viz.kernel = self.kernel
        
        # Ring 7 -> Ring 6: WebUI uses viz engine
        self.webui.viz = self.viz
        
        # Ring 8 -> Ring 4: Deployment uses network
        self.deploy.network = self.network
    
    def execute_file(self, filepath: str, proof=False):
        """Execute a .mdld file through the full stack"""
        print(f"📄 Loading: {filepath}")
        
        with open(filepath, 'r') as f:
            source = f.read()
        
        print(f"📝 Source ({len(source)} chars):")
        print("-" * 60)
        print(source[:200] + ("..." if len(source) > 200 else ""))
        print("-" * 60)
        
        # Parse with ANTLR
        print("🔍 Parsing with ANTLR...")
        input_stream = InputStream(source)
        lexer = mdldLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = mdldParser(token_stream)
        tree = parser.document()  # Entry point for MADLAD grammar
        
        # Execute with interpreter
        print("⚙️  Executing through ring stack...")
        interpreter = MdldInterpreter(proof_mode=proof)
        result = interpreter.visit(tree)
        
        print(f"\n✅ Execution complete")
        return result
    
    def repl(self):
        """Interactive REPL"""
        print("🎮 MADLAD REPL (type 'exit' to quit)")
        print("   All 9 rings loaded and ready")
        print()
        
        interpreter = MdldInterpreter(proof_mode=False)
        
        while True:
            try:
                line = input("madlad> ")
                if line.strip().lower() in ['exit', 'quit']:
                    break
                
                if not line.strip():
                    continue
                
                # Parse and execute
                input_stream = InputStream(line)
                lexer = mdldLexer(input_stream)
                token_stream = CommonTokenStream(lexer)
                parser = mdldParser(token_stream)
                tree = parser.document()  # Correct entry point
                
                result = interpreter.visit(tree)
                if result is not None:
                    print(f"→ {result}")
                    
            except EOFError:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n👋 Goodbye!")


def test_suite(runtime):
    """Run test suite"""
    print("🧪 Running MADLAD Test Suite\n")
    
    test_dir = Path(__file__).parent / "MADLAD" / "rings"
    test_files = [
        "simple_math.mdld",
        "hello.mdld",
        "paper.mdld",
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        filepath = test_dir / test_file
        if not filepath.exists():
            print(f"⏭️  Skipping {test_file} (not found)")
            continue
        
        try:
            print(f"\n{'='*60}")
            print(f"Test: {test_file}")
            print('='*60)
            runtime.execute_file(str(filepath))
            passed += 1
            print(f"✅ PASS: {test_file}")
        except Exception as e:
            failed += 1
            print(f"❌ FAIL: {test_file}")
            print(f"   Error: {e}")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print('='*60)
    return failed == 0


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 madlad_e2e.py <file.mdld>      # Execute file")
        print("  python3 madlad_e2e.py --repl           # Interactive REPL")
        print("  python3 madlad_e2e.py --test           # Run tests")
        sys.exit(1)
    
    # Handle help flag before initialization
    cmd = sys.argv[1]
    if cmd in ["--help", "-h", "help"]:
        print("MADLAD End-to-End Integration")
        print("=" * 60)
        print("\nUsage:")
        print("  python3 madlad_e2e.py <file.mdld>      # Execute MDLD file")
        print("  python3 madlad_e2e.py --repl           # Interactive REPL")
        print("  python3 madlad_e2e.py --test           # Run test suite")
        print("  python3 madlad_e2e.py --proof <file>   # Generate Metamath proof")
        print("\nExamples:")
        print("  python3 madlad_e2e.py test_e2e.mdld")
        print("  python3 madlad_e2e.py MADLAD/rings/paper.mdld")
        print("\nRings: 0=Kernel, 1=VM, 2=Compiler, 3=Analysis, 4=Network,")
        print("       5=Database, 6=Visualization, 7=WebUI, 8=Deployment")
        sys.exit(0)
    
    # Initialize runtime
    runtime = MadladRuntime()
    
    # Handle commands
    if cmd == "--repl":
        runtime.repl()
    elif cmd == "--test":
        success = test_suite(runtime)
        sys.exit(0 if success else 1)
    elif cmd == "--proof" and len(sys.argv) > 2:
        # Execute with proof generation
        runtime.execute_file(sys.argv[2], proof=True)
    else:
        # Execute file
        runtime.execute_file(cmd)


if __name__ == "__main__":
    main()
