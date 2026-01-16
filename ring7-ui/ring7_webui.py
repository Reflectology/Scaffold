#!/usr/bin/env python3
"""
Ring 7: Unified GUI - Tabbed Interface with Webscape Wanderer

CLI Usage:
    python ring7_webui.py              # Launch Tkinter GUI
    python ring7_webui.py --web        # Launch web interface
    python ring7_webui.py --web 8080   # Launch on specific port
"""

import json
import threading
import http.server
import socketserver
import webbrowser
import time
import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Try Tkinter (may not be available in all environments)
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    HAS_TK = True
except ImportError:
    HAS_TK = False

from ring0_kernel import bus, ReflectologyKernel, OmegaState
from ring1_vm import MadladVM, OpCode, Instruction
from ring2_compiler import MadladCompiler
from ring6_extension import WebscapeWanderer, build_sample_omega

# =============================================================================
# WEB-BASED GUI (Always Available)
# =============================================================================

class ReflectologyWebGUI:
    """Web-based GUI with tabbed interface"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.kernel = ReflectologyKernel()
        self.omega = self.kernel.initialize()
        self.compiler = MadladCompiler()
        self.vm = MadladVM()
        self.wanderer = WebscapeWanderer()
        self.log_messages = []
        self._server = None
        self._thread = None
        self._unified = None  # Reference to UnifiedReflectology for state sync
        bus.register_ring("ring7", self)
    
    def log(self, msg: str):
        """Add to log"""
        ts = time.strftime("%H:%M:%S")
        self.log_messages.append(f"[{ts}] {msg}")
        if len(self.log_messages) > 100:
            self.log_messages = self.log_messages[-100:]
    
    def _sync_to_unified(self):
        """Sync state back to unified system if connected"""
        if self._unified and hasattr(self._unified, 'omega'):
            self._unified.omega = self.omega
            self._unified.history.append(("gui_sync", self.omega.checksum()[:16]))
    
    def apply_axiom(self, axiom_id: int) -> Dict:
        """Apply axiom and return result"""
        try:
            self.omega = self.kernel.apply_interface(axiom_id, self.omega)
            self._sync_to_unified()
            self.log(f"Applied axiom {axiom_id}")
            return {"ok": True, "axiom": axiom_id, "checksum": self.omega.checksum()[:16],
                    "cost": round(self.omega.cost, 6), "entropy": round(self.omega.entropy, 6)}
        except Exception as e:
            self.log(f"Error applying axiom {axiom_id}: {e}")
            return {"ok": False, "error": str(e)}
    
    def compile_and_run(self, source: str) -> Dict:
        """Compile and execute MADLAD code"""
        try:
            bytecode = self.compiler.compile(source)
            self.vm.omega = self.omega
            result = self.vm.execute(bytecode)
            self.omega = self.vm.omega
            self._sync_to_unified()
            self.log(f"Executed {len(bytecode)} instructions, result: {result}")
            return {"ok": True, "result": result, "instructions": len(bytecode),
                    "cost": round(self.omega.cost, 6), "bytecode_preview": [str(b) for b in bytecode[:5]]}
        except Exception as e:
            self.log(f"Compile error: {e}")
            return {"ok": False, "error": str(e)}
    
    def get_omega_data(self) -> Dict:
        """Get current omega state"""
        return {
            "id": self.omega.id,
            "cost": round(self.omega.cost, 6),
            "entropy": round(self.omega.entropy, 6),
            "dimension": self.omega.dimension,
            "checksum": self.omega.checksum()[:16],
            "data": {k: str(v)[:50] for k, v in self.omega.data.items() if not str(k).startswith('_')}
        }
    
    def generate_html(self) -> str:
        """Generate the full web interface HTML"""
        omega_json = json.dumps(self.get_omega_data())
        wanderer_graph = json.dumps(self.wanderer.visualizer.omega_to_graph(self.omega.data))
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reflectology Control Center</title>
    <style>
        :root {{
            --primary: #4CAF50; --secondary: #2196F3; --accent: rgb(204, 135, 187);
            --bg: #1a1a2e; --panel: #16213e; --text: #fff; --dim: #888;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); }}
        
        .app {{ display: grid; grid-template-columns: 250px 1fr 300px; grid-template-rows: 60px 1fr; height: 100vh; }}
        
        header {{ grid-column: 1 / -1; background: var(--panel); padding: 0 2em; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #333; }}
        header h1 {{ font-size: 1.3em; color: var(--accent); }}
        header .status {{ font-size: 0.9em; color: var(--dim); }}
        
        .sidebar {{ background: var(--panel); padding: 1em; overflow-y: auto; border-right: 1px solid #333; }}
        .sidebar h3 {{ font-size: 0.9em; color: var(--dim); margin: 1em 0 0.5em; text-transform: uppercase; }}
        .sidebar button {{ width: 100%; padding: 0.7em; margin: 0.2em 0; background: rgba(255,255,255,0.05); color: var(--text); border: 1px solid #444; border-radius: 4px; cursor: pointer; text-align: left; font-size: 0.9em; }}
        .sidebar button:hover {{ background: rgba(255,255,255,0.1); border-color: var(--accent); }}
        .sidebar button.active {{ background: var(--secondary); border-color: var(--secondary); }}
        
        .main {{ display: flex; flex-direction: column; overflow: hidden; }}
        
        .tabs {{ display: flex; background: var(--panel); border-bottom: 1px solid #333; }}
        .tab {{ padding: 1em 1.5em; cursor: pointer; border-bottom: 3px solid transparent; font-size: 0.9em; }}
        .tab:hover {{ background: rgba(255,255,255,0.05); }}
        .tab.active {{ border-bottom-color: var(--accent); color: var(--accent); }}
        
        .content {{ flex: 1; overflow: hidden; }}
        .tab-panel {{ display: none; height: 100%; overflow: auto; padding: 1em; }}
        .tab-panel.active {{ display: block; }}
        
        .panel-right {{ background: var(--panel); padding: 1em; overflow-y: auto; border-left: 1px solid #333; }}
        .panel-right h3 {{ font-size: 0.9em; color: var(--dim); margin-bottom: 0.5em; }}
        
        .state-display {{ background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px; font-family: monospace; font-size: 0.85em; max-height: 200px; overflow-y: auto; margin-bottom: 1em; }}
        .log {{ background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px; font-family: monospace; font-size: 0.8em; height: 300px; overflow-y: auto; }}
        
        .form-group {{ margin: 1em 0; }}
        .form-group label {{ display: block; margin-bottom: 0.3em; font-size: 0.9em; color: var(--dim); }}
        .form-group input, .form-group textarea, .form-group select {{ width: 100%; padding: 0.5em; background: rgba(0,0,0,0.3); border: 1px solid #444; border-radius: 4px; color: var(--text); font-size: 0.9em; }}
        .form-group textarea {{ height: 150px; font-family: monospace; }}
        
        button.primary {{ background: var(--secondary); color: white; border: none; padding: 0.7em 1.5em; border-radius: 4px; cursor: pointer; font-size: 0.9em; }}
        button.primary:hover {{ opacity: 0.8; }}
        
        .metric {{ display: inline-block; margin: 0.5em; padding: 1em; background: rgba(0,0,0,0.3); border-radius: 8px; min-width: 120px; }}
        .metric .label {{ font-size: 0.75em; color: var(--dim); }}
        .metric .value {{ font-size: 1.5em; font-weight: bold; color: var(--primary); }}
        
        #viz-container {{ width: 100%; height: calc(100vh - 200px); background: var(--bg); border-radius: 4px; }}
        #viz-container canvas {{ width: 100%; height: 100%; }}
        
        .axiom-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 0.3em; }}
        .axiom-btn {{ padding: 0.5em; background: rgba(255,255,255,0.05); border: 1px solid #444; border-radius: 4px; cursor: pointer; font-size: 0.8em; text-align: center; }}
        .axiom-btn:hover {{ background: var(--secondary); border-color: var(--secondary); }}
    </style>
</head>
<body>
    <div class="app">
        <header>
            <h1>Ω Reflectology Control Center</h1>
            <div class="status">Ring 7 GUI · <span id="conn-status">Connected</span></div>
        </header>
        
        <aside class="sidebar">
            <h3>Quick Actions</h3>
            <button onclick="applyAllAxioms()">Apply All 40 Axioms</button>
            <button onclick="resetOmega()">Reset Ω State</button>
            <button onclick="refreshViz()">Refresh Visualization</button>
            
            <h3>Rings</h3>
            <button onclick="showTab('kernel')">Ring 0: Kernel</button>
            <button onclick="showTab('vm')">Ring 1: VM</button>
            <button onclick="showTab('compiler')">Ring 2: Compiler</button>
            <button onclick="showTab('parser')">Parser (ZFC)</button>
            <button onclick="showTab('analysis')">Ring 3: Analysis</button>
            <button onclick="showTab('viz')">Ring 6: Visualization</button>
        </aside>
        
        <main class="main">
            <div class="tabs">
                <div class="tab active" onclick="showTab('dashboard')">Dashboard</div>
                <div class="tab" onclick="showTab('kernel')">Kernel</div>
                <div class="tab" onclick="showTab('parser')">Parser</div>
                <div class="tab" onclick="showTab('compiler')">Compiler</div>
                <div class="tab" onclick="showTab('analysis')">Analysis</div>
                <div class="tab" onclick="showTab('viz')">3D Visualization</div>
            </div>
            
            <div class="content">
                <!-- Dashboard Tab -->
                <div id="tab-dashboard" class="tab-panel active">
                    <h2>Ω State Metrics</h2>
                    <div id="metrics"></div>
                    
                    <h2 style="margin-top: 2em;">Quick Axiom Application</h2>
                    <div class="axiom-grid" id="axiom-grid"></div>
                    
                    <h2 style="margin-top: 2em;">Axiom Descriptions</h2>
                    <div id="axiom-desc" style="font-size: 0.9em; color: var(--dim); max-height: 200px; overflow-y: auto;"></div>
                </div>
                
                <!-- Kernel Tab -->
                <div id="tab-kernel" class="tab-panel">
                    <h2>Ring 0: Math Kernel (40 Axioms)</h2>
                    <div class="form-group">
                        <label>Apply Single Axiom (1-40)</label>
                        <input type="number" id="axiom-id" min="1" max="40" value="13">
                    </div>
                    <button class="primary" onclick="applySingleAxiom()">Apply Axiom</button>
                    <button class="primary" onclick="applyAllAxioms()">Apply All 40</button>
                    
                    <h3 style="margin-top: 2em;">Axiom Categories (per Reflectology Theory)</h3>
                    <div style="margin-top: 1em;">
                        <button onclick="applyAxiomRange(1,5)">§1 Configuration Space (1-5)</button>
                        <button onclick="applyAxiomRange(6,10)">§2 Reduce Redundancy (6-10)</button>
                        <button onclick="applyAxiomRange(11,14)">§3 Canonical Forms (11-14)</button>
                        <button onclick="applyAxiomRange(15,24)">§4 Goodness Function (15-24)</button>
                        <button onclick="applyAxiomRange(25,39)">§5 Decision Making (25-39)</button>
                        <button onclick="applyAxiomRange(40,40)">§6 Dual Symmetry (40)</button>
                    </div>
                    
                    <h3 style="margin-top: 2em;">Axiom Reference</h3>
                    <div style="font-size: 0.85em; max-height: 300px; overflow-y: auto; background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px;">
                        <pre id="axiom-ref"></pre>
                    </div>
                </div>
                
                <!-- Parser Tab -->
                <div id="tab-parser" class="tab-panel">
                    <h2>ZFC-Grounded Parser</h2>
                    <p style="color: var(--dim); margin-bottom: 1em;">Parse MADLAD code using set-theoretic foundations (pure Python, zero dependencies)</p>
                    <div class="form-group">
                        <label>Source Code to Parse</label>
                        <textarea id="parse-code">Define x = 42
let f(x) = x * x
o13(loss(theta))
o21(goodness(omega))</textarea>
                    </div>
                    <button class="primary" onclick="parseCode()">Parse</button>
                    <button onclick="tokenizeCode()">Tokenize Only</button>
                    <button onclick="validateCode()">Validate</button>
                    
                    <h3 style="margin-top: 1em;">Parse Result</h3>
                    <div id="parse-result" style="background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px; font-family: monospace; font-size: 0.85em; max-height: 300px; overflow-y: auto;"></div>
                </div>
                
                <!-- Compiler Tab -->
                <div id="tab-compiler" class="tab-panel">
                    <h2>Ring 2: MADLAD Compiler + Ring 1: VM</h2>
                    <p style="color: var(--dim); margin-bottom: 1em;">Compile to bytecode and execute on the MADLAD VM</p>
                    <div class="form-group">
                        <label>MADLAD Source Code</label>
                        <textarea id="source-code">let x = 10
let y = 20
let z = x + y * 2
command(13, z)
command(21, z)
print(z)</textarea>
                    </div>
                    <button class="primary" onclick="compileAndRun()">Compile & Execute</button>
                    <button onclick="compileOnly()">Compile Only (Show Bytecode)</button>
                    
                    <div id="compile-result" style="margin-top: 1em;"></div>
                    
                    <h3 style="margin-top: 2em;">VM State</h3>
                    <div id="vm-state" style="background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px; font-family: monospace; font-size: 0.85em;"></div>
                </div>
                
                <!-- Analysis Tab -->
                <div id="tab-analysis" class="tab-panel">
                    <h2>Ring 3: Mathematical Analysis</h2>
                    <p style="color: var(--dim); margin-bottom: 1em;">Apply bidirectional binomial analysis, fixed-point iteration, and gamma analysis to Ω</p>
                    
                    <h3>Newton-Raphson Root Finding</h3>
                    <div class="form-group">
                        <label>Initial Value (x₀)</label>
                        <input type="number" id="newton-x0" value="2.0" step="0.1">
                    </div>
                    <button class="primary" onclick="runNewton()">Find √2</button>
                    
                    <h3 style="margin-top: 1em;">Fixed-Point Iteration</h3>
                    <div class="form-group">
                        <label>Initial Value</label>
                        <input type="number" id="fixedpt-x0" value="1.0" step="0.1">
                    </div>
                    <button class="primary" onclick="runFixedPoint()">Iterate to Fixed Point</button>
                    
                    <h3 style="margin-top: 1em;">Bidirectional Binomial</h3>
                    <div class="form-group">
                        <label>n (trials)</label>
                        <input type="number" id="binom-n" value="10">
                    </div>
                    <div class="form-group">
                        <label>k (successes)</label>
                        <input type="number" id="binom-k" value="5">
                    </div>
                    <button class="primary" onclick="runBinomial()">Compute C(n,k)</button>
                    
                    <div id="analysis-result" style="margin-top: 1em; background: rgba(0,0,0,0.3); padding: 1em; border-radius: 4px;"></div>
                </div>
                
                <!-- 3D Visualization Tab -->
                <div id="tab-viz" class="tab-panel">
                    <h2>Webscape Wanderer - 3D Ω Visualization</h2>
                    <div style="margin-bottom: 1em;">
                        <button class="primary" onclick="refreshViz()">Refresh</button>
                        <button onclick="toggleSpin()">Toggle Spin</button>
                        <button onclick="resetVizView()">Reset View</button>
                    </div>
                    <div id="viz-container"></div>
                </div>
            </div>
        </main>
        
        <aside class="panel-right">
            <h3>Ω State</h3>
            <div id="state" class="state-display"></div>
            
            <h3>Activity Log</h3>
            <div id="log" class="log"></div>
        </aside>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let omega = {omega_json};
        let graphData = {wanderer_graph};
        let scene, camera, renderer, nodeGroup;
        let spinning = true;
        
        // Tab management
        function showTab(name) {{
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById('tab-' + name).classList.add('active');
            document.querySelector(`.tab[onclick="showTab('${{name}}')"]`)?.classList.add('active');
            
            if (name === 'viz') initViz();
            if (name === 'kernel') loadAxiomRef();
        }}
        
        // API calls
        async function api(endpoint, params = {{}}) {{
            const url = '/api/' + endpoint + '?' + new URLSearchParams(params);
            const resp = await fetch(url);
            return await resp.json();
        }}
        
        async function applySingleAxiom() {{
            const id = document.getElementById('axiom-id').value;
            const result = await api('axiom', {{ id }});
            updateState();
            addLog(result.ok ? `Applied axiom ${{id}} → cost=${{result.cost}}` : `Error: ${{result.error}}`);
        }}
        
        async function applyAllAxioms() {{
            addLog('Applying all 40 axioms...');
            for (let i = 1; i <= 40; i++) {{
                await api('axiom', {{ id: i }});
            }}
            updateState();
            addLog('All 40 axioms applied');
        }}
        
        async function applyAxiomRange(start, end) {{
            for (let i = start; i <= end; i++) {{
                await api('axiom', {{ id: i }});
            }}
            updateState();
            addLog(`Applied axioms ${{start}}-${{end}}`);
        }}
        
        async function resetOmega() {{
            await api('reset');
            updateState();
            addLog('Ω state reset');
        }}
        
        // Parser functions
        async function parseCode() {{
            const source = document.getElementById('parse-code').value;
            const result = await api('parse', {{ source: encodeURIComponent(source) }});
            const el = document.getElementById('parse-result');
            if (result.ok) {{
                el.innerHTML = `<div style="color: #4CAF50;">✓ Parsed successfully</div><pre>${{JSON.stringify(result.ast, null, 2)}}</pre>`;
            }} else {{
                el.innerHTML = `<div style="color: #f44336;">✗ Parse errors:</div><pre>${{result.errors.join('\\n')}}</pre>`;
            }}
            addLog(result.ok ? 'Parsed code successfully' : 'Parse failed');
        }}
        
        async function tokenizeCode() {{
            const source = document.getElementById('parse-code').value;
            const result = await api('tokenize', {{ source: encodeURIComponent(source) }});
            const el = document.getElementById('parse-result');
            el.innerHTML = `<div style="color: #2196F3;">Tokens (${{result.tokens.length}}):</div><pre>${{result.tokens.map(t => `${{t.type.padEnd(20)}} '${{t.text}}'`).join('\\n')}}</pre>`;
            addLog(`Tokenized: ${{result.tokens.length}} tokens`);
        }}
        
        async function validateCode() {{
            const source = document.getElementById('parse-code').value;
            const result = await api('validate', {{ source: encodeURIComponent(source) }});
            const el = document.getElementById('parse-result');
            el.innerHTML = result.valid 
                ? `<div style="color: #4CAF50; font-size: 2em;">✓ Valid MADLAD code</div>`
                : `<div style="color: #f44336; font-size: 2em;">✗ Invalid</div>`;
            addLog(result.valid ? 'Code is valid' : 'Code is invalid');
        }}
        
        // Compiler functions
        async function compileAndRun() {{
            const source = document.getElementById('source-code').value;
            const result = await api('compile', {{ source: encodeURIComponent(source) }});
            const el = document.getElementById('compile-result');
            if (result.ok) {{
                el.innerHTML = `<div style="color: #4CAF50;">✓ Executed ${{result.instructions}} instructions</div>
                    <div>Result: <strong>${{result.result}}</strong></div>
                    <div>Ω cost after: ${{result.cost}}</div>`;
            }} else {{
                el.innerHTML = `<div style="color: #f44336;">✗ Error: ${{result.error}}</div>`;
            }}
            updateState();
            addLog(result.ok ? `Executed ${{result.instructions}} instructions` : `Compile error`);
        }}
        
        async function compileOnly() {{
            const source = document.getElementById('source-code').value;
            const result = await api('bytecode', {{ source: encodeURIComponent(source) }});
            const el = document.getElementById('compile-result');
            if (result.ok) {{
                el.innerHTML = `<div style="color: #2196F3;">Bytecode (${{result.bytecode.length}} instructions):</div>
                    <pre>${{result.bytecode.join('\\n')}}</pre>`;
            }} else {{
                el.innerHTML = `<div style="color: #f44336;">✗ Error: ${{result.error}}</div>`;
            }}
            addLog(`Compiled to ${{result.bytecode?.length || 0}} instructions`);
        }}
        
        // Analysis functions
        async function runNewton() {{
            const x0 = document.getElementById('newton-x0').value;
            const result = await api('analysis/newton', {{ x0 }});
            document.getElementById('analysis-result').innerHTML = result.ok
                ? `<div style="color: #4CAF50;">√2 ≈ ${{result.value}} (converged in ${{result.iterations}} iterations)</div>`
                : `<div style="color: #f44336;">Error: ${{result.error}}</div>`;
            addLog(`Newton-Raphson: ${{result.value}}`);
        }}
        
        async function runFixedPoint() {{
            const x0 = document.getElementById('fixedpt-x0').value;
            const result = await api('analysis/fixedpoint', {{ x0 }});
            document.getElementById('analysis-result').innerHTML = result.ok
                ? `<div style="color: #4CAF50;">Fixed point: ${{result.value}} (${{result.converged ? 'converged' : 'not converged'}} in ${{result.iterations}} iterations)</div>`
                : `<div style="color: #f44336;">Error: ${{result.error}}</div>`;
            addLog(`Fixed-point: ${{result.value}}`);
        }}
        
        async function runBinomial() {{
            const n = document.getElementById('binom-n').value;
            const k = document.getElementById('binom-k').value;
            const result = await api('analysis/binomial', {{ n, k }});
            document.getElementById('analysis-result').innerHTML = result.ok
                ? `<div style="color: #4CAF50;">C(${{n}},${{k}}) = ${{result.value}}</div>`
                : `<div style="color: #f44336;">Error: ${{result.error}}</div>`;
            addLog(`Binomial C(${{n}},${{k}}) = ${{result.value}}`);
        }}
        
        async function updateState() {{
            omega = await api('omega');
            document.getElementById('state').textContent = JSON.stringify(omega, null, 2);
            updateMetrics();
        }}
        
        function updateMetrics() {{
            const metricsHtml = `
                <div class="metric"><div class="label">Cost</div><div class="value">${{omega.cost}}</div></div>
                <div class="metric"><div class="label">Entropy</div><div class="value">${{omega.entropy}}</div></div>
                <div class="metric"><div class="label">Dimension</div><div class="value">${{omega.dimension}}</div></div>
                <div class="metric"><div class="label">Checksum</div><div class="value" style="font-size:0.8em;">${{omega.checksum}}</div></div>
            `;
            document.getElementById('metrics').innerHTML = metricsHtml;
        }}
        
        function addLog(msg) {{
            const log = document.getElementById('log');
            const ts = new Date().toLocaleTimeString();
            log.innerHTML += `[${{ts}}] ${{msg}}<br>`;
            log.scrollTop = log.scrollHeight;
        }}
        
        // Axiom reference
        const AXIOM_NAMES = {{
            1: 'Initial Emptiness: Ω₀ := ∅',
            2: 'First Structure: Ω₁ := {{∅}}',
            3: 'Recursive Encapsulation: Ω₂ := {{Ω₁}}',
            4: 'Fractal Nature: T(Ω) = λT(Ω′)',
            5: 'Hierarchical Structuring: Ω = ∪ᵢ Ωᵢ',
            6: 'Redundancy Reduction: Ω / ∼',
            7: 'Symmetry Reduction: Ω / G',
            8: 'Symmetry Breaking: S(Ω) ≠ Ω ⇒ Ω′ ⊂ Ω',
            9: 'Complexity Reduction: C(Ω) ≥ C(Ω′)',
            10: 'Ω-Bijection: ∃f : Ω′ ↔ Ω″',
            11: 'Complex Symmetry-Flow-Force Associativity',
            12: 'Contextual Monoid',
            13: 'Loss Function: L(ω) := θ(Ωω) − Cω',
            14: 'Canonical Selection: ω* := argmin L(ω)',
            15: 'Reflective Convergence',
            16: 'Normalization (Entropy): H(Ω)',
            17: 'Self-Correction',
            18: 'Nonlinear Logic Formation',
            19: 'Hyperreal Extension: ω + ε',
            20: 'Dimensional Consistency',
            21: 'Rubik\'s Cube Goodness: G := θ(Ω) − C',
            22: 'Information Preservation',
            23: 'Energy Efficiency',
            24: 'Chaotic Creativity Principle',
            25: 'Gradient Flow Dynamics: dω/dt = −∇L(ω)',
            26: 'General Dynamical System',
            27: 'Recursive Structure',
            28: 'Probabilistic Convergence',
            29: 'MAD Activation',
            30: 'Self-Regulation',
            31: 'Base Transform: ω′ = f(ω)',
            32: 'Path Dependence',
            33: 'Feedback Loop',
            34: 'Non-Equilibrium Dynamics',
            35: 'Causality and Correlation',
            36: 'Judgment Paradox',
            37: 'Student Supremacy',
            38: 'Recursive Lineage',
            39: 'Internal Emergence',
            40: 'Reflective Conjugate Duality: ω†'
        }};
        
        function loadAxiomRef() {{
            const el = document.getElementById('axiom-ref');
            el.textContent = Object.entries(AXIOM_NAMES).map(([k,v]) => `Axiom ${{k}}: ${{v}}`).join('\\n');
        }}
        
        // Generate axiom grid
        function initAxiomGrid() {{
            const grid = document.getElementById('axiom-grid');
            for (let i = 1; i <= 40; i++) {{
                grid.innerHTML += `<div class="axiom-btn" onclick="api('axiom', {{id: ${{i}}}}).then(updateState).then(() => addLog('Applied axiom ${{i}}'))" title="${{AXIOM_NAMES[i]}}">${{i}}</div>`;
            }}
        }}
        
        // 3D Visualization
        function initViz() {{
            if (scene) return; // Already initialized
            
            const container = document.getElementById('viz-container');
            const canvas = document.createElement('canvas');
            container.appendChild(canvas);
            
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, alpha: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            
            nodeGroup = new THREE.Group();
            const nodes = new Map();
            
            graphData.nodes.forEach(node => {{
                const geo = new THREE.SphereGeometry(node.size * 0.05, 16, 16);
                const mat = new THREE.MeshBasicMaterial({{ color: node.color }});
                const mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(node.x || 0, node.y || 0, node.z || 0);
                mesh.userData = node;
                nodes.set(node.id, mesh);
                nodeGroup.add(mesh);
            }});
            scene.add(nodeGroup);
            
            const edgeMat = new THREE.LineBasicMaterial({{ color: 0x444466, opacity: 0.5, transparent: true }});
            graphData.edges.forEach(edge => {{
                const src = nodes.get(edge.source);
                const tgt = nodes.get(edge.target);
                if (src && tgt) {{
                    const geo = new THREE.BufferGeometry().setFromPoints([src.position, tgt.position]);
                    scene.add(new THREE.Line(geo, edgeMat));
                }}
            }});
            
            camera.position.z = 8;
            
            let isDragging = false, prevMouse = {{ x: 0, y: 0 }};
            canvas.addEventListener('mousedown', e => {{ isDragging = true; prevMouse = {{ x: e.clientX, y: e.clientY }}; }});
            canvas.addEventListener('mousemove', e => {{
                if (isDragging) {{
                    nodeGroup.rotation.y += (e.clientX - prevMouse.x) * 0.005;
                    nodeGroup.rotation.x += (e.clientY - prevMouse.y) * 0.005;
                    prevMouse = {{ x: e.clientX, y: e.clientY }};
                }}
            }});
            canvas.addEventListener('mouseup', () => isDragging = false);
            canvas.addEventListener('wheel', e => {{
                camera.position.z = Math.max(2, Math.min(20, camera.position.z + e.deltaY * 0.01));
            }});
            
            function animate() {{
                requestAnimationFrame(animate);
                if (spinning && !isDragging) nodeGroup.rotation.y += 0.002;
                renderer.render(scene, camera);
            }}
            animate();
        }}
        
        async function refreshViz() {{
            graphData = await api('graph');
            scene = null;
            document.getElementById('viz-container').innerHTML = '';
            initViz();
        }}
        
        function toggleSpin() {{ spinning = !spinning; }}
        function resetVizView() {{ if (camera) camera.position.z = 8; if (nodeGroup) nodeGroup.rotation.set(0, 0, 0); }}
        
        // Initialize
        initAxiomGrid();
        updateState();
        setInterval(updateState, 5000);
    </script>
</body>
</html>'''
    
    def start(self, open_browser: bool = True) -> Dict:
        """Start the web server"""
        gui = self
        
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(gui.generate_html().encode())
                elif self.path.startswith('/api/'):
                    self.handle_api()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def handle_api(self):
                from urllib.parse import parse_qs, urlparse, unquote
                parsed = urlparse(self.path)
                endpoint = parsed.path[5:]  # Remove '/api/'
                params = parse_qs(parsed.query)
                
                result = {}
                
                if endpoint == 'omega':
                    result = gui.get_omega_data()
                elif endpoint == 'axiom':
                    axiom_id = int(params.get('id', ['1'])[0])
                    result = gui.apply_axiom(axiom_id)
                elif endpoint == 'reset':
                    gui.omega = gui.kernel.initialize()
                    gui._sync_to_unified()
                    gui.log("Reset Ω state")
                    result = {"ok": True}
                elif endpoint == 'compile':
                    source = unquote(params.get('source', [''])[0])
                    result = gui.compile_and_run(source)
                elif endpoint == 'bytecode':
                    # Compile only, return bytecode
                    source = unquote(params.get('source', [''])[0])
                    try:
                        bytecode = gui.compiler.compile(source)
                        result = {"ok": True, "bytecode": [str(b) for b in bytecode]}
                    except Exception as e:
                        result = {"ok": False, "error": str(e)}
                elif endpoint == 'parse':
                    # Parse MADLAD code
                    source = unquote(params.get('source', [''])[0])
                    try:
                        # Try to import ZFC parser
                        import sys
                        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
                        from zfc_parser import parse as zfc_parse
                        parse_result = zfc_parse(source)
                        result = {"ok": parse_result.ok, "ast": parse_result.ast, "errors": parse_result.errors, "tokens": parse_result.tokens}
                        gui.log(f"Parsed: {'ok' if parse_result.ok else 'failed'}")
                    except ImportError:
                        result = {"ok": False, "errors": ["ZFC parser not available"]}
                    except Exception as e:
                        result = {"ok": False, "errors": [str(e)]}
                elif endpoint == 'tokenize':
                    source = unquote(params.get('source', [''])[0])
                    try:
                        import sys
                        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
                        from zfc_parser import tokenize as zfc_tokenize
                        tokens = zfc_tokenize(source)
                        result = {"ok": True, "tokens": tokens}
                    except Exception as e:
                        result = {"ok": False, "tokens": [], "error": str(e)}
                elif endpoint == 'validate':
                    source = unquote(params.get('source', [''])[0])
                    try:
                        import sys
                        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'python'))
                        from zfc_parser import validate as zfc_validate
                        result = {"valid": zfc_validate(source)}
                    except Exception as e:
                        result = {"valid": False, "error": str(e)}
                elif endpoint == 'analysis/newton':
                    # Newton-Raphson for sqrt(2)
                    x0 = float(params.get('x0', ['2.0'])[0])
                    try:
                        from ring3_analysis import NewtonRaphson
                        nr = NewtonRaphson(lambda x: x*x - 2, lambda x: 2*x)
                        res = nr.solve(x0)
                        result = {"ok": True, "value": round(res.value, 10), "iterations": res.iterations, "converged": res.convergence}
                        gui.log(f"Newton-Raphson: √2 ≈ {res.value}")
                    except Exception as e:
                        result = {"ok": False, "error": str(e)}
                elif endpoint == 'analysis/fixedpoint':
                    x0 = float(params.get('x0', ['1.0'])[0])
                    try:
                        from ring3_analysis import FixedPointIterator
                        fpi = FixedPointIterator(lambda x: (x + 2/x) / 2)  # Converges to sqrt(2)
                        res = fpi.iterate(x0)
                        result = {"ok": True, "value": round(res.value, 10), "iterations": res.iterations, "converged": res.convergence}
                        gui.log(f"Fixed-point: {res.value}")
                    except Exception as e:
                        result = {"ok": False, "error": str(e)}
                elif endpoint == 'analysis/binomial':
                    n = int(params.get('n', ['10'])[0])
                    k = int(params.get('k', ['5'])[0])
                    try:
                        from ring3_analysis import BidirectionalBinomial
                        bb = BidirectionalBinomial()
                        val = bb.compute(n, k)
                        result = {"ok": True, "value": val}
                        gui.log(f"C({n},{k}) = {val}")
                    except Exception as e:
                        result = {"ok": False, "error": str(e)}
                elif endpoint == 'graph':
                    result = gui.wanderer.visualizer.omega_to_graph(gui.omega.data)
                elif endpoint == 'log':
                    result = {"messages": gui.log_messages[-20:]}
                else:
                    result = {"error": f"Unknown endpoint: {endpoint}"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            
            def log_message(self, format, *args):
                pass
        
        try:
            self._server = socketserver.TCPServer(("", self.port), Handler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
            
            url = f"http://localhost:{self.port}"
            if open_browser:
                webbrowser.open(url)
            
            return {"ok": True, "url": url}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def stop(self):
        """Stop the server"""
        if self._server:
            self._server.shutdown()
            self._server = None


# =============================================================================
# TKINTER GUI (Optional)
# =============================================================================

if HAS_TK:
    class ReflectologyTkGUI:
        """Native Tkinter GUI"""
        
        def __init__(self):
            self.kernel = ReflectologyKernel()
            self.omega = self.kernel.initialize()
            self.compiler = MadladCompiler()
            self.vm = MadladVM()
            self.wanderer = WebscapeWanderer()
            
            self.root = tk.Tk()
            self.root.title("Reflectology Control Center")
            self.root.geometry("1200x800")
            self.root.configure(bg='#1a1a2e')
            
            self._setup_ui()
        
        def _setup_ui(self):
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TNotebook', background='#1a1a2e')
            style.configure('TNotebook.Tab', background='#16213e', foreground='white', padding=[10, 5])
            style.map('TNotebook.Tab', background=[('selected', '#2196F3')])
            style.configure('TFrame', background='#1a1a2e')
            style.configure('TLabel', background='#1a1a2e', foreground='white')
            style.configure('TButton', background='#2196F3', foreground='white')
            
            # Main notebook (tabs)
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Dashboard tab
            self._create_dashboard_tab()
            
            # Kernel tab
            self._create_kernel_tab()
            
            # Compiler tab
            self._create_compiler_tab()
            
            # Visualization tab
            self._create_viz_tab()
        
        def _create_dashboard_tab(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Dashboard")
            
            ttk.Label(frame, text="Ω State Metrics", font=('Segoe UI', 14, 'bold')).pack(pady=10)
            
            self.metrics_frame = ttk.Frame(frame)
            self.metrics_frame.pack(fill='x', padx=20)
            
            self.cost_var = tk.StringVar(value="0.0")
            self.entropy_var = tk.StringVar(value="0.0")
            self.dim_var = tk.StringVar(value="0")
            
            for label, var in [("Cost", self.cost_var), ("Entropy", self.entropy_var), ("Dimension", self.dim_var)]:
                f = ttk.Frame(self.metrics_frame)
                f.pack(side='left', padx=20, pady=10)
                ttk.Label(f, text=label, font=('Segoe UI', 10)).pack()
                ttk.Label(f, textvariable=var, font=('Segoe UI', 20, 'bold')).pack()
            
            self._update_metrics()
        
        def _create_kernel_tab(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Kernel")
            
            ttk.Label(frame, text="Apply Axiom (1-40)").pack(pady=5)
            self.axiom_entry = ttk.Entry(frame)
            self.axiom_entry.insert(0, "13")
            self.axiom_entry.pack(pady=5)
            
            ttk.Button(frame, text="Apply Axiom", command=self._apply_axiom).pack(pady=5)
            ttk.Button(frame, text="Apply All 40", command=self._apply_all).pack(pady=5)
        
        def _create_compiler_tab(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Compiler")
            
            ttk.Label(frame, text="MADLAD Source Code").pack(pady=5)
            self.code_text = scrolledtext.ScrolledText(frame, height=10, bg='#16213e', fg='white')
            self.code_text.insert('1.0', "let x = 10\nlet y = 20\nlet z = x + y * 2\ncommand(13, z)")
            self.code_text.pack(fill='x', padx=20, pady=5)
            
            ttk.Button(frame, text="Compile & Run", command=self._compile_run).pack(pady=5)
            
            self.result_var = tk.StringVar(value="")
            ttk.Label(frame, textvariable=self.result_var).pack(pady=10)
        
        def _create_viz_tab(self):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="3D Visualization")
            
            ttk.Label(frame, text="Webscape Wanderer", font=('Segoe UI', 14, 'bold')).pack(pady=10)
            ttk.Label(frame, text="Click to open 3D visualization in browser").pack()
            
            ttk.Button(frame, text="Open in Browser", command=self._open_viz).pack(pady=20)
            ttk.Button(frame, text="ASCII View", command=self._ascii_viz).pack(pady=5)
            
            self.ascii_text = scrolledtext.ScrolledText(frame, height=20, bg='#16213e', fg='white', font=('Courier', 10))
            self.ascii_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        def _update_metrics(self):
            self.cost_var.set(f"{self.omega.cost:.4f}")
            self.entropy_var.set(f"{self.omega.entropy:.4f}")
            self.dim_var.set(str(self.omega.dimension))
        
        def _apply_axiom(self):
            try:
                aid = int(self.axiom_entry.get())
                self.omega = self.kernel.apply_interface(aid, self.omega)
                self._update_metrics()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def _apply_all(self):
            for i in range(1, 41):
                self.omega = self.kernel.apply_interface(i, self.omega)
            self._update_metrics()
            messagebox.showinfo("Done", "Applied all 40 axioms")
        
        def _compile_run(self):
            try:
                source = self.code_text.get('1.0', 'end')
                bytecode = self.compiler.compile(source)
                self.vm.omega = self.omega
                result = self.vm.execute(bytecode)
                self.omega = self.vm.omega
                self._update_metrics()
                self.result_var.set(f"✓ Result: {result} ({len(bytecode)} instructions)")
            except Exception as e:
                self.result_var.set(f"✗ Error: {e}")
        
        def _open_viz(self):
            self.wanderer.open_browser(self.omega.data)
        
        def _ascii_viz(self):
            ascii_view = self.wanderer.ascii_view(self.omega.data)
            self.ascii_text.delete('1.0', 'end')
            self.ascii_text.insert('1.0', ascii_view)
        
        def run(self):
            self.root.mainloop()


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Ring 7: Reflectology GUI")
    parser.add_argument('--web', nargs='?', const=8080, type=int, metavar='PORT', 
                        help='Launch web interface (default port 8080)')
    parser.add_argument('--no-browser', action='store_true', help='Start web server without opening browser')
    args = parser.parse_args()
    
    if args.web:
        gui = ReflectologyWebGUI(port=args.web)
        result = gui.start(open_browser=not args.no_browser)
        if result["ok"]:
            print(f"✓ Web GUI running at {result['url']}")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping...")
                gui.stop()
        else:
            print(f"✗ Error: {result['error']}")
    elif HAS_TK:
        gui = ReflectologyTkGUI()
        gui.run()
    else:
        # Fallback to web if no Tkinter
        print("Tkinter not available, launching web interface...")
        gui = ReflectologyWebGUI()
        result = gui.start()
        if result["ok"]:
            print(f"✓ Web GUI running at {result['url']}")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                gui.stop()


if __name__ == "__main__":
    main()
