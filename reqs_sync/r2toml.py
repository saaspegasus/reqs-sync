#!/usr/bin/env python3
import sys
import re
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
        "tool": {
            "uv": {
                "dev-dependencies": []
            }
        }
    }


def update_pyproject_toml(dependencies, output_file='pyproject.toml', dev=False):
    """Update or create pyproject.toml with the parsed dependencies."""
    try:
        # Try to read existing pyproject.toml
        with open(output_file, 'rb') as f:
            pyproject_data = tomli.load(f)
            print(f"Found existing {output_file}")
    except FileNotFoundError:
        # Create new pyproject.toml with default structure
        pyproject_data = create_default_pyproject()
        print(f"Creating new {output_file}")

    if dev:
        # Ensure tool.uv.dev-dependencies exists
        if "tool" not in pyproject_data:
            pyproject_data["tool"] = {}
        if "uv" not in pyproject_data["tool"]:
            pyproject_data["tool"]["uv"] = {}
        if "dev-dependencies" not in pyproject_data["tool"]["uv"]:
            pyproject_data["tool"]["uv"]["dev-dependencies"] = []

        # Update dev dependencies
        pyproject_data["tool"]["uv"]["dev-dependencies"] = dependencies
    else:
        # Ensure project section exists
        if 'project' not in pyproject_data:
            pyproject_data['project'] = {}

        # Update project dependencies
        pyproject_data['project']['dependencies'] = dependencies

    # Write updated pyproject.toml
    with open(output_file, 'wb') as f:
        tomli_w.dump(pyproject_data, f)


def main():
    if len(sys.argv) != 2:
        print("Usage: python r2toml.py requirements.in")
        sys.exit(1)

    requirements_file = sys.argv[1]
    if not Path(requirements_file).exists():
        print(f"Error: File {requirements_file} not found")
        sys.exit(1)

    dependencies = parse_requirements(requirements_file)
    update_pyproject_toml(dependencies)
    print(f"Successfully updated pyproject.toml with {len(dependencies)} dependencies")


if __name__ == "__main__":
    main()
