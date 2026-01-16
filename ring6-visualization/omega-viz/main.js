/**
 * Ring 6: Ω Configuration Space Visualization
 * Uses MDLD ANTLR parser + Three.js for 3D rendering
 */

import antlr4 from 'antlr4';
import mdldLexer from './mdldLexer.js';
import mdldParser from './mdldParser.js';
import mdldVisitor from './mdldVisitor.js';
import * as THREE from 'three';

// =============================================================================
// MDLD AST VISITOR - Extract Ω state from parsed MDLD
// =============================================================================

class OmegaExtractorVisitor extends mdldVisitor {
    constructor() {
        super();
        this.omega = {};
        this.axioms = [];
        this.transforms = [];
        this.errors = [];
    }

    visitDocument(ctx) {
        this.visitChildren(ctx);
        return {
            omega: this.omega,
            axioms: this.axioms,
            transforms: this.transforms,
            errors: this.errors
        };
    }

    visitDefineStmt(ctx) {
        try {
            const id = ctx.IDENTIFIER ? ctx.IDENTIFIER().getText() : 
                       ctx.getChild(1)?.getText() || 'unknown';
            const value = this.extractValue(ctx);
            this.omega[id] = { type: 'definition', value };
        } catch (e) {
            this.errors.push(`defineStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitAxiomStmt(ctx) {
        try {
            const axiomText = ctx.getText();
            const axiomMatch = axiomText.match(/axiom_?(\d+)/i);
            const axiomNum = axiomMatch ? parseInt(axiomMatch[1]) : null;
            
            this.axioms.push({
                number: axiomNum,
                text: axiomText.substring(0, 100)
            });
            
            if (axiomNum) {
                this.omega[`axiom_${axiomNum}`] = { type: 'axiom', value: true, applied: true };
            }
        } catch (e) {
            this.errors.push(`axiomStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitConfigSpaceDecl(ctx) {
        try {
            const text = ctx.getText();
            const omegaMatch = text.match(/Ω[₀₁₂₃₄₅₆₇₈₉]?/);
            if (omegaMatch) {
                this.omega[omegaMatch[0]] = { type: 'omega', value: text };
            }
        } catch (e) {
            this.errors.push(`configSpaceDecl: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitEvaluateStmt(ctx) {
        try {
            const text = ctx.getText();
            // Extract goodness function parameters
            const params = text.match(/(\w+)\s*:\s*([\d.]+)/g);
            if (params) {
                params.forEach(p => {
                    const [key, val] = p.split(':').map(s => s.trim());
                    this.omega[key] = { type: 'float', value: parseFloat(val) };
                });
            }
            this.transforms.push({ type: 'evaluate', text });
        } catch (e) {
            this.errors.push(`evaluateStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitOptimizeStmt(ctx) {
        try {
            this.transforms.push({ type: 'optimize', text: ctx.getText() });
            this.omega['ω*'] = { type: 'optimal', value: 'argmin L(ω)' };
        } catch (e) {
            this.errors.push(`optimizeStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitComputeStmt(ctx) {
        try {
            this.transforms.push({ type: 'compute', text: ctx.getText() });
        } catch (e) {
            this.errors.push(`computeStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitReduceStmt(ctx) {
        try {
            this.transforms.push({ type: 'reduce', text: ctx.getText() });
        } catch (e) {
            this.errors.push(`reduceStmt: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitThetaExpr(ctx) {
        try {
            this.omega['θ'] = { type: 'transform', value: ctx.getText() };
        } catch (e) {
            this.errors.push(`thetaExpr: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitGoodnessExpr(ctx) {
        try {
            this.omega['G'] = { type: 'goodness', value: ctx.getText() };
        } catch (e) {
            this.errors.push(`goodnessExpr: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    visitLossExpr(ctx) {
        try {
            this.omega['L'] = { type: 'loss', value: ctx.getText() };
        } catch (e) {
            this.errors.push(`lossExpr: ${e.message}`);
        }
        return this.visitChildren(ctx);
    }

    extractValue(ctx) {
        const text = ctx.getText();
        // Try to extract assignment value
        const assignMatch = text.match(/:=\s*(.+)/);
        return assignMatch ? assignMatch[1] : text;
    }
}

// =============================================================================
// MDLD PARSER WRAPPER
// =============================================================================

class MDLDParser {
    parse(input) {
        const chars = new antlr4.CharStream(input);
        const lexer = new mdldLexer(chars);
        const tokens = new antlr4.CommonTokenStream(lexer);
        const parser = new mdldParser(tokens);
        
        // Collect errors
        const errors = [];
        parser.removeErrorListeners();
        parser.addErrorListener({
            syntaxError: (rec, sym, line, col, msg) => {
                errors.push({ line, col, msg });
            }
        });
        
        const tree = parser.document();
        const visitor = new OmegaExtractorVisitor();
        const result = visitor.visit(tree);
        
        return {
            ...result,
            parseErrors: errors,
            tree: this.treeToString(tree, parser.ruleNames)
        };
    }

    treeToString(tree, ruleNames, indent = 0) {
        const pad = '  '.repeat(indent);
        if (tree.getChildCount() === 0) {
            return `${pad}${tree.getText()}\n`;
        }
        
        const ruleName = ruleNames[tree.ruleIndex] || 'unknown';
        let result = `${pad}${ruleName}\n`;
        
        for (let i = 0; i < tree.getChildCount(); i++) {
            result += this.treeToString(tree.getChild(i), ruleNames, indent + 1);
        }
        return result;
    }
}

// =============================================================================
// THREE.JS VISUALIZATION
// =============================================================================

class OmegaVisualizer {
    constructor(canvas) {
        this.canvas = canvas;
        this.nodes = new Map();
        this.edges = [];
        this.selectedNode = null;
        
        this.initThree();
        this.initEvents();
        this.animate();
    }

    initThree() {
        const w = this.canvas.parentElement.clientWidth;
        const h = this.canvas.parentElement.clientHeight;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);
        this.camera.position.z = 15;
        
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas, 
            antialias: true, 
            alpha: true 
        });
        this.renderer.setSize(w, h);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.setClearColor(0x1a1a2e, 1);
        
        // Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambient);
        
        const point = new THREE.PointLight(0xffffff, 1);
        point.position.set(10, 10, 10);
        this.scene.add(point);
        
        // Node group for rotation
        this.nodeGroup = new THREE.Group();
        this.scene.add(this.nodeGroup);
        
        // Edge geometry
        this.edgeMaterial = new THREE.LineBasicMaterial({ 
            color: 0x444466, 
            transparent: true, 
            opacity: 0.4 
        });
        
        // Raycaster for interaction
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
    }

    initEvents() {
        let isDragging = false;
        let prevMouse = { x: 0, y: 0 };
        
        this.canvas.addEventListener('mousedown', (e) => {
            isDragging = true;
            prevMouse = { x: e.clientX, y: e.clientY };
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
                this.nodeGroup.rotation.y += (e.clientX - prevMouse.x) * 0.005;
                this.nodeGroup.rotation.x += (e.clientY - prevMouse.y) * 0.005;
                prevMouse = { x: e.clientX, y: e.clientY };
            }
            
            // Update mouse for raycasting
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
            this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        });
        
        this.canvas.addEventListener('mouseup', () => isDragging = false);
        this.canvas.addEventListener('mouseleave', () => isDragging = false);
        
        this.canvas.addEventListener('wheel', (e) => {
            this.camera.position.z = Math.max(5, Math.min(50, 
                this.camera.position.z + e.deltaY * 0.02));
        });
        
        this.canvas.addEventListener('click', () => this.selectHoveredNode());
        
        window.addEventListener('resize', () => this.onResize());
    }

    onResize() {
        const w = this.canvas.parentElement.clientWidth;
        const h = this.canvas.parentElement.clientHeight;
        this.camera.aspect = w / h;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(w, h);
    }

    setOmega(omega) {
        // Clear existing nodes
        while (this.nodeGroup.children.length > 0) {
            this.nodeGroup.remove(this.nodeGroup.children[0]);
        }
        this.nodes.clear();
        this.edges = [];
        
        const keys = Object.keys(omega);
        const n = keys.length;
        
        // Create nodes in a sphere layout
        keys.forEach((key, i) => {
            const data = omega[key];
            const node = this.createNode(key, data, i, n);
            this.nodes.set(key, node);
            this.nodeGroup.add(node.mesh);
        });
        
        // Create edges (circular + by type)
        keys.forEach((key, i) => {
            if (i < n - 1) {
                this.createEdge(keys[i], keys[i + 1]);
            }
        });
        if (n > 2) {
            this.createEdge(keys[n - 1], keys[0]);
        }
    }

    createNode(key, data, index, total) {
        const color = this.getNodeColor(data.type);
        const size = this.getNodeSize(data.type, data.value);
        
        // Spherical layout
        const phi = Math.acos(-1 + (2 * index) / total);
        const theta = Math.sqrt(total * Math.PI) * phi;
        const radius = 5;
        
        const x = radius * Math.cos(theta) * Math.sin(phi);
        const y = radius * Math.sin(theta) * Math.sin(phi);
        const z = radius * Math.cos(phi);
        
        const geometry = new THREE.SphereGeometry(size, 32, 32);
        const material = new THREE.MeshPhongMaterial({ 
            color, 
            emissive: color,
            emissiveIntensity: 0.2,
            shininess: 80
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x, y, z);
        mesh.userData = { key, data };
        
        return { mesh, key, data, color };
    }

    createEdge(from, to) {
        const nodeA = this.nodes.get(from);
        const nodeB = this.nodes.get(to);
        if (!nodeA || !nodeB) return;
        
        const points = [nodeA.mesh.position, nodeB.mesh.position];
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, this.edgeMaterial);
        this.nodeGroup.add(line);
        this.edges.push(line);
    }

    getNodeColor(type) {
        const colors = {
            'axiom': 0x82aaff,
            'omega': 0xcc87bb,
            'definition': 0x9c27b0,
            'float': 0x2196f3,
            'int': 0x4caf50,
            'transform': 0xff9800,
            'goodness': 0x8bc34a,
            'loss': 0xf44336,
            'optimal': 0xe91e63,
            'default': 0x9e9e9e
        };
        return colors[type] || colors.default;
    }

    getNodeSize(type, value) {
        if (type === 'axiom') return 0.4;
        if (type === 'omega') return 0.5;
        if (type === 'optimal') return 0.6;
        if (typeof value === 'number') return Math.min(0.3 + Math.abs(value) * 0.1, 0.7);
        return 0.35;
    }

    selectHoveredNode() {
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const meshes = Array.from(this.nodes.values()).map(n => n.mesh);
        const intersects = this.raycaster.intersectObjects(meshes);
        
        const info = document.getElementById('node-info');
        
        if (intersects.length > 0) {
            const { key, data } = intersects[0].object.userData;
            info.classList.remove('hidden');
            info.querySelector('.node-name').textContent = key;
            info.querySelector('.node-type').textContent = `Type: ${data.type}`;
            info.querySelector('.node-value').textContent = 
                typeof data.value === 'object' ? JSON.stringify(data.value) : String(data.value);
        } else {
            info.classList.add('hidden');
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Gentle auto-rotation
        this.nodeGroup.rotation.y += 0.001;
        
        // Hover effect
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const meshes = Array.from(this.nodes.values()).map(n => n.mesh);
        const intersects = this.raycaster.intersectObjects(meshes);
        
        meshes.forEach(m => {
            m.material.emissiveIntensity = 0.2;
            m.scale.setScalar(1);
        });
        
        if (intersects.length > 0) {
            intersects[0].object.material.emissiveIntensity = 0.5;
            intersects[0].object.scale.setScalar(1.2);
        }
        
        this.renderer.render(this.scene, this.camera);
    }
}

// =============================================================================
// MAIN APPLICATION
// =============================================================================

class App {
    constructor() {
        this.parser = new MDLDParser();
        this.visualizer = new OmegaVisualizer(document.getElementById('viz-canvas'));
        
        document.getElementById('parse-btn').addEventListener('click', () => this.parse());
        
        // Parse initial content
        this.parse();
    }

    parse() {
        const input = document.getElementById('mdld-input').value;
        const result = this.parser.parse(input);
        
        // Display parse tree
        const parseOutput = document.getElementById('parse-output');
        if (result.parseErrors.length > 0) {
            parseOutput.innerHTML = `<span class="token-error">Parse Errors:\n${
                result.parseErrors.map(e => `  Line ${e.line}:${e.col} - ${e.msg}`).join('\n')
            }</span>\n\n${result.tree}`;
        } else {
            parseOutput.textContent = result.tree;
        }
        
        // Display Ω state
        const omegaState = document.getElementById('omega-state');
        omegaState.textContent = JSON.stringify(result.omega, null, 2);
        
        // Update visualization
        this.visualizer.setOmega(result.omega);
        
        console.log('MDLD Parse Result:', result);
    }
}

// Initialize
window.addEventListener('DOMContentLoaded', () => new App());
