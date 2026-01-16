#!/usr/bin/env python3
"""
Ring 6: Visualization & Analysis - MDLD Omega Visualizer

Uses ANTLR JavaScript parser + Three.js for 3D Ω configuration space visualization.

CLI Usage:
    python ring6_extension.py                # Terminal ASCII view
    python ring6_extension.py --dev          # Start Vite dev server
    python ring6_extension.py --server PORT  # Start data API server
    python ring6_extension.py --json         # Output Ω as graph JSON
"""

import sys
import os
import json
import math
import http.server
import socketserver
import threading
import webbrowser
import subprocess
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path

# Path to omega-viz project (MDLD + Three.js)
OMEGA_VIZ_PATH = Path(__file__).parent / "omega-viz"

try:
    from ring0_kernel import bus, ReflectologyKernel, OmegaState
except ImportError:
    # Fallback if ring0 not available
    class OmegaState:
        def __init__(self, data=None):
            self.data = data or {}
            self.dimension = 0
            self.cost = 0.0
    
    class ReflectologyKernel:
        def initialize(self):
            return OmegaState({'level': 0})
        def apply_interface(self, axiom, omega):
            omega.data[f'axiom_{axiom}'] = True
            return omega
    
    class Bus:
        def register_ring(self, name, obj): pass
    bus = Bus()


# =============================================================================
# Ω TO WEBSCAPE-WANDERER DATA CONVERTER
# =============================================================================

class OmegaToGraphConverter:
    """Convert Ω states to webscape-wanderer graph format"""
    
    def __init__(self):
        self.color_map = {
            'int': [0.3, 0.69, 0.31, 1.0],      # Green
            'float': [0.13, 0.59, 0.95, 1.0],    # Blue
            'bool_true': [0.55, 0.76, 0.29, 1.0],
            'bool_false': [0.96, 0.26, 0.21, 1.0],
            'str': [1.0, 0.6, 0.0, 1.0],         # Orange
            'dict': [0.61, 0.15, 0.69, 1.0],     # Purple
            'list': [0.0, 0.74, 0.83, 1.0],      # Cyan
            'complex': [0.91, 0.12, 0.39, 1.0],  # Pink
            'omega': [0.8, 0.53, 0.73, 1.0],     # Accent
            'default': [0.62, 0.62, 0.62, 1.0],
        }
    
    def omega_to_wanderer_format(self, omega: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Ω state to webscape-wanderer expected format:
        {
            nodes: [...],           # Array of node IDs (strings)
            linkIndexPairs: [...],  # Flat array of [src_idx, tgt_idx, src_idx, tgt_idx, ...]
            nodeData: {...}         # Map of node ID -> metadata
        }
        """
        keys = [k for k in omega.keys() if not str(k).startswith('_')]
        
        nodes = []
        node_data = {}
        link_index_pairs = []
        
        for i, key in enumerate(keys):
            node_id = str(key)
            value = omega[key]
            
            nodes.append(node_id)
            node_data[node_id] = self._create_node_data(key, value, i, len(keys))
        
        # Create edges - connect related nodes
        for i, key in enumerate(keys):
            value = omega[key]
            
            # Connect to next node in sequence (circular)
            if len(keys) > 1:
                next_idx = (i + 1) % len(keys)
                link_index_pairs.extend([i, next_idx])
            
            # If value references another key, connect them
            if isinstance(value, str) and value in keys:
                target_idx = keys.index(value)
                if target_idx != i:
                    link_index_pairs.extend([i, target_idx])
        
        return {
            'nodes': nodes,
            'linkIndexPairs': link_index_pairs,
            'nodeData': node_data,
            'meta': {
                'source': 'reflectology',
                'dimension': len(keys),
                'type': 'omega_configuration_space'
            }
        }
    
    def _create_node_data(self, key: str, value: Any, idx: int, total: int) -> Dict:
        """Create node metadata in webscape-wanderer format"""
        
        # Determine color based on type
        if isinstance(value, bool):
            color = self.color_map['bool_true'] if value else self.color_map['bool_false']
            size = 8 if value else 4
        elif isinstance(value, int):
            color = self.color_map['int']
            size = min(max(abs(value) * 0.3, 4), 20)
        elif isinstance(value, float):
            color = self.color_map['float']
            size = min(max(abs(value) * 2, 4), 20)
        elif isinstance(value, complex):
            color = self.color_map['complex']
            size = min(max(abs(value) * 1.5, 6), 20)
        elif isinstance(value, dict):
            color = self.color_map['dict']
            size = 10 + len(value)
        elif isinstance(value, (list, tuple)):
            color = self.color_map['list']
            size = 6 + len(value)
        elif isinstance(value, str):
            color = self.color_map['str']
            size = 6 + min(len(value) * 0.3, 10)
        elif isinstance(value, OmegaState):
            color = self.color_map['omega']
            size = 15
        else:
            color = self.color_map['default']
            size = 6
        
        return {
            'id': str(key),
            'name': str(key),
            'value': str(value)[:200],
            'type': type(value).__name__,
            'color': color,
            'size': size,
            'emphasis': 1.0 if idx == 0 else 0.5,
        }
    
    def to_valuenetwork_format(self, omega: Dict[str, Any]) -> Dict[str, Dict]:
        """Convert to valuenetwork.json style format for full compatibility"""
        keys = list(omega.keys())
        result = {}
        
        for i, key in enumerate(keys):
            value = omega[key]
            node_id = str(key)
            
            # Build dependencies (references to other keys)
            deps = []
            if isinstance(value, str) and value in keys:
                deps.append(value)
            elif isinstance(value, dict):
                for v in value.values():
                    if isinstance(v, str) and v in keys:
                        deps.append(v)
            
            result[node_id] = {
                'name': str(key),
                'description': str(value)[:100],
                'dependencies': deps,
                'dependents': [],  # Will be computed
                'type': type(value).__name__,
            }
        
        # Compute dependents (reverse of dependencies)
        for node_id, data in result.items():
            for dep in data['dependencies']:
                if dep in result:
                    result[dep]['dependents'].append(node_id)
        
        return result


# =============================================================================
# WEBSCAPE WANDERER SERVER
# =============================================================================

class WebscapeWanderer:
    """Integration layer for webscape-wanderer visualization"""
    
    _instance = None
    _server = None
    _thread = None
    _vite_process = None
    
    def __init__(self):
        self.converter = OmegaToGraphConverter()
        self.current_omega = {}
        self.kernel = ReflectologyKernel()
        bus.register_ring("ring6", self)
    
    def set_omega(self, omega):
        """Update the current Ω state"""
        if isinstance(omega, OmegaState):
            self.current_omega = dict(omega.data)
        else:
            self.current_omega = dict(omega)
    
    def get_graph_data(self) -> Dict[str, Any]:
        """Get current graph data in webscape-wanderer format"""
        return self.converter.omega_to_wanderer_format(self.current_omega)
    
    def get_valuenetwork_data(self) -> Dict[str, Dict]:
        """Get data in valuenetwork.json format"""
        return self.converter.to_valuenetwork_format(self.current_omega)
    
    def write_data_files(self, omega=None):
        """Write Ω data to omega-viz public directory"""
        if omega:
            self.set_omega(omega)
        
        # Ensure public dir exists
        public_dir = OMEGA_VIZ_PATH / "public"
        public_dir.mkdir(exist_ok=True)
        
        # Write graph format
        graph_data = self.get_graph_data()
        with open(public_dir / "omega_data.json", 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        return {
            'graph': str(public_dir / "omega_data.json")
        }
    
    def start_dev_server(self, omega=None):
        """Start Vite dev server for omega-viz"""
        if omega:
            self.write_data_files(omega)
        
        # Check if npm/pnpm is available
        npm_cmd = 'pnpm' if subprocess.run(['which', 'pnpm'], capture_output=True).returncode == 0 else 'npm'
        
        # Install deps if needed
        if not (OMEGA_VIZ_PATH / "node_modules").exists():
            print(f"Installing dependencies with {npm_cmd}...")
            subprocess.run([npm_cmd, 'install'], cwd=OMEGA_VIZ_PATH)
        
        # Start Vite dev server
        print(f"Starting Vite dev server...")
        WebscapeWanderer._vite_process = subprocess.Popen(
            [npm_cmd, 'run', 'dev'],
            cwd=OMEGA_VIZ_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        # Wait for server to start (port 8888 per package.json)
        import time
        time.sleep(3)
        
        url = "http://localhost:8888"
        webbrowser.open(url)
        
        return {"ok": True, "url": url, "pid": WebscapeWanderer._vite_process.pid}
    
    def start_api_server(self, omega, port: int = 5173) -> Dict:
        """Start HTTP API server that serves Ω data for webscape-wanderer"""
        self.set_omega(omega)
        
        graph_data = self.get_graph_data()
        vn_data = self.get_valuenetwork_data()
        
        outer_self = self
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                # CORS headers
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                
                if self.path == '/omega' or self.path == '/omega/graph':
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(graph_data).encode())
                
                elif self.path == '/omega/valuenetwork':
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(vn_data).encode())
                
                elif self.path == '/omega/raw':
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(outer_self.current_omega, default=str).encode())
                
                else:
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'endpoints': ['/omega', '/omega/graph', '/omega/valuenetwork', '/omega/raw'],
                        'nodes': len(graph_data['nodes']),
                        'edges': len(graph_data['linkIndexPairs']) // 2
                    }).encode())
            
            def log_message(self, format, *args):
                pass
        
        try:
            if WebscapeWanderer._server:
                WebscapeWanderer._server.shutdown()
            
            WebscapeWanderer._server = socketserver.TCPServer(("", port), Handler)
            WebscapeWanderer._thread = threading.Thread(
                target=WebscapeWanderer._server.serve_forever, 
                daemon=True
            )
            WebscapeWanderer._thread.start()
            
            return {"ok": True, "url": f"http://localhost:{port}", "port": port}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def ascii_view(self, omega=None) -> str:
        """Generate ASCII terminal visualization"""
        if omega:
            self.set_omega(omega)
        
        lines = []
        lines.append("╔══════════════════════════════════════════════════════════════╗")
        lines.append("║           Ω CONFIGURATION SPACE - TERMINAL VIEW              ║")
        lines.append("╠══════════════════════════════════════════════════════════════╣")
        
        graph = self.get_graph_data()
        
        for node_id in graph['nodes']:
            node = graph['nodeData'].get(node_id, {})
            size = int(node.get('size', 6))
            bar_len = min(size, 25)
            bar = "█" * bar_len
            
            val = self.current_omega.get(node_id, '')
            if isinstance(val, bool):
                indicator = "◉" if val else "○"
            elif isinstance(val, (int, float)):
                indicator = "▣"
            elif isinstance(val, dict):
                indicator = "◈"
            elif isinstance(val, (list, tuple)):
                indicator = "◇"
            else:
                indicator = "◦"
            
            label = str(node_id)[:15].ljust(15)
            value_str = str(node.get('value', ''))[:25].ljust(25)
            lines.append(f"║ {indicator} {label} │ {bar.ljust(25)} │ {value_str} ║")
        
        lines.append("╠══════════════════════════════════════════════════════════════╣")
        n_edges = len(graph['linkIndexPairs']) // 2
        lines.append(f"║ Nodes: {len(graph['nodes']):3d}  │  Edges: {n_edges:3d}                                   ║")
        lines.append("╚══════════════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)
    
    @staticmethod
    def stop():
        """Stop all servers"""
        if WebscapeWanderer._server:
            WebscapeWanderer._server.shutdown()
            WebscapeWanderer._server = None
        if WebscapeWanderer._vite_process:
            WebscapeWanderer._vite_process.terminate()
            WebscapeWanderer._vite_process = None
        return {"ok": True}


# =============================================================================
# CLI INTERFACE
# =============================================================================

def build_sample_omega() -> Dict[str, Any]:
    """Build a sample Ω state for demonstration"""
    kernel = ReflectologyKernel()
    omega = kernel.initialize()
    
    for i in [2, 5, 13, 16, 21, 25, 40]:
        omega = kernel.apply_interface(i, omega)
    
    omega.data.update({
        'loss': 0.234,
        'entropy': 1.386,
        'gradient': -0.05,
        'goodness': 0.89,
        'theta': 2.718,
        'convergence': 0.95,
        'dimension': omega.dimension,
        'cost': omega.cost
    })
    
    return omega.data


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ring 6: Ω Visualization via Webscape Wanderer"
    )
    parser.add_argument('--dev', action='store_true', 
                        help='Start Vite dev server for webscape-wanderer')
    parser.add_argument('--server', type=int, metavar='PORT', 
                        help='Start API server on PORT')
    parser.add_argument('--json', action='store_true', 
                        help='Output graph data as JSON')
    parser.add_argument('--valuenetwork', action='store_true',
                        help='Output in valuenetwork.json format')
    parser.add_argument('--write', action='store_true',
                        help='Write data files to webscape-wanderer/data/')
    args = parser.parse_args()
    
    wanderer = WebscapeWanderer()
    omega = build_sample_omega()
    
    if args.json:
        wanderer.set_omega(omega)
        print(json.dumps(wanderer.get_graph_data(), indent=2))
    
    elif args.valuenetwork:
        wanderer.set_omega(omega)
        print(json.dumps(wanderer.get_valuenetwork_data(), indent=2))
    
    elif args.write:
        paths = wanderer.write_data_files(omega)
        print(f"✓ Wrote {paths['valuenetwork']}")
        print(f"✓ Wrote {paths['graph']}")
    
    elif args.dev:
        result = wanderer.start_dev_server(omega)
        if result["ok"]:
            print(f"✓ Dev server at {result['url']}")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping...")
                WebscapeWanderer.stop()
        else:
            print(f"✗ Error: {result.get('error', 'unknown')}")
    
    elif args.server:
        result = wanderer.start_api_server(omega, args.server)
        if result["ok"]:
            print(f"✓ API server at {result['url']}")
            print("  GET /omega          - Graph data")
            print("  GET /omega/valuenetwork - ValueNetwork format")
            print("  GET /omega/raw      - Raw Ω state")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping...")
                WebscapeWanderer.stop()
        else:
            print(f"✗ Error: {result['error']}")
    
    else:
        # Default: ASCII view
        print(wanderer.ascii_view(omega))
        print(f"\nOmega Viz path: {OMEGA_VIZ_PATH}")
        print("Use --dev to start visualization, --server PORT for API")


if __name__ == "__main__":
    main()
