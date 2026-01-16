#!/usr/bin/env python3
"""
End-to-end test: Ring 8 deployment → Ring 6 visualization → Ring 7 webview

This demonstrates the full pipeline:
1. Generate Azure ARM template
2. Convert to PlantUML diagram
3. Transform to Omega state
4. Visualize in 3D graph (webscape-wanderer format)
5. Display in Ring 7 web UI

Run: python test_deployment_viz.py
"""

import sys
import json
from pathlib import Path

# Add all rings to path
rings_root = Path(__file__).parent
for ring in ['ring0-math-kernel', 'ring6-visualization', 'ring7-ui', 'ring8-deployment']:
    sys.path.insert(0, str(rings_root / ring))

from ring8_deployment import AzureDeployment, AZURE_SDK_AVAILABLE

def test_full_pipeline():
    print("="*60)
    print("Ring 8 → Ring 6 → Ring 7 Integration Test")
    print("="*60)
    
    # Step 1: Generate ARM template
    print("\n[Step 1] Generating Azure ARM template...")
    deployer = AzureDeployment()
    template = deployer.generate_arm_template("reflectology-app", "eastus")
    print(f"✅ Template created: {len(template['resources'])} resources")
    
    # Step 2: Generate PlantUML
    print("\n[Step 2] Generating PlantUML diagram...")
    puml = deployer.generate_plantuml(template)
    print(f"✅ PlantUML generated: {len(puml.split(chr(10)))} lines")
    print("\nPlantUML Diagram:")
    print("-" * 60)
    print(puml)
    print("-" * 60)
    
    # Step 3: Convert to Omega state
    print("\n[Step 3] Converting to Omega configuration space...")
    omega = deployer.to_omega_state(template)
    print(f"✅ Omega state: {len(omega)} keys")
    print(f"   Keys: {list(omega.keys())}")
    
    # Step 4: Generate visualization data
    print("\n[Step 4] Generating visualization data for webscape-wanderer...")
    viz_data = deployer.generate_visualization_data(template)
    print(f"✅ Visualization package ready:")
    print(f"   - PlantUML: {len(viz_data['puml'])} chars")
    print(f"   - Omega: {len(viz_data['omega'])} keys")
    print(f"   - Graph nodes: {len(viz_data['graph']['nodes'])}")
    print(f"   - Graph edges: {len(viz_data['graph']['linkIndexPairs']) // 2}")
    
    # Step 5: Save outputs
    print("\n[Step 5] Saving outputs...")
    
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Save template
    template_file = output_dir / "deployment_template.json"
    with open(template_file, 'w') as f:
        json.dump(template, f, indent=2)
    print(f"✅ Template: {template_file}")
    
    # Save PlantUML
    puml_file = output_dir / "deployment_diagram.puml"
    with open(puml_file, 'w') as f:
        f.write(puml)
    print(f"✅ PlantUML: {puml_file}")
    
    # Save visualization data
    viz_file = output_dir / "deployment_viz.json"
    with open(viz_file, 'w') as f:
        json.dump(viz_data, f, indent=2)
    print(f"✅ Viz data: {viz_file}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ INTEGRATION TEST PASSED")
    print("="*60)
    print("\nNext steps:")
    print(f"1. View PlantUML: cat {puml_file}")
    print(f"2. Render diagram: plantuml {puml_file}")
    print(f"3. Launch Ring 7 GUI: python ring7-ui/ring7_webui.py --web")
    print(f"4. Load viz data in browser: http://localhost:8080")
    
    # Check Azure SDK
    print("\n" + "="*60)
    print("Azure SDK Status")
    print("="*60)
    if AZURE_SDK_AVAILABLE:
        print("✅ Azure SDK installed")
        print("\nTo deploy to Azure:")
        print("1. Set environment variables:")
        print("   export AZURE_SUBSCRIPTION_ID='...'")
        print("   export AZURE_CLIENT_ID='...'")
        print("   export AZURE_TENANT_ID='...'")
        print("   export AZURE_CLIENT_SECRET='...'")
        print(f"2. Run: python ring8-deployment/ring8_cli.py deploy {template_file} my-resource-group")
    else:
        print("⚠️  Azure SDK not installed")
        print("   Install: pip install azure-mgmt-resource azure-identity")
        print("   Note: PlantUML and visualization work without Azure SDK")
    
    return viz_data

if __name__ == "__main__":
    test_full_pipeline()
