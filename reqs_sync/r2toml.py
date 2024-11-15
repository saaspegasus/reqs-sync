#!/usr/bin/env python3
import tomli
import tomli_w
from pathlib import Path


def parse_requirements(requirements_file):
    """Parse requirements.in file and return cleaned dependencies."""
    dependencies = []

    with open(requirements_file, 'r') as f:
        for line in f:
            # Skip empty lines, comments, and constraint files
            line = line.strip()
            if (not line or
                line.startswith('#') or
                line.startswith('-c') or
                line.startswith('--constraint')):
                continue

            # Handle extras syntax (e.g., package[extra1,extra2])
            if '[' in line:
                package = line.split('#')[0].strip()  # Remove inline comments
                dependencies.append(package)
            else:
                # Remove any inline comments and version specifiers
                package = line.split('#')[0].strip()
                dependencies.append(package)

    return dependencies


def create_default_pyproject():
    """Create default pyproject.toml structure."""
    return {
        "project": {
            "name": "",
            "version": "0.1.0",
            "description": "",
            "authors": [],
            "dependencies": []
        },
        "build-system": {
            "requires": ["setuptools>=61.0"],
            "build-backend": "setuptools.build_meta"
        },
        "dependency-groups": {}
    }


def update_pyproject_toml(dependencies, output_file='pyproject.toml', group=None):
    """Update or create pyproject.toml with the parsed dependencies.

    Args:
        dependencies: List of dependencies to add
        output_file: Path to pyproject.toml
        group: Optional group name. If None, updates project.dependencies
    """
    try:
        with open(output_file, 'rb') as f:
            pyproject_data = tomli.load(f)
            print(f"Found existing {output_file}")
    except FileNotFoundError:
        pyproject_data = create_default_pyproject()
        print(f"Creating new {output_file}")

    if group:
        # Handle dependency group
        if "dependency-groups" not in pyproject_data:
            pyproject_data["dependency-groups"] = {}
        if group not in pyproject_data["dependency-groups"]:
            pyproject_data["dependency-groups"][group] = []

        # Update group dependencies
        pyproject_data["dependency-groups"][group] = dependencies
        print(f"Updating dependencies for group: {group}")
    else:
        # Ensure project section exists
        if 'project' not in pyproject_data:
            pyproject_data['project'] = {}

        # Update project dependencies
        pyproject_data['project']['dependencies'] = dependencies
        print("Updating main project dependencies")

    # Write updated pyproject.toml
    with open(output_file, 'wb') as f:
        tomli_w.dump(pyproject_data, f)
