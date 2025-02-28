"""Module for managing Python project dependencies and virtual environments."""

import os
import subprocess
import venv
from importlib.metadata import distribution, distributions
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
import toml
from packaging import version
from packaging.requirements import Requirement

class ProjectManager:
    """Manages Python project setup, dependencies, and virtual environments.

    This class provides functionality for:
    - Creating and managing virtual environments
    - Installing and updating project dependencies
    - Managing requirements files
    - Checking for dependency conflicts
    - Listing installed packages

    Attributes:
        workspace_root (Path): The root directory of the workspace
        venv_path (Path): Path to the virtual environment directory
    """

    def __init__(self, workspace_root: Union[str, Path]):
        """Initialize the ProjectManager.

        Args:
            workspace_root: Path to the workspace root directory
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.venv_path = self.workspace_root / '.venv'

    def create_virtual_environment(self) -> None:
        """Create a virtual environment in the project directory.

        Creates a new virtual environment with pip installed if one doesn't already exist.
        The environment is created in the .venv directory within the workspace root.

        Raises:
            OSError: If virtual environment creation fails
        """
        if not self.venv_path.exists():
            venv.create(self.venv_path, with_pip=True)

    def _get_python_path(self) -> Path:
        """Get the path to the Python executable in the virtual environment.

        Returns:
            Path: The path to the Python executable

        Raises:
            FileNotFoundError: If the Python executable is not found in the virtual environment
        """
        if os.name == 'nt':  # Windows
            python_path = self.venv_path / 'Scripts' / 'python.exe'
        else:  # Unix-like
            python_path = self.venv_path / 'bin' / 'python'
        
        if not python_path.exists():
            raise FileNotFoundError(f"Python executable not found in virtual environment: {python_path}")
        
        return python_path

    def install_dependencies(self, requirements_file: Optional[Union[str, Path]] = None) -> None:
        """Install project dependencies from requirements.txt or pyproject.toml.

        If no requirements file is specified, the method will look for:
        1. requirements.txt in the workspace root
        2. pyproject.toml in the workspace root

        Args:
            requirements_file: Optional path to a requirements file

        Raises:
            FileNotFoundError: If no requirements file is found
            subprocess.CalledProcessError: If pip install fails
        """
        python_path = self._get_python_path()
        
        if requirements_file:
            req_path = Path(requirements_file)
        else:
            # Try to find requirements file
            req_path = self.workspace_root / 'requirements.txt'
            pyproject_path = self.workspace_root / 'pyproject.toml'
            
            if not req_path.exists() and pyproject_path.exists():
                # Use pyproject.toml
                self._install_from_pyproject(python_path, pyproject_path)
                return
            elif not req_path.exists():
                raise FileNotFoundError("No requirements.txt or pyproject.toml found")
        
        subprocess.run(
            [str(python_path), '-m', 'pip', 'install', '-r', str(req_path)],
            check=True
        )

    def _install_from_pyproject(self, python_path: Path, pyproject_path: Path) -> None:
        """Install dependencies from pyproject.toml.

        Args:
            python_path: Path to the Python executable
            pyproject_path: Path to the pyproject.toml file

        Raises:
            subprocess.CalledProcessError: If pip install fails
        """
        with open(pyproject_path, 'r') as f:
            pyproject = toml.load(f)
        
        if 'project' in pyproject and 'dependencies' in pyproject['project']:
            deps = pyproject['project']['dependencies']
            subprocess.run(
                [str(python_path), '-m', 'pip', 'install'] + deps,
                check=True
            )

    def get_installed_packages(self) -> List[Dict[str, str]]:
        """Get a list of installed packages and their versions.

        Returns:
            List of dictionaries containing:
                - name: Package name
                - version: Package version
        """
        packages = []
        for dist in distributions():
            packages.append({
                'name': dist.metadata['Name'],
                'version': dist.version
            })
        return packages

    def check_dependency_conflicts(self) -> List[Dict[str, Any]]:
        """Check for dependency conflicts in installed packages.

        Analyzes all installed packages and their requirements to identify
        version conflicts between dependencies.

        Returns:
            List of dictionaries containing:
                - package: Name of the package with a conflict
                - requires: The requirement specification that is not met
                - installed: The currently installed version
        """
        conflicts = []
        installed = {dist.metadata['Name']: dist for dist in distributions()}
        
        for pkg_name, dist in installed.items():
            pkg_requires = dist.requires or []
            for req_str in pkg_requires:
                req = Requirement(req_str)
                if req.name in installed:
                    req_version = version.parse(installed[req.name].version)
                    if not req.specifier.contains(req_version):
                        conflicts.append({
                            'package': pkg_name,
                            'requires': str(req),
                            'installed': str(req_version)
                        })
        return conflicts

    def update_package(self, package_name: str, version: Optional[str] = None) -> None:
        """Update a specific package to the latest or specified version.

        Args:
            package_name: Name of the package to update
            version: Optional specific version to install. If None, updates to latest

        Raises:
            subprocess.CalledProcessError: If pip install fails
        """
        python_path = self._get_python_path()
        cmd = [str(python_path), '-m', 'pip', 'install', '--upgrade']
        
        if version:
            cmd.append(f"{package_name}=={version}")
        else:
            cmd.append(package_name)
        
        subprocess.run(cmd, check=True)

    def create_requirements_file(self) -> None:
        """Create a requirements.txt file from installed packages.

        Generates a requirements.txt file in the workspace root containing
        all currently installed packages and their versions.

        Raises:
            subprocess.CalledProcessError: If pip freeze fails
            IOError: If unable to write to requirements.txt
        """
        python_path = self._get_python_path()
        req_path = self.workspace_root / 'requirements.txt'
        
        with open(req_path, 'w') as f:
            subprocess.run(
                [str(python_path), '-m', 'pip', 'freeze'],
                stdout=f,
                check=True
            ) 