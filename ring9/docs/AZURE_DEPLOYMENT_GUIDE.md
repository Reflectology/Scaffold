# Azure Deployment → Visualization Pipeline

## Overview

Ring 8 now integrates with Azure SDK, generates PlantUML diagrams, and feeds deployment data to Ring 6/7 for visualization.

## Architecture

```
Ring 8 (Deployment)
    ↓ ARM Template
    ↓ Azure SDK
    ↓ deploy_to_azure()
    ↓
    ├→ PlantUML Diagram (.puml)
    ├→ Omega State (Ω configuration)
    └→ Graph Data (webscape-wanderer format)
        ↓
        Ring 6 (Visualization)
            ↓ 3D Graph
            ↓
            Ring 7 (Web UI)
                ↓ Browser Display
```

## Installation

### Core System (No Azure Deployment)
```bash
# Works out of the box - PlantUML and visualization only
cd PythonRings
python3 test_deployment_viz.py
```

### Full Azure Integration
```bash
# Install Azure SDK
pip install azure-mgmt-resource azure-identity

# Set Azure credentials
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_SECRET="your-client-secret"

# Test deployment
python3 ring8-deployment/ring8_cli.py status
```

## Usage Examples

### 1. Generate ARM Template

```bash
cd PythonRings/ring8-deployment
python3 ring8_cli.py template my-app eastus > template.json
```

**Output**: `template.json` with Azure resources

### 2. Generate PlantUML Diagram

```bash
python3 ring8_cli.py plantuml template.json -o diagram.puml
```

**Output**: `diagram.puml` ready for rendering

```plantuml
@startuml Azure Deployment
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/release/2-1/dist
!includeurl AzurePuml/AzureCommon.puml
!includeurl AzurePuml/Web/AzureWebApp.puml
!includeurl AzurePuml/Compute/AzureAppService.puml

title Reflectology Azure Deployment

AzureAppService(plan0, "my-app-plan", "App Service Plan")
AzureWebApp(app1, "my-app", "Web App")
plan0 -down-> app1 : hosts
@enduml
```

### 3. Deploy to Azure

```bash
python3 ring8_cli.py deploy template.json my-resource-group --name my-deployment
```

**Output**:
```json
{
  "status": "success",
  "deployment_name": "my-deployment",
  "resource_group": "my-resource-group",
  "provisioning_state": "Succeeded",
  "resources": 2,
  "timestamp": 1737849600.0
}
```

### 4. Visualize Deployment

```bash
python3 ring8_cli.py visualize template.json --port 8080
```

**Output**: 
- Saves `template_viz.json` with Omega state + graph data
- Instructions to launch Ring 7 web UI

### 5. End-to-End Test

```bash
cd PythonRings
python3 test_deployment_viz.py
```

**Validates**:
- ✅ ARM template generation
- ✅ PlantUML diagram creation
- ✅ Omega state conversion
- ✅ Graph data for visualization
- ✅ File output to `test_output/`

## Integration Points

### Ring 8 → Ring 6 (Omega Conversion)

```python
from ring8_deployment import AzureDeployment

deployer = AzureDeployment()
template = deployer.generate_arm_template("my-app")

# Convert to Omega state
omega = deployer.to_omega_state(template)
# {
#   "deployment_type": "azure_arm",
#   "resource_count": 2,
#   "resource_0": {...},
#   "resource_1": {...}
# }
```

### Ring 8 → Ring 7 (Visualization Data)

```python
viz_data = deployer.generate_visualization_data(template)
# {
#   "puml": "...",       # PlantUML diagram
#   "omega": {...},      # Omega state
#   "graph": {           # Webscape-wanderer format
#     "nodes": ["app", "plan"],
#     "linkIndexPairs": [0, 1],
#     "nodeData": {...}
#   },
#   "template": {...}    # Original ARM template
# }
```

### Ring 7 Web UI Display

The Ring 7 GUI can display deployment visualizations:
1. **Dashboard Tab**: Omega metrics (cost, entropy, dimension)
2. **Visualization Tab**: 3D graph of resources
3. **PlantUML Tab** (future): Rendered deployment diagram

## PlantUML Rendering

### Option 1: PlantUML CLI
```bash
# Install PlantUML
brew install plantuml  # macOS
apt install plantuml   # Ubuntu

# Render diagram
plantuml test_output/deployment_diagram.puml
# Output: deployment_diagram.png
```

### Option 2: Online Renderer
```bash
# Copy .puml content to: http://www.plantuml.com/plantuml/uml/
cat test_output/deployment_diagram.puml
```

### Option 3: VS Code Extension
Install "PlantUML" extension and open `.puml` files

## Axiom Integration

Ring 8 deployments follow Reflectology axioms:

| Axiom | Application | Effect |
|-------|-------------|--------|
| **o1** (Initial Emptiness) | Empty resource group | Clean deployment state |
| **o2** (First Structure) | Add first resource | Establish baseline |
| **o3** (Recursive Encapsulation) | Nested resources | Hierarchical dependencies |
| **o6** (Redundancy Reduction) | Deduplication | Minimize resource overlap |
| **o14** (Canonical Selection) | Optimal resource selection | Best SKU/region choice |
| **o40** (Dual Symmetry) | Deployment ↔ Teardown | Reversible operations |

## File Outputs

After running `test_deployment_viz.py`:

```
PythonRings/test_output/
├── deployment_template.json   # ARM template
├── deployment_diagram.puml    # PlantUML diagram
└── deployment_viz.json        # Full visualization data
```

## Verification

### Check System Status
```bash
python3 ring8-deployment/ring8_cli.py status
```

**Expected Output**:
```
Ring 8 Deployment System Status
==================================================
Azure SDK Available: ✅ Yes
AZURE_SUBSCRIPTION_ID: ✅ Set
AZURE_CLIENT_ID: ✅ Set
AZURE_TENANT_ID: ✅ Set
AZURE_CLIENT_SECRET: ✅ Set

Azure Client: ✅ Authenticated

PlantUML Generator: ✅ Available
Omega Converter: ✅ Available
Visualization Integration: ✅ Available
```

### Verify Integration
```bash
python3 -c "
import sys
sys.path.insert(0, 'ring0-math-kernel')
sys.path.insert(0, 'ring8-deployment')
from ring8_deployment import AzureDeployment
d = AzureDeployment()
t = d.generate_arm_template('test')
print('✅ Template:', len(t['resources']), 'resources')
puml = d.generate_plantuml(t)
print('✅ PlantUML:', len(puml.split('\n')), 'lines')
viz = d.generate_visualization_data(t)
print('✅ Viz data:', list(viz.keys()))
"
```

## Troubleshooting

### "Azure SDK not installed"
```bash
pip install azure-mgmt-resource azure-identity
```

### "Azure credentials not configured"
Set environment variables or use Azure CLI:
```bash
az login
az account show  # Get subscription ID
```

### "ModuleNotFoundError: No module named 'ring0_kernel'"
```bash
# Run from PythonRings/ directory
cd /path/to/PythonRings
python3 test_deployment_viz.py
```

### PlantUML Rendering Fails
- Check PlantUML syntax at http://www.plantuml.com/plantuml/
- Verify `!includeurl` URLs are accessible
- Use local Azure-PlantUML files if offline

## Advanced: Custom Deployments

### Add Database Resource
```python
from ring8_deployment import AzureDeployment

deployer = AzureDeployment()
template = deployer.generate_arm_template("my-app")

# Add SQL Database
sql_server = {
    "type": "Microsoft.Sql/servers",
    "apiVersion": "2021-02-01-preview",
    "name": "my-sql-server",
    "location": "eastus",
    "properties": {
        "administratorLogin": "sqladmin",
        "administratorLoginPassword": "[parameters('sqlPassword')]"
    }
}

template["resources"].append(sql_server)

# Regenerate visualization
viz_data = deployer.generate_visualization_data(template)
print(f"Resources: {len(viz_data['graph']['nodes'])}")
```

### Deploy with Custom Parameters
```python
deployment_result = deployer.deploy_to_azure(
    template,
    resource_group="prod-rg",
    deployment_name="reflectology-prod-v1"
)

if deployment_result["status"] == "success":
    print(f"✅ Deployed: {deployment_result['deployment_name']}")
else:
    print(f"❌ Error: {deployment_result['message']}")
```

## Next Steps

1. **Install Azure SDK** for live deployments
2. **Render PlantUML diagrams** with plantuml CLI or online tool
3. **Launch Ring 7 GUI** to visualize deployments in browser
4. **Integrate with CI/CD** pipeline (GitHub Actions, Azure DevOps)
5. **Add monitoring** to track deployment status in real-time

## References

- Azure SDK Documentation: https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/
- PlantUML Azure Library: https://github.com/plantuml-stdlib/Azure-PlantUML
- Ring 8 Implementation: [ring8_deployment.py](ring8-deployment/ring8_deployment.py)
- Integration Test: [test_deployment_viz.py](test_deployment_viz.py)
- System Status: [SYSTEM_STATUS.md](SYSTEM_STATUS.md)
