import json
import re
from typing import List

import tomli


class DependencyParser:
    """Class for parsing different types of dependency files"""

    def parse_requirements_txt(self, content: str) -> List[str]:
        """Parse a requirements.txt file and extract package names

        Args:
            content: The content of the requirements.txt file

        Returns:
            A list of package names
        """
        packages = []
        lines = content.strip().split("\n")

        for line in lines:
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            if line.strip():
                packages.append(line.strip())

        return packages

    def parse_package_json(self, content: str) -> List[str]:
        """Parse a package.json file and extract package names

        Args:
            content: The content of the package.json file

        Returns:
            A list of package names
        """
        packages = []
        try:
            data = json.loads(content)

            # Extract dependencies
            dependencies = data.get("dependencies", {})
            dev_dependencies = data.get("devDependencies", {})

            # Add all dependencies
            packages.extend(list(dependencies.keys()))
            packages.extend(list(dev_dependencies.keys()))

        except json.JSONDecodeError:
            print("Error parsing package.json")

        return packages

    def parse_pyproject_toml(self, content: str) -> List[str]:
        """Parse a pyproject.toml file and extract package names

        Args:
            content: The content of the pyproject.toml file

        Returns:
            A list of package names
        """
        packages = []
        try:
            data = tomli.loads(content)

            # Extract dependencies from project section
            project_deps = data.get("project", {}).get("dependencies", [])
            if project_deps:
                for dep in project_deps:
                    # Extract package name (ignoring version specifiers)
                    match = re.match(r"^([\w\-\.]+)", dep)
                    if match:
                        package_name = match.group(1)
                        packages.append(package_name)

            # Extract dependencies from tool.poetry section
            poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            if poetry_deps:
                packages.extend(list(poetry_deps.keys()))

        except Exception as e:
            print(f"Error parsing pyproject.toml: {e}")

        return packages

    def parse_csproj(self, content: str) -> List[str]:
        """Parse a .csproj file and extract package names

        Args:
            content: The content of the .csproj file

        Returns:
            A list of package names
        """
        packages = []

        # Look for PackageReference elements
        package_refs = re.findall(r'<PackageReference\s+Include="([^"]+)"', content)
        packages.extend(package_refs)

        return packages

    def parse_dependency_file(self, content: str, file_type: str) -> List[str]:
        """Parse a dependency file and extract package names

        Args:
            content: The content of the dependency file
            file_type: The type of dependency file ('requirements.txt', 'package.json', etc.)

        Returns:
            A list of package names
        """
        if file_type == "requirements.txt":
            return self.parse_requirements_txt(content)
        elif file_type == "package.json":
            return self.parse_package_json(content)
        elif file_type == "pyproject.toml":
            return self.parse_pyproject_toml(content)
        elif file_type == ".csproj":
            return self.parse_csproj(content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
