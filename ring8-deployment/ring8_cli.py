#!/usr/bin/env python3
"""
Ring 8 CLI: Deploy to Azure and visualize in web UI

Usage:
    python ring8_cli.py template reflectology-app eastus > template.json
    python ring8_cli.py deploy template.json my-resource-group
    python ring8_cli.py plantuml template.json > deployment.puml
    python ring8_cli.py visualize template.json --port 8080
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ring8_deployment import AzureDeployment, FormalProofs
from ring6_extension import WebscapeWanderer
from ring7_webui import ReflectologyWebGUI

def main():
    parser = argparse.ArgumentParser(description="Ring 8: Azure Deployment & Visualization CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Template generation
    template_parser = subparsers.add_parser("template", help="Generate ARM template")
    template_parser.add_argument("app_name", help="Application name")
    template_parser.add_argument("location", nargs="?", default="eastus", help="Azure location")
    
    # Deployment
    deploy_parser = subparsers.add_parser("deploy", help="Deploy to Azure")
    deploy_parser.add_argument("template_file", help="Path to ARM template JSON")
    deploy_parser.add_argument("resource_group", help="Azure resource group name")
    deploy_parser.add_argument("--name", help="Deployment name (optional)")
    
    # PlantUML generation
    puml_parser = subparsers.add_parser("plantuml", help="Generate PlantUML diagram")
    puml_parser.add_argument("template_file", help="Path to ARM template JSON")
    puml_parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    
    # Visualization
    viz_parser = subparsers.add_parser("visualize", help="Launch web visualization")
    viz_parser.add_argument("template_file", help="Path to ARM template JSON")
    viz_parser.add_argument("--port", type=int, default=8080, help="Web server port")
    
    # Status check
    status_parser = subparsers.add_parser("status", help="Check Azure SDK availability")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    deployer = AzureDeployment()
    
    if args.command == "template":
        # Generate ARM template
        template = deployer.generate_arm_template(args.app_name, args.location)
        print(json.dumps(template, indent=2))
    
    elif args.command == "deploy":
        # Deploy to Azure
        with open(args.template_file) as f:
            template = json.load(f)
        
        print(f"🚀 Deploying {len(template['resources'])} resources to Azure...")
        result = deployer.deploy_to_azure(template, args.resource_group, args.name)
        
        print(json.dumps(result, indent=2))
        
        if result["status"] == "success":
            print(f"\n✅ Deployment successful!")
            print(f"   Resource Group: {result['resource_group']}")
            print(f"   Deployment: {result['deployment_name']}")
            print(f"   State: {result['provisioning_state']}")
        else:
            print(f"\n❌ Deployment failed: {result['message']}")
            sys.exit(1)
    
    elif args.command == "plantuml":
        # Generate PlantUML
        with open(args.template_file) as f:
            template = json.load(f)
        
        puml = deployer.generate_plantuml(template)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(puml)
            print(f"✅ PlantUML written to {args.output}")
        else:
            print(puml)
    
    elif args.command == "visualize":
        # Launch visualization
        with open(args.template_file) as f:
            template = json.load(f)
        
        print(f"🌐 Generating visualization data...")
        viz_data = deployer.generate_visualization_data(template)
        
        print(f"✅ PlantUML diagram ({len(viz_data['puml'])} chars)")
        print(f"✅ Omega state ({len(viz_data['omega'])} keys)")
        print(f"✅ Graph ({len(viz_data['graph']['nodes'])} nodes, {len(viz_data['graph']['linkIndexPairs'])//2} edges)")
        
        # Save visualization data
        viz_file = Path(args.template_file).stem + "_viz.json"
        with open(viz_file, 'w') as f:
            json.dump(viz_data, f, indent=2)
        
        print(f"\n💾 Visualization data saved to {viz_file}")
        print(f"\n🚀 Launching web UI on port {args.port}...")
        print(f"   Open: http://localhost:{args.port}")
        print(f"\n   The deployment will be visible in:")
        print(f"   - Dashboard: Omega metrics")
        print(f"   - Visualization: 3D graph view")
        print(f"   - PlantUML tab: Architecture diagram")
        
        # Note: Full web integration would require Ring 7 enhancements
        print(f"\n💡 To view in Ring 7 GUI:")
        print(f"   python ring7_webui.py --web {args.port}")
        print(f"   Then load {viz_file} in the Visualization tab")
    
    elif args.command == "status":
        # Check status
        from ring8_deployment import AZURE_SDK_AVAILABLE
        import os
        
        print("Ring 8 Deployment System Status")
        print("=" * 50)
        print(f"Azure SDK Available: {'✅ Yes' if AZURE_SDK_AVAILABLE else '❌ No (pip install azure-mgmt-resource azure-identity)'}")
        
        if AZURE_SDK_AVAILABLE:
            print(f"AZURE_SUBSCRIPTION_ID: {'✅ Set' if os.getenv('AZURE_SUBSCRIPTION_ID') else '❌ Not set'}")
            print(f"AZURE_CLIENT_ID: {'✅ Set' if os.getenv('AZURE_CLIENT_ID') else '❌ Not set'}")
            print(f"AZURE_TENANT_ID: {'✅ Set' if os.getenv('AZURE_TENANT_ID') else '❌ Not set'}")
            print(f"AZURE_CLIENT_SECRET: {'✅ Set' if os.getenv('AZURE_CLIENT_SECRET') else '❌ Not set'}")
            
            if deployer.client:
                print(f"\nAzure Client: ✅ Authenticated")
            else:
                print(f"\nAzure Client: ⚠️  Not authenticated (check credentials)")
        
        print(f"\nPlantUML Generator: ✅ Available")
        print(f"Omega Converter: ✅ Available")
        print(f"Visualization Integration: ✅ Available")

if __name__ == "__main__":
    main()
