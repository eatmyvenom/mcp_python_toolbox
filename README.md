# MCP Python Toolbox

A Model Context Protocol (MCP) server that provides a comprehensive set of tools for Python development, enabling AI assistants like Claude to effectively work with Python code and projects.

## Features

### File Operations (`FileOperations`)
- Safe file operations within a workspace directory
- Path validation to prevent unauthorized access outside workspace
- Read and write files with line-specific operations
- Create and delete files and directories
- List directory contents with detailed metadata (size, type, modification time)
- Automatic parent directory creation when writing files

### Code Analysis (`CodeAnalyzer`)
- Parse and analyze Python code structure using AST
- Extract detailed information about:
  - Import statements and their aliases
  - Function definitions with arguments and decorators
  - Class definitions with base classes and methods
  - Global variable assignments
- Format code using:
  - Black (default)
  - PEP8 (using autopep8)
- Comprehensive code linting using Pylint with detailed reports

### Project Management (`ProjectManager`)
- Create and manage virtual environments with pip support
- Flexible dependency management:
  - Install from requirements.txt
  - Install from pyproject.toml
  - Support for specific package versions
- Advanced dependency handling:
  - Check for version conflicts between packages
  - List all installed packages with versions
  - Update packages to specific versions
  - Generate requirements.txt from current environment

### Code Execution (`CodeExecutor`)
- Execute Python code in a controlled environment
- Uses project's virtual environment for consistent dependencies
- Temporary file management for code execution
- Capture stdout, stderr, and exit codes
- Support for custom working directories

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gianlucamazza/mcp_python_toolbox.git
cd mcp_python_toolbox
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Usage

### Starting the Server

```python
from mcp_python_toolbox import PythonToolboxServer

server = PythonToolboxServer(workspace_root="path/to/your/project")
server.setup()
server.run()
```

### Core Module Examples

#### File Operations
```python
from mcp_python_toolbox.core import FileOperations

file_ops = FileOperations(workspace_root="path/to/project")

# Read file contents
content = file_ops.read_file("src/example.py")
# Read specific lines
lines = file_ops.read_file("src/example.py", start_line=10, end_line=20)

# Write to file
file_ops.write_file("output.txt", "Hello, World!")
# Append to file
file_ops.write_file("log.txt", "New entry\n", mode='a')

# List directory contents
contents = file_ops.list_directory("src")
for item in contents:
    print(f"{item['name']} - {item['type']} - {item['size']} bytes")
```

#### Code Analysis
```python
from mcp_python_toolbox.core import CodeAnalyzer

analyzer = CodeAnalyzer(workspace_root="path/to/project")

# Analyze Python file structure
analysis = analyzer.parse_python_file("src/example.py")
print(f"Found {len(analysis['functions'])} functions")
print(f"Found {len(analysis['classes'])} classes")

# Format code
formatted = analyzer.format_code(code, style='black')

# Lint code
issues = analyzer.lint_code("src/example.py")
for issue in issues:
    print(f"Line {issue['line']}: {issue['message']}")
```

#### Project Management
```python
from mcp_python_toolbox.core import ProjectManager

pm = ProjectManager(workspace_root="path/to/project")

# Create virtual environment
pm.create_virtual_environment()

# Install dependencies
pm.install_dependencies()  # from requirements.txt or pyproject.toml
pm.install_dependencies("requirements-dev.txt")  # from specific file

# Check for conflicts
conflicts = pm.check_dependency_conflicts()
if conflicts:
    print("Found dependency conflicts:")
    for conflict in conflicts:
        print(f"{conflict['package']} requires {conflict['requires']}")

# Update packages
pm.update_package("requests")  # to latest
pm.update_package("flask", version="2.0.0")  # to specific version
```

#### Code Execution
```python
from mcp_python_toolbox.core import CodeExecutor

executor = CodeExecutor(workspace_root="path/to/project")

code = '''
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
'''

result = executor.execute_code(code)
print(f"Output: {result['stdout']}")
print(f"Errors: {result['stderr']}")
print(f"Exit code: {result['exit_code']}")
```

## Development

### Running Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/mcp_python_toolbox
```

### Linting

```bash
pylint src/mcp_python_toolbox
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the [Model Context Protocol](https://github.com/modelcontextprotocol/servers) project
- Built with modern Python development tools and best practices
- Uses industry-standard formatting (Black) and linting (Pylint) tools
