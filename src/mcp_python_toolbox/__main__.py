"""
Main entry point for the MCP Python Toolbox server.
"""

import os
import argparse
from pathlib import Path
from .server import PythonToolboxServer

def main() -> None:
    """Run the MCP Python Toolbox server."""
    parser = argparse.ArgumentParser(description="MCP Python Toolbox Server")
    parser.add_argument(
        "--workspace",
        type=str,
        default=os.getcwd(),
        help="Path to the workspace root directory (default: current directory)"
    )

    args = parser.parse_args()
    workspace_root = Path(args.workspace).resolve()

    server = PythonToolboxServer(workspace_root)
    server.setup()
    server.run()

if __name__ == "__main__":
    main() 