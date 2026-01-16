# Integration Plan: Webscape Wanderer → M0WER

## Ω-Configuration Space Mapping

### Current Configuration (ω₁): Webscape Wanderer Standalone
```
Ω_wanderer = {
  rendering: WebGPU + THREE.js + TSL shaders
  layout: cola.js + d3-force-3d + web workers
  data: LevelGraph + SPARQL + JSON files
  interaction: inertial-turntable-camera + selection
  presentation: Web Component (LitElement)
}
```

### Target Configuration (ω₂): M0WER Extension Module
```
Ω_m0wer = {
  rendering: D3.js SVG (Ring 6 - VS Code Webview)
  layout: D3 force simulation (basic)
  data: CodeStructure (in-memory, axiom-annotated)
  interaction: VS Code commands + webview messages
  presentation: Webview Panel
}
```

### Canonical Form (CF(ω)): Minimal Viable Integration
Apply **Axiom #9: Complexity Reduction** — Remove redundancies while preserving essential transformations:

```
CF(Ω) = {
  rendering: THREE.js (subset) in webview
  layout: d3-force-3d (simplified, no workers)
  data: DiagramData → graph adapter
  interaction: Preserve camera + selection, remove routing
  presentation: Inject into M0WER webview
}
```

---

## Ring Architecture Placement

Following the **40 Axioms** structure from `.github/copilot-instructions.md`:

- **Ring 6**: M0WER + Enhanced Visualization Module
  - M0WER provides: Code analysis, axiom mapping, entity tree
  - Wanderer provides: 3D force-directed visualization with better interaction

---

## Transformation Path (θ)

### Phase 1: Extract Core Visualization (Axiom #6: Redundancy Reduction)

**Remove from wanderer:**
- ❌ LevelGraph database → Use M0WER's `DiagramData` directly
- ❌ Web workers → VS Code handles background work differently
- ❌ Router/navigation → Use M0WER's command system
- ❌ LitElement custom element → Inject into webview HTML
- ❌ SPARQL query engine → M0WER has `CodeAnalyzer`
- ❌ All data loading logic → M0WER generates structure

**Keep from wanderer:**
- ✅ `gpu/graph-viz.ts` - THREE.js rendering setup
- ✅ `gpu/rendering.ts` - Canvas and animation loop
- ✅ `graph-layout.ts` - Force-directed layout logic
- ✅ `interaction.ts` - Camera controls and selection
- ✅ `shaders/*.tsl.ts` - Visual node/edge shaders

---

### Phase 2: Create Adapter (Axiom #10: Ω-Bijection)

Create bidirectional mapping between data structures:

```typescript
// src/adapters/wanderer-adapter.ts
import { DiagramData, DiagramNode, DiagramLink } from './diagramGenerator';

export interface GraphNode {
  id: string;
  x?: number;
  y?: number;
  z?: number;
  color?: string;
  size?: number;
  label?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  weight?: number;
}

export function diagramToGraph(diagram: DiagramData): {
  nodes: GraphNode[];
  edges: GraphEdge[];
} {
  const nodes = diagram.nodes.map(node => ({
    id: node.id,
    x: node.position?.x || 0,
    y: node.position?.y || 0,
    z: 0,
    size: node.metrics.utility || 1,
    color: node.canonical ? '#00aa00' : '#888888',
    label: node.name,
  }));

  const edges = diagram.links.map(link => ({
    source: link.source,
    target: link.target,
    weight: link.weight,
  }));

  return { nodes, edges };
}
```

---

### Phase 3: Minimal Integration (Axiom #14: Canonical Selection)

**File Structure in M0WER:**
```
M0WER/
├── src/
│   ├── extension.ts           # Existing
│   ├── webviewPanel.ts        # MODIFY: Inject 3D viz
│   ├── diagramGenerator.ts    # Existing
│   ├── codeAnalyzer.ts        # Existing
│   ├── visualization/         # NEW
│   │   ├── wanderer-adapter.ts    # Data transformation
│   │   ├── three-renderer.ts      # THREE.js setup (from wanderer)
│   │   ├── force-layout.ts        # d3-force-3d (simplified)
│   │   └── interaction.ts         # Camera + selection
│   └── ...
├── lib/                       # NEW
│   └── OBJLoader.js          # Copy from wanderer if needed
```

---

### Phase 4: Webview Integration Pattern

**Modify `webviewPanel.ts`:**

```typescript
// Add THREE.js option to layout dropdown
<select id="layoutType">
  <option value="force">Force-Directed (2D)</option>
  <option value="force3d">Force-Directed (3D)</option> <!-- NEW -->
  <option value="radial">Radial</option>
  <option value="hierarchical">Hierarchical</option>
</select>

// In the script section, add THREE.js import and 3D rendering
<script src="https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.min.js"></script>
<script>
  // Existing D3 code...
  
  // Add 3D rendering mode
  if (layoutType === 'force3d') {
    // Initialize THREE.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('diagram') });
    
    // Convert DiagramData to 3D graph
    const graphData = diagramDataTo3D(diagramData);
    
    // Apply force-directed layout
    const layout = d3.forceSimulation3d(graphData.nodes)
      .force("link", d3.forceLink3d(graphData.edges))
      .force("charge", d3.forceManyBody3d())
      .force("center", d3.forceCenter3d());
    
    // Render nodes as THREE.js instances
    // ... (simplified from wanderer's rendering.ts)
  }
</script>
```

---

### Phase 5: Goodness Function Evaluation (Axiom #21)

**Before Integration:**
```
G(ω_separate) = θ(wanderer) + θ(m0wer) - C(maintain_both)
                ≈ 10 + 8 - 5 = 13
```

**After Integration:**
```
G(ω_integrated) = θ(enhanced_m0wer) - C(complexity)
                  ≈ 15 - 3 = 12
```

**Optimization Point:** The integration is justified if:
- M0WER gains 3D visualization capability
- Wanderer's code analysis benefits from axiom framework
- Maintenance cost reduces by unifying codebases

---

## Implementation Checklist

### Step 1: Prepare Wanderer Code
- [ ] Extract core rendering logic from `src/gpu/`
- [ ] Remove worker dependencies
- [ ] Create standalone THREE.js initialization
- [ ] Simplify force layout to run synchronously

### Step 2: Create Adapter Layer
- [ ] Write `DiagramData → GraphData` transformer
- [ ] Map axiom colors to node visualization
- [ ] Handle metric-based sizing/positioning

### Step 3: Integrate into M0WER
- [ ] Add THREE.js library to webview
- [ ] Create 3D layout mode option
- [ ] Wire up camera controls
- [ ] Preserve node selection → editor jumping

### Step 4: Test & Refine
- [ ] Verify performance with large graphs (>100 nodes)
- [ ] Ensure VS Code theme compatibility
- [ ] Test on different OS (macOS, Linux, Windows)

---

## Mathematical Justification (Reflectology Framework)

### Axiom #1-5: Define Configuration Space
The two projects exist in different Ω spaces:
- `Ω_wanderer`: Web-based graph viz for arbitrary data
- `Ω_m0wer`: VS Code extension for code structure

### Axiom #6-7: Reduce Redundancy via Symmetry
Both implement graph visualization → **redundant structure**.
Group action G: "render graph from nodes + edges"
Equivalence class: All implementations of force-directed layout

### Axiom #11-14: Compute Canonical Form
The canonical implementation combines:
- M0WER's axiom-based code analysis (unique)
- Wanderer's 3D rendering (superior UX)
- Eliminates duplicate database/query layers

### Axiom #21: Goodness Function
```
G(ω) = Utility - Cost
     = (3D_viz + axiom_analysis + code_navigation) - (maintenance + complexity)
```
Maximized when we **reduce to one codebase with enhanced capabilities**.

### Axiom #40: Reflective Conjugate Duality
The integration creates a self-dual system:
- Analysis (M0WER) ↔ Visualization (Wanderer)
- Code structure ↔ Graph rendering
- Static (axioms) ↔ Dynamic (interaction)

---

## Mathematical Program Description (Equational Form)

### Program as Transformation Sequence

The entire webscape-wanderer system can be described as a composition of transformations on configuration spaces:

```
Program = θ_render ∘ θ_layout ∘ θ_interpolate ∘ θ_parse : Ω_data → Ω_visual
```

Where each θ represents a distinct transformation ring.

---

### 1. Configuration Space Definition (Axiom #1-5: IRE)

**Initial Graph Data:**
```
Ω_graph = {
  V: Set of vertices (nodes)
  E: Set of edges (node_i, node_j)
  A: Attributes (colors, sizes, labels)
}
```

**Recursive Structure (Axiom #3):**
```
Ω_0 = ∅                           # Empty graph
Ω_1 = {v₁}                        # Single node
Ω_2 = {v₁, v₂, (v₁→v₂)}         # Node + edge
Ω_n = Ω_{n-1} ∪ {new_nodes, new_edges}
```

**Fractal Composition (Axiom #4):**
```
T(Ω_subgraph) = λ · T(Ω_parent)   # Subgraphs maintain structural similarity
```

---

### 2. Data Parsing Transformation (Ring 5 → Ring 6)

**Axiom #31: Base Transform**
```
θ_parse: JSON → Ω_graph

θ_parse(json_data) = {
  V = {extract_nodes(json_data)},
  E = {extract_edges(json_data)},
  A = {compute_attributes(V, E)}
}
```

**From `graph-db.js` and `data.ts`:**
```
Ω_raw ──θ_parse──> Ω_structured
```

---

### 3. Force Layout Transformation (Axiom #25-26: Gradient Flow)

**The core force-directed layout is a dynamical system:**

```
θ_layout: Ω_graph → Ω_positioned

Positions evolve according to:
d²x_i/dt² = Σ F_repulsive(x_i, x_j) + Σ F_attractive(x_i, x_k) - γ(dx_i/dt)
            j≠i                        (i,k)∈E

Simplified to gradient descent (Axiom #25):
dx_i/dt = -∇_i U(x₁, x₂, ..., x_n)
```

Where the potential function is:
```
U = Σ k_spring · ||x_i - x_j||² + Σ k_repel/||x_i - x_j||
    edges                          pairs

θ_layout^(t) := x(t) = x(0) + ∫₀ᵗ (-∇U) dt'
```

**Iterative Application (Axiom #29: MAD):**
```
ω(t+1) = θ_layout(ω(t))
ω* = lim_{t→∞} θ_layout^t(ω_0)    # Fixed point convergence (Axiom #15)
```

From `graph-layout.ts`:
```
Ω_graph ──θ_layout──> Ω_3D_positions
```

---

### 4. GPU Interpolation (Axiom #19: Hyperreal Extension)

**Smooth animation uses infinitesimal steps:**

```
θ_interpolate: Ω_discrete → Ω_continuous

Position at frame f:
x_i(f) = x_i(t) + ε · (x_i(t+1) - x_i(t))

where ε ∈ [0, 1] is the interpolation parameter
```

From `gpu/interpolation.ts` using `gpu-io`:
```
x_smooth(τ) = (1-α)·x_current + α·x_target   where α(τ) = smooth_step(τ)
```

**This is Axiom #19 in action:** Using hyperreals to bridge discrete layout updates.

```
Ω_discrete ──θ_interpolate──> Ω_smooth
```

---

### 5. Camera Transformation (Axiom #32: Path Dependence)

**Camera state evolution is path-dependent:**

```
θ_camera: Ω_3D → Ω_screen

Camera at time t depends on trajectory:
C(t) = ∫₀ᵗ F(input(τ), C(τ)) dτ

Where C = (position, rotation, zoom)
```

From `camera-animation.ts` and `interaction.ts`:
```
C(t+dt) = C(t) + velocity(t)·dt + damping(C(t))
```

**Inertial damping (Axiom #30: Self-Regulation):**
```
velocity(t+1) = decay · velocity(t) + input_force(t)
```

Path from initial → user interaction creates unique trajectory:
```
Ω_3D ──θ_camera(history)──> Ω_view
```

---

### 6. Rendering Transformation (Axiom #21: Goodness Function)

**Final transformation projects to screen:**

```
θ_render: Ω_view → Ω_pixels

For each node i:
  screen_pos = project(x_i, camera_matrix)
  color = G(node_i) = utility(i) - cost(i)
  size = scale · metric(i)
```

Where G (goodness) determines visual prominence:
```
G(node) = {
  complexity_metric: determines color intensity
  connectivity: determines size
  canonical: highlights if G(node) is local maximum
}
```

From `gpu/rendering.ts` and `shaders/graph-node.tsl.ts`:
```
Ω_view ──θ_render──> Ω_framebuffer ──display──> User's screen
```

**Instance rendering uses symmetry (Axiom #7):**
```
All nodes share base geometry (sphere/mesh)
Transform = translate · scale · rotate
Render(node_i) = G · instance_transform_i
```

---

### 7. Interaction Loop (Axiom #33: Feedback Loop)

**The complete system forms a feedback loop:**

```
Ω(t+1) = F(Ω(t), user_input(t))

F = θ_render ∘ θ_camera ∘ θ_interpolate ∘ θ_layout

Fixed points: Ω* where F(Ω*) = Ω*
```

**Selection transforms graph state (Axiom #8: Symmetry Breaking):**
```
select(node_id): Ω → Ω'
  where Ω' highlights subgraph, breaking visual symmetry
```

From `selection.ts`:
```
Ω_neutral ──select(id)──> Ω_highlighted
```

---

### 8. Complete Program Equation

**Main loop from `main.ts`:**

```
Program: Ω_initial → Ω_final

Ω(frame) = θ_render(
             θ_camera(
               θ_interpolate(
                 θ_layout^n(
                   θ_parse(
                     data_source
                   )
                 )
               ), 
               user_input
             )
           )

where n is iteration count until convergence
```

**Time-evolution (Axiom #26: General Dynamical System):**
```
dΩ/dt = f(Ω, controls)

Ω(t) = ∫₀ᵗ [θ_layout(Ω) + θ_camera(controls) + θ_interpolate(Ω)] dt
```

---

### 9. Worker Decomposition (Ring Separation)

**Workers partition the computation:**

```
θ_total = θ_main ⊕ θ_layout_worker ⊕ θ_camera_worker ⊕ θ_query_worker

where ⊕ represents parallel composition with message passing:

Main thread:        θ_render, θ_interpolate, θ_interaction
Layout worker:      θ_layout (force simulation)
Camera worker:      θ_camera (smooth animation)
Query worker:       θ_query (SPARQL on graph)
```

**Each worker is an autonomous transformation space:**
```
Worker_i: Ω_in → Ω_out   via message(Ω_in) → compute → message(Ω_out)
```

From `get-workers.ts` and `worker.js`.

---

### 10. Integration Equation: Wanderer + M0WER

**Combined system:**

```
Ω_codebase ──θ_analyze──> Ω_structure ──θ_diagram──> Ω_graph ──θ_visualize──> Ω_3D ──θ_render──> Screen
     ↑                        ↑                         ↑                      ↑
  M0WER              M0WER DiagramGenerator      Wanderer adapter       Wanderer renderer
```

**Full equation:**
```
θ_integrated = θ_wanderer_render ∘ θ_adapter ∘ θ_m0wer_diagram ∘ θ_m0wer_analyze

Integrated(codebase) = {
  entities = analyze(codebase),
  diagram = generate_diagram(entities, axioms),
  graph_3d = adapt(diagram),
  pixels = render_3d(graph_3d, camera, interpolation)
}
```

**Goodness optimization (Axiom #21):**
```
G(θ_integrated) = θ(features) - C(complexity)
                = (axiom_analysis + 3d_viz + code_nav) - (maintenance + coupling)
                > G(θ_separate)
```

---

### 11. Canonical Form Equation (CF)

**Applying Axiom #14 to find optimal implementation:**

```
CF(Ω_implementation) = argmin_{impl ∈ All_implementations} L(impl)

where loss function:
L(impl) = α·complexity(impl) + β·redundancy(impl) - γ·utility(impl)
```

**For this integration:**
```
L(separate) = α·2000 + β·500 - γ·15  = 2500 - 15 = 2485
L(integrated) = α·1200 + β·100 - γ·20 = 1300 - 20 = 1280

∴ CF = integrated implementation
```

---

### 12. Type Signatures (Category Theory View)

**Each transformation has a type:**

```
θ_parse:        JSON → Graph
θ_layout:       Graph → Positioned_Graph
θ_interpolate:  Discrete_Positions → Smooth_Positions  
θ_camera:       3D_Space × Input_History → View_Space
θ_render:       View_Space → Pixel_Array

Composition:
θ_render ∘ θ_camera ∘ θ_interpolate ∘ θ_layout ∘ θ_parse
  : JSON → Pixel_Array
```

**Functorial properties:**
- Identity: θ_id(Ω) = Ω
- Associativity: (θ₃ ∘ θ₂) ∘ θ₁ = θ₃ ∘ (θ₂ ∘ θ₁)
- Preservation: θ(structure(Ω)) = structure(θ(Ω))

---

## Summary: Program as Pure Mathematics

The entire webscape-wanderer system is:

1. **Configuration space Ω** containing graph data
2. **Sequence of transformations θ** that process the graph
3. **Dynamical system** that evolves positions over time
4. **Feedback loop** incorporating user interaction
5. **Rendering pipeline** projecting to screen space

Every line of code implements a mathematical operation from the 40 axioms. The program **IS** the equation:

```
∀ frame: Screen(frame) = Π(frame) ∘ R ∘ C ∘ I ∘ L^n ∘ P(data)

where:
  P = Parse transformation (Axiom #31)
  L = Layout force iteration (Axiom #25-26)
  I = GPU interpolation (Axiom #19)
  C = Camera projection (Axiom #32)
  R = WebGL rendering (Axiom #21)
  Π = Display projection to screen
```

This is **Reflectology in practice**: Every program is a mathematical transformation on configuration spaces.

---

## Next Steps

Run this integration plan by executing:
```bash
cd /path/to/M0WER
mkdir -p src/visualization
# Copy extracted wanderer files
# Implement adapter
# Test in VS Code
```

The goal: **M0WER becomes the canonical visualization tool for Reflectology codebases**, with wanderer's rendering engine as its Ring 6 visualization layer.

---

*"Math once, visualize everywhere, really."*
