# mcp-servers/python-code-tools

[collect-files]

**Search:** ['mcp-servers/python-code-tools']
**Exclude:** ['.venv', 'node_modules', '.git', '__pycache__', '*.pyc', '*.ruff_cache']
**Include:** []
**Date:** 4/30/2025, 11:16:19 AM
**Files:** 25

=== File: mcp-servers/python-code-tools/.ruff.toml ===
line-length = 120

[format]
docstring-code-format = true
line-ending = "lf"
preview = true


=== File: mcp-servers/python-code-tools/README.md ===
# Python Code Tools MCP Server

This project implements a Model Context Protocol (MCP) server that provides code quality and maintenance tools for Python projects. It allows AI assistants and other MCP clients to perform code linting and fixing operations on both individual Python code snippets and entire project directories.

## Features

- **Code Linting with Auto-fix**: Uses Ruff, a fast Python linter written in Rust, to identify issues and automatically fix them where possible
- **Project-level Linting**: Analyze and fix code issues across entire Python projects or specific directories
- **Generic architecture** allows for easily swapping underlying tools in the future
- **Support for multiple transports**:
  - **stdio**: For direct subprocess communication
  - **SSE**: For HTTP-based communication
- **Convenient command-line interface** with dedicated scripts for each transport
- **Integration with AI assistants** like Claude and other MCP clients

## Requirements

- Python 3.10+
- MCP Python SDK (`pip install mcp>=1.6.0`)
- Ruff (`pip install ruff>=0.1.0`)

## Installation

### Using UV (Recommended)

1. Clone this repository
2. Create and activate a virtual environment:

```bash
# Create the virtual environment
uv venv

# Activate it (Unix/macOS)
source .venv/bin/activate
# Or on Windows
.venv\Scripts\activate
```

3. Install the package in development mode:

```bash
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Usage

### Command Line

The server provides several convenient entry points:

#### General Command

```bash
# Start with stdio transport
python-code-tools stdio

# Start with SSE transport
python-code-tools sse --host localhost --port 3001
```

#### Transport-Specific Commands

```bash
# Start with stdio transport
python-code-tools-stdio

# Start with SSE transport (with optional host/port args)
python-code-tools-sse
# or with custom host and port
python-code-tools-sse --host 0.0.0.0 --port 5000
```

### As a Python Module

```bash
# Using stdio transport
python -m python_code_tools stdio

# Using SSE transport
python -m python_code_tools sse --host localhost --port 3001
```

## Using with MCP Clients

See the [examples directory](./examples/README.md) for detailed examples of using the Python Code Tools MCP server with different clients and tools.

## Available Tools

### `lint_code`

Lints a Python code snippet and automatically fixes issues when possible.

**Parameters**:

- `code` (string, required): The Python code to lint
- `fix` (boolean, optional): Whether to automatically fix issues when possible (default: true)
- `config` (object, optional): Optional configuration settings for the linter

**Returns**:

- `fixed_code` (string): The code after linting and fixing
- `issues` (list): List of issues found in the code
- `fixed_count` (integer): Number of issues that were automatically fixed
- `remaining_count` (integer): Number of issues that could not be fixed

### `lint_project`

Lints a Python project directory and automatically fixes issues when possible.

**Parameters**:

- `project_path` (string, required): Path to the project directory to lint
- `file_patterns` (array of strings, optional): List of file patterns to include (e.g., `["*.py", "src/**/*.py"]`)
- `fix` (boolean, optional): Whether to automatically fix issues when possible (default: true)
- `config` (object, optional): Optional configuration settings for the linter

**Returns**:

- `issues` (array): List of issues found in the code
- `fixed_count` (integer): Number of issues that were automatically fixed
- `remaining_count` (integer): Number of issues that could not be fixed
- `modified_files` (array): List of files that were modified by the auto-fix
- `project_path` (string): The path to the project that was linted
- `has_ruff_config` (boolean): Whether the project has a ruff configuration file
- `files_summary` (object): Summary of issues grouped by file

## Extending the Server

### Adding New Linters

The server is designed to be extended with additional linters. To add a new linter:

1. Create a new class that extends the appropriate base class (`CodeLinter` or `ProjectLinter`) in a new file under `python_code_tools/linters/`
2. Implement the required methods (`lint_code()` or `lint_project()`)
3. Update the `create_mcp_server()` function in `server.py` to use your new linter

Example for a hypothetical alternative code linter:

```python
# python_code_tools/linters/alt_linter.py
from python_code_tools.linters.base import CodeLinter, CodeLintResult

class AltLinter(CodeLinter):
    """An alternative linter implementation."""

    def __init__(self, **kwargs):
        super().__init__(name="alt-linter", **kwargs)

    async def lint_code(self, code, fix=True, config=None):
        # Implement the linting logic using your tool of choice
        # ...
        return CodeLintResult(
            fixed_code=fixed_code,
            issues=issues,
            fixed_count=fixed_count,
            remaining_count=remaining_count
        )
```

Example for a hypothetical alternative project linter:

```python
# python_code_tools/linters/alt_project_linter.py
from python_code_tools.linters.base import ProjectLinter, ProjectLintResult

class AltProjectLinter(ProjectLinter):
    """An alternative project linter implementation."""

    def __init__(self, **kwargs):
        super().__init__(name="alt-project-linter", **kwargs)

    async def lint_project(self, project_path, file_patterns=None, fix=True, config=None):
        # Implement the project linting logic using your tool of choice
        # ...
        return ProjectLintResult(
            issues=issues,
            fixed_count=fixed_count,
            remaining_count=remaining_count,
            modified_files=modified_files,
            project_path=project_path,
            has_ruff_config=has_config,
            files_summary=files_summary
        )
```

### Adding New Tool Types

To add entirely new tool types beyond linting:

1. Implement the tool logic in an appropriate module
2. Add a new function to the `create_mcp_server()` function in `server.py`
3. Register it with the `@mcp.tool()` decorator


=== File: mcp-servers/python-code-tools/examples/README.md ===
# Python Code Tools Examples

This directory contains example code demonstrating how to use the Python Code Tools MCP server with different clients and tools.

## Example Files

### Code Linting Examples

- **stdio_client_example.py**: Shows how to use the `lint_code` tool with pydantic-ai's Agent class via stdio transport
- **direct_mcp_client_example.py**: Shows how to use the `lint_code` tool with a direct MCP client via stdio transport

### Project Linting Examples

- **project_linting_example.py**: Shows how to use the `lint_project` tool with pydantic-ai's Agent class
- **direct_project_linting_example.py**: Shows how to use the `lint_project` tool with a direct MCP client

## Usage Examples

### Linting a Code Snippet

Using pydantic-ai:

````python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# Sample Python code with some issues
SAMPLE_CODE = """
import sys
import os
import time  # unused import

def calculate_sum(a, b):
    result = a + b
    return result

# Line too long - will be flagged by ruff
long_text = "This is a very long line of text that exceeds the default line length limit in most Python style guides"
"""

async def main():
    # Set up the MCP server as a subprocess
    server = MCPServerStdio("python", args=["-m", "python_code_tools", "stdio"])

    # Create an agent with the MCP server
    agent = Agent("claude-3-7-sonnet-latest", mcp_servers=[server])

    # Use the MCP server in a conversation
    async with agent.run_mcp_servers():
        result = await agent.run(
            f"""
            Please analyze this Python code using the lint_code tool:

            ```python
            {SAMPLE_CODE}
            ```

            Explain what issues were found and what was fixed.
            """
        )

        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
````

Using a direct MCP client:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Sample code with issues
SAMPLE_CODE = """
import os
import time  # unused import

unused_var = 10
"""

async def main():
    # Create parameters for the stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "python_code_tools", "stdio"],
        env=dict(os.environ)
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        # Create a client session
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Call the lint_code tool
            result = await session.call_tool(
                "lint_code",
                {
                    "code": SAMPLE_CODE,
                    "fix": True
                }
            )

            # Process the result
            if result.content and len(result.content) > 0:
                first_content = result.content[0]
                if hasattr(first_content, "type") and first_content.type == "text":
                    lint_result = json.loads(first_content.text)
                    print(f"Fixed code:\n{lint_result['fixed_code']}")
```

### Linting a Project

Using pydantic-ai:

````python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

async def main():
    # Set up the MCP server as a subprocess
    server = MCPServerStdio("python", args=["-m", "python_code_tools", "stdio"])

    # Create an agent with the MCP server
    agent = Agent("claude-3-7-sonnet-latest", mcp_servers=[server])

    # Use the MCP server in a conversation
    async with agent.run_mcp_servers():
        result = await agent.run(
            """
            Please analyze the Python code in the project directory "/path/to/your/project"
            using the lint_project tool. Focus on the src directory with this command:

            ```
            lint_project(
                project_path="/path/to/your/project",
                file_patterns=["src/**/*.py"],
                fix=True
            )
            ```

            Explain what issues were found and what was fixed.
            """
        )

        print(result.output)
````

Using a direct MCP client:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create parameters for the stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "python_code_tools", "stdio"],
        env=dict(os.environ)
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        # Create a client session
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Call the lint_project tool
            result = await session.call_tool(
                "lint_project",
                {
                    "project_path": "/path/to/your/project",
                    "file_patterns": ["**/*.py"],
                    "fix": True
                }
            )

            # Process the result
            lint_result = json.loads(result.content[0].text)
            print(f"Issues found: {len(lint_result['issues'])}")
            print(f"Fixed issues: {lint_result['fixed_count']}")
```

## Additional Examples

Check the individual example files for more detailed usage patterns, including:

- Error handling
- Processing and displaying results
- Configuring tool parameters
- Working with different transport options


=== File: mcp-servers/python-code-tools/examples/direct_mcp_client_example.py ===
"""Example of using the Python Code Tools MCP server with a direct MCP client."""

import asyncio
import json
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Sample Python code with some issues
SAMPLE_CODE = """
import sys
import os
import time  # unused import

def calculate_sum(a, b):
    result = a + b
    unused_variable = 42  # unused variable
    return result

# Line too long - will be flagged by ruff
long_text = "This is a very long line of text that exceeds the default line length limit in most Python style guides"
"""  # noqa: E501


async def main():
    # Create parameters for the stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "python_code_tools", "stdio"],
        env=dict(os.environ),  # Convert _Environ to regular dict
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        # Create a client session
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("Connected to Python Code Tools MCP server")

            # List available tools
            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            print(f"Available tools: {tool_names}")

            # Call the lint_code tool
            result = await session.call_tool("lint_code", {"code": SAMPLE_CODE, "fix": True})

            # Display the results
            print("\nLint Results:")

            # Get the content text from the result
            if result.content and len(result.content) > 0:
                first_content = result.content[0]
                # Check if the content is TextContent (which has a text attribute)
                if hasattr(first_content, "type") and first_content.type == "text":
                    lint_result_text = first_content.text

                    # Print the raw response for debugging
                    print(f"Response debug: {lint_result_text}")

                    lint_result = json.loads(lint_result_text)

                    # Calculate total issues
                    fixed_count = lint_result.get("fixed_count", 0)
                    remaining_count = lint_result.get("remaining_count", 0)
                    total_issues = fixed_count + remaining_count

                    print(f"Total issues found: {total_issues}")
                    print(f"Fixed issues: {fixed_count}")
                    print(f"Remaining issues: {remaining_count}")

                    print("\nFixed code:")
                    print("------------")
                    print(lint_result["fixed_code"])
                    print("------------")

                    # Show remaining issues if any
                    if remaining_count > 0:
                        print("\nRemaining issues:")
                        for issue in lint_result["issues"]:
                            print(
                                f"- Line {issue['line']}, Col {issue['column']}: {issue['code']} - {issue['message']}"
                            )
                    else:
                        print("\nAll issues were fixed!")

                    # Compare with original code
                    if fixed_count > 0:
                        print("\nChanges made:")
                        # A simple diff would be ideal here, but for simplicity we'll just highlight
                        # that changes were made
                        print(f"- Fixed {fixed_count} issues with the code")

                        if lint_result["fixed_code"] != SAMPLE_CODE:
                            print("- Code was modified during fixing")
                        else:
                            print("- NOTE: Code appears unchanged despite fixes")
                else:
                    print(
                        "Unexpected content type: "
                        f"{first_content.type if hasattr(first_content, 'type') else 'unknown'}"
                    )
            else:
                print("No content in the response")


if __name__ == "__main__":
    asyncio.run(main())


=== File: mcp-servers/python-code-tools/examples/direct_project_linting_example.py ===
"""Example of using project linting with a direct MCP client."""

import asyncio
import json
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Use the current working directory (where you run the script from)
PROJECT_PATH = os.getcwd()


async def main():
    print(f"Using project path: {PROJECT_PATH}")

    # Create parameters for the stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "python_code_tools", "stdio"],
        env=dict(os.environ),  # Convert _Environ to regular dict
    )

    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        # Create a client session
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("Connected to Python Code Tools MCP server")

            # List available tools
            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            print(f"Available tools: {tool_names}")

            try:
                # Call the lint_project tool with improved error handling
                print(f"Calling lint_project tool for path: {PROJECT_PATH}")
                result = await session.call_tool(
                    "lint_project",
                    {
                        "project_path": PROJECT_PATH,
                        "file_patterns": ["**/*.py", "*.py"],  # Both top-level and nested Python files
                        "fix": True,
                    },
                )

                # Display the results
                print("\nProject Lint Results:")

                # First, check if we got any response at all
                if not result or not result.content:
                    print("Error: No response content received from the MCP server")
                    sys.exit(1)

                # Get the content text from the result with better error handling
                first_content = result.content[0] if result.content else None
                if not first_content:
                    print("Error: Empty response content")
                    sys.exit(1)

                # Check if the content is TextContent (which has a text attribute)
                if not hasattr(first_content, "type") or first_content.type != "text":
                    print(f"Error: Unexpected content type: {getattr(first_content, 'type', 'unknown')}")
                    sys.exit(1)

                lint_result_text = first_content.text
                if not lint_result_text:
                    print("Error: Empty text content in response")
                    sys.exit(1)

                # Print the raw response for debugging
                print(f"Response debug: {lint_result_text}")

                try:
                    lint_result = json.loads(lint_result_text)

                    # Check if we got an error from the server
                    if "error" in lint_result:
                        print(f"Server reported an error: {lint_result['error']}")
                        sys.exit(1)

                    project_path = lint_result.get("project_path", PROJECT_PATH)
                    print(f"Project path: {project_path}")

                    # Display configuration information
                    config_source = lint_result.get("config_source", "unknown")
                    print(f"Configuration source: {config_source}")

                    if "config_summary" in lint_result and "ruff" in lint_result["config_summary"]:
                        ruff_config = lint_result["config_summary"]["ruff"]
                        print("Ruff configuration:")
                        for key, value in ruff_config.items():
                            print(f"  {key}: {value}")

                    # Calculate total issues (sum of fixed and remaining)
                    fixed_count = lint_result.get("fixed_count", 0)
                    remaining_count = lint_result.get("remaining_count", 0)
                    total_issues_count = fixed_count + remaining_count

                    # Print issue counts
                    print(f"\nTotal issues found: {total_issues_count}")
                    print(f"Fixed issues: {fixed_count}")
                    print(f"Remaining issues: {remaining_count}")

                    # Display fixed issues
                    if lint_result.get("fixed_issues") and fixed_count > 0:
                        print("\nIssues that were fixed:")
                        fixed_issues_by_file = {}
                        for issue in lint_result.get("fixed_issues", []):
                            file_path = issue.get("file", "unknown")
                            if file_path not in fixed_issues_by_file:
                                fixed_issues_by_file[file_path] = []
                            fixed_issues_by_file[file_path].append(issue)

                        # Print fixed issues grouped by file
                        for file_path, issues in fixed_issues_by_file.items():
                            print(f"\nFile: {file_path}")
                            for issue in issues:
                                print(
                                    f"  Line {issue.get('line', '?')}, Col {issue.get('column', '?')}: "
                                    f"{issue.get('code', '?')} - {issue.get('message', 'Unknown issue')}"
                                )

                    # Display remaining issues
                    if remaining_count > 0:
                        print("\nRemaining issues:")
                        issues_by_file = {}
                        for issue in lint_result.get("issues", []):
                            file_path = issue.get("file", "unknown")
                            if file_path not in issues_by_file:
                                issues_by_file[file_path] = []
                            issues_by_file[file_path].append(issue)

                        # Print issues grouped by file
                        for file_path, issues in issues_by_file.items():
                            print(f"\nFile: {file_path}")
                            for issue in issues:
                                print(
                                    f"  Line {issue.get('line', '?')}, Col {issue.get('column', '?')}: "
                                    f"{issue.get('code', '?')} - {issue.get('message', 'Unknown issue')}"
                                )

                    # Print file summary
                    if "files_summary" in lint_result and lint_result["files_summary"]:
                        print("\nFiles Summary:")
                        for file_path, summary in lint_result["files_summary"].items():
                            print(f"- {file_path}: {summary.get('total_issues', 0)} remaining issues")
                            if "issue_types" in summary:
                                print("  Issue types:")
                                for code, count in summary["issue_types"].items():
                                    print(f"    {code}: {count}")

                    # Print modified files
                    if "modified_files" in lint_result and lint_result["modified_files"]:
                        print("\nModified files:")
                        for file in lint_result["modified_files"]:
                            print(f"- {file}")
                    else:
                        print("\nNo files were modified.")

                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Raw response text: {lint_result_text}")
            except Exception as e:
                print(f"Error during linting: {e}", file=sys.stderr)
                import traceback

                traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())


=== File: mcp-servers/python-code-tools/examples/project_linting_example.py ===
"""Example of project-based linting with Python Code Tools MCP server."""

import asyncio
import os

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio


async def main():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Using project path: {current_dir}")

    # Set up the MCP server as a subprocess
    server = MCPServerStdio("python", args=["-m", "python_code_tools", "stdio"])

    # Create an agent with the MCP server
    agent = Agent("claude-3-7-sonnet-latest", mcp_servers=[server])

    # Use the MCP server in a conversation
    async with agent.run_mcp_servers():
        print("Connected to Python Code Tools MCP server via stdio")

        # Example conversation with actual project path
        result = await agent.run(
            f"""
            Please analyze the Python code in this project directory using the lint_project tool.

            Run this command:
            ```
            lint_project(
                project_path="{current_dir}",
                file_patterns=["**/*.py"],
                fix=True
            )
            ```

            After running the lint_project tool, provide a detailed analysis that includes:
            1. How many total issues were found (fixed + remaining)
            2. What types of issues were fixed automatically
            3. What issues remain and need manual attention
            4. Which files were modified

            Please be specific about the exact issues found and fixed.
            """
        )

        print("\nAgent's response:")
        print(result.output)


if __name__ == "__main__":
    asyncio.run(main())


=== File: mcp-servers/python-code-tools/examples/stdio_client_example.py ===
"""Example client using stdio transport with the Python Code Tools MCP server."""

import asyncio

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# Sample Python code with some issues
SAMPLE_CODE = """
import sys
import os
import time  # unused import

def calculate_sum(a, b):
    result = a + b
    unused_variable = 42  # unused variable
    return result

# Line too long - will be flagged by ruff
long_text = "This is a very long line of text that exceeds the default line length limit in most Python style guides like PEP 8 which recommends 79 characters, but if the configuration is set to 120, it will be ignored unless the line continues for more than 120 characters like this one now does at over 300 characters."
"""


async def main():
    # Set up the MCP server as a subprocess
    server = MCPServerStdio("python", args=["-m", "python_code_tools", "stdio"])

    # Create an agent with the MCP server
    agent = Agent("claude-3-7-sonnet-latest", mcp_servers=[server])

    # Use the MCP server in a conversation
    async with agent.run_mcp_servers():
        print("Connected to Python Code Tools MCP server via stdio")

        # Example conversation
        result = await agent.run(
            f"""
            Please analyze this Python code using the lint_code tool:

            ```python
            {SAMPLE_CODE}
            ```

            After running the lint_code tool, provide a detailed analysis that includes:
            1. How many total issues were found (fixed + remaining)
            2. What types of issues were fixed automatically
            3. What issues remain and need manual attention
            4. Show the fixed code and explain what was changed

            Please be specific about the exact issues found and fixed.

            Show the updated code with comments explaining the changes made.
            """
        )

        print("\nAgent's response:")
        print(result.output)


if __name__ == "__main__":
    asyncio.run(main())


=== File: mcp-servers/python-code-tools/pyproject.toml ===
[project]
name = "python-code-tools"
version = "0.1.0"
description = "MCP server providing Python code quality tools"
authors = [{ name = "Brian Krabach" }]
license = "MIT"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.7.2,<3.0.0",
    "mcp>=1.6.0",
    "ruff>=0.1.0",
    "tomli>=2.2.1",
]

[dependency-groups]
dev = ["pytest>=7.0.0", "black>=23.0.0", "mypy>=1.0.0"]

[project.scripts]
# Main entry point
python-code-tools = "python_code_tools.cli:main"

# Convenience scripts for specific transports
python-code-tools-stdio = "python_code_tools.cli:stdio_main"
python-code-tools-sse = "python_code_tools.cli:sse_main"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"


=== File: mcp-servers/python-code-tools/pyrightconfig.json ===
{
  "extraPaths": ["./"],
  "typeCheckingMode": "basic"
}


=== File: mcp-servers/python-code-tools/python_code_tools/__init__.py ===
"""Python Code Tools MCP server package."""

__version__ = "0.1.0"


=== File: mcp-servers/python-code-tools/python_code_tools/__main__.py ===
"""Entry point for running the package as a module."""

from python_code_tools.cli import main

if __name__ == "__main__":
    main()


=== File: mcp-servers/python-code-tools/python_code_tools/cli.py ===
"""Command-line interface for the Python Code Tools MCP server."""

import argparse
import sys
from typing import List, Optional

from python_code_tools.server import create_mcp_server


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        argv: Command line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(description="Python Code Tools MCP Server")
    parser.add_argument(
        "transport",
        choices=["stdio", "sse"],
        help="Transport protocol to use (stdio or sse)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for SSE server (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="Port for SSE server (default: 3001)",
    )

    args = parser.parse_args(argv)

    try:
        # Create the MCP server with the specified settings
        mcp = create_mcp_server(host=args.host, port=args.port)

        # Run the server with the appropriate transport
        print(f"Starting Python Code Tools MCP server with {args.transport} transport")
        if args.transport == "sse":
            print(f"Server URL: http://{args.host}:{args.port}/sse")

        mcp.run(transport=args.transport)
        return 0
    except KeyboardInterrupt:
        print("Server stopped", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def stdio_main() -> int:
    """Convenience entry point for stdio transport.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    return main(["stdio"])


def sse_main() -> int:
    """Convenience entry point for SSE transport.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Get any command-line arguments after the script name
    argv = sys.argv[1:]

    # Pre-populate the 'transport' argument
    all_args = ["sse"] + argv

    return main(all_args)


if __name__ == "__main__":
    sys.exit(main())


=== File: mcp-servers/python-code-tools/python_code_tools/linters/__init__.py ===
"""Module imports for the linters package."""

from python_code_tools.linters.base import (
    BaseLinter,
    CodeLinter,
    CodeLintResult,
    LintResult,
    ProjectLinter,
    ProjectLintResult,
)
from python_code_tools.linters.ruff import RuffLinter, RuffProjectLinter

__all__ = [
    # Base classes
    "BaseLinter",
    "CodeLinter",
    "ProjectLinter",
    "LintResult",
    "CodeLintResult",
    "ProjectLintResult",
    # Implementations
    "RuffLinter",
    "RuffProjectLinter",
]


=== File: mcp-servers/python-code-tools/python_code_tools/linters/base.py ===
"""Base interfaces for code linters."""

import abc
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

"""Result models for linting operations."""


class LintResult(BaseModel):
    """Base result model for linting."""

    issues: List[Dict[str, Any]] = Field(default_factory=list, description="List of issues found in the code")
    fixed_count: int = Field(0, description="Number of issues that were automatically fixed")
    remaining_count: int = Field(0, description="Number of issues that could not be fixed")


class CodeLintResult(LintResult):
    """Result model for code snippet linting."""

    fixed_code: str = Field(..., description="The code after linting and fixing (if enabled)")


class ProjectLintResult(LintResult):
    """Result model for project linting."""

    modified_files: List[str] = Field(
        default_factory=list, description="List of files that were modified by auto-fixes"
    )
    project_path: str = Field(..., description="Path to the project directory that was linted")
    has_ruff_config: bool = Field(False, description="Whether the project has a ruff configuration file")
    # Configuration information
    config_source: Optional[str] = Field(
        "default", description="Source of the configuration (none, pyproject.toml, ruff.toml, etc.)"
    )
    config_summary: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Summary of configuration from different sources"
    )
    files_summary: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Summary of issues by file")
    # New fields for tracking fixed issues
    fixed_issues: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of issues that were fixed during linting"
    )
    fixed_issues_summary: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Summary of fixed issues grouped by file"
    )


class BaseLinter(abc.ABC):
    """Abstract base class for all linters."""

    def __init__(self, name: str, **kwargs):
        """Initialize the linter.

        Args:
            name: The name of the linter
            **kwargs: Additional configuration options
        """
        self.name = name
        self.config = kwargs


class CodeLinter(BaseLinter):
    """Abstract base class for code snippet linters."""

    @abc.abstractmethod
    async def lint_code(self, code: str, fix: bool = True, config: Optional[Dict[str, Any]] = None) -> CodeLintResult:
        """Lint the provided code snippet and return the results.

        Args:
            code: The Python code to lint
            fix: Whether to automatically fix issues when possible
            config: Optional configuration settings for the linter

        Returns:
            A CodeLintResult object containing the fixed code and issue details
        """
        pass


class ProjectLinter(BaseLinter):
    """Abstract base class for project directory linters."""

    @abc.abstractmethod
    async def lint_project(
        self,
        project_path: str,
        file_patterns: Optional[List[str]] = None,
        fix: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ) -> ProjectLintResult:
        """Lint a project directory and return the results.

        Args:
            project_path: Path to the project directory
            file_patterns: Optional list of file patterns to include
            fix: Whether to automatically fix issues when possible
            config: Optional configuration settings for the linter

        Returns:
            A ProjectLintResult object containing issues found and fix details
        """
        pass


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/__init__.py ===
from python_code_tools.linters.ruff.project import RuffProjectLinter
from python_code_tools.linters.ruff.snippet import RuffLinter

__all__ = [
    # Base classes
    "RuffLinter",
    "RuffProjectLinter",
]


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/config.py ===
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import tomli

default_config = {
    "select": "E,F,W,I",
    "ignore": [],
    "line-length": 100,
}


async def get_config(user_config: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], str]:
    """Get the preferred configuration for Ruff.

    Args:
        user_config: Optional user-provided configuration

    Returns:
        Tuple of (configuration settings, source description)
    """
    print(f"Getting Ruff configuration. User config provided: {user_config is not None}")

    # Priority order:
    # 1. User-provided configuration
    # 2. Project configuration from .ruff.toml
    # 3. Project configuration from pyproject.toml
    # 4. Default configuration

    if user_config:
        # User config has highest priority - use ONLY this
        print("Using user-provided configuration")
        return user_config, "user"
    else:
        # Project config has second priority - use ONLY this
        project_config, source = await read_project_config(Path.cwd())
        if project_config:
            print(f"Using project configuration from {source}")
            return project_config, source
        else:
            # Default config has lowest priority - use ONLY this
            print("No project configuration found, using default configuration")
            return default_config, "default"


async def read_project_config(path: Path) -> Tuple[Dict[str, Any], str]:
    """Read Ruff configuration from files within the project directory.

    Args:
        path: Project directory path

    Returns:
        Tuple of (configuration settings, source description)
    """
    config = {}
    source = "none"

    print(f"Looking for Ruff configuration files in {path}")

    # Check for .ruff.toml (highest priority)
    ruff_toml_path = path / ".ruff.toml"
    if ruff_toml_path.exists():
        print(f"Found .ruff.toml at {ruff_toml_path}")
        try:
            with open(ruff_toml_path, "rb") as f:
                ruff_config = tomli.load(f)
                if "lint" in ruff_config:
                    config.update(ruff_config["lint"])
                else:
                    config.update(ruff_config)
                # Return immediately since this is highest priority
                return config, ".ruff.toml"
        except Exception as e:
            print(f"Error reading .ruff.toml: {e}")

    # Check for pyproject.toml (lower priority)
    pyproject_path = path / "pyproject.toml"
    if pyproject_path.exists():
        print(f"Found pyproject.toml at {pyproject_path}")
        try:
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomli.load(f)
                # Extract Ruff configuration
                if "tool" in pyproject_data and "ruff" in pyproject_data["tool"]:
                    ruff_config = pyproject_data["tool"]["ruff"]
                    if "lint" in ruff_config:
                        config.update(ruff_config["lint"])
                    else:
                        config.update(ruff_config)
                    return config, "pyproject.toml"
        except Exception as e:
            print(f"Error reading pyproject.toml: {e}")

    return config, source


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/project.py ===
from pathlib import Path

from python_code_tools.linters.base import ProjectLinter, ProjectLintResult
from python_code_tools.linters.ruff.config import get_config
from python_code_tools.linters.ruff.reporter import create_issues_summary, identify_fixed_issues, print_final_report
from python_code_tools.linters.ruff.runner import get_python_files, run_ruff_check, run_ruff_fix
from python_code_tools.linters.ruff.utils import (
    convert_issue_paths_to_relative,
    convert_summary_paths_to_relative,
    get_file_hashes,
    get_modified_files,
)


class RuffProjectLinter(ProjectLinter):
    def __init__(self, **kwargs) -> None:
        super().__init__(name="ruff-project", **kwargs)

    async def lint_project(self, project_path: str, file_patterns=None, fix=True, config=None) -> ProjectLintResult:
        path = Path(project_path)
        effective_config, config_source = await get_config(config)
        has_ruff_config = config_source != "default"

        # Properly structure the config summary as a dictionary of dictionaries
        config_summary = {"ruff": {}}
        for key, value in effective_config.items():
            config_summary["ruff"][key] = value

        py_files = await get_python_files(path, file_patterns)
        if not py_files:
            return ProjectLintResult(
                issues=[],
                fixed_count=0,
                remaining_count=0,
                modified_files=[],
                project_path=str(path),
                has_ruff_config=has_ruff_config,
                config_source=config_source,
                config_summary=config_summary,
                files_summary={},
                fixed_issues=[],
                fixed_issues_summary={},
            )

        # Initial scan - find all issues before fixing
        initial_issues = await run_ruff_check(path, py_files, effective_config)
        total_issues_count = len(initial_issues)

        # Create a copy of initial issues for tracking
        remaining_issues_list = initial_issues.copy()
        fixed_issues_list = []
        modified_files = []

        # Only run the fixer if requested and there are issues to fix
        if fix and initial_issues:
            before_hashes = await get_file_hashes(path, py_files)

            # Run the auto-fix
            await run_ruff_fix(path, py_files, effective_config)

            # Check what's changed
            after_hashes = await get_file_hashes(path, py_files)
            modified_files = get_modified_files(before_hashes, after_hashes)

            # Get remaining issues after fixing
            remaining_issues_list = await run_ruff_check(path, py_files, effective_config)

            # Identify which issues were actually fixed
            fixed_issues_list = identify_fixed_issues(initial_issues, remaining_issues_list)

        # Calculate counts
        fixed_issues_count = len(fixed_issues_list)
        remaining_issues_count = len(remaining_issues_list)

        # Debug info
        print(f"DEBUG: Initial issues found: {total_issues_count}")
        print(f"DEBUG: Issues fixed: {fixed_issues_count}")
        print(f"DEBUG: Issues remaining: {remaining_issues_count}")

        # Sanity check
        expected_total = fixed_issues_count + remaining_issues_count
        if total_issues_count != expected_total:
            print(
                f"WARNING: Issue count mismatch - initial: {total_issues_count}, "
                f"calculated total: {expected_total} (fixed: {fixed_issues_count} + remaining: {remaining_issues_count})"
            )

            # Adjust total to match reality if needed
            if expected_total > total_issues_count:
                total_issues_count = expected_total
                print(f"Adjusted total issues count to {total_issues_count}")

        # Convert all paths to relative
        str_project_path = str(path)
        relative_remaining_issues = convert_issue_paths_to_relative(remaining_issues_list, str_project_path)
        relative_fixed_issues = convert_issue_paths_to_relative(fixed_issues_list, str_project_path)

        # Create summaries with relative paths
        fixed_summary = create_issues_summary(relative_fixed_issues, "fixed_types", "total_fixed")
        files_summary = create_issues_summary(relative_remaining_issues, "issue_types", "total_issues")

        # Convert all paths in summaries to relative
        relative_fixed_summary = convert_summary_paths_to_relative(fixed_summary, str_project_path)
        relative_files_summary = convert_summary_paths_to_relative(files_summary, str_project_path)

        print_final_report(
            total_issues_count,
            fixed_issues_count,
            remaining_issues_count,
            modified_files,
            relative_fixed_issues,
            relative_remaining_issues,
            relative_files_summary,
            relative_fixed_summary,
        )

        # Return the results with the correct counts and relative paths
        return ProjectLintResult(
            issues=relative_remaining_issues,
            fixed_count=fixed_issues_count,
            remaining_count=remaining_issues_count,
            modified_files=modified_files,
            project_path=str(path),
            has_ruff_config=has_ruff_config,
            config_source=config_source,
            config_summary=config_summary,
            files_summary=relative_files_summary,
            fixed_issues=relative_fixed_issues,
            fixed_issues_summary=relative_fixed_summary,
        )


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/reporter.py ===
from typing import Any, Dict, List


def create_issues_summary(issues: List[Dict[str, Any]], types_key: str, total_key: str) -> Dict[str, Dict[str, Any]]:
    """Create a summary of issues by file.

    Args:
        issues: List of issues to summarize
        types_key: Key to use for the types dictionary
        total_key: Key to use for the total count

    Returns:
        Dictionary mapping file paths to issue summaries
    """
    summary = {}
    for issue in issues:
        file_path = issue.get("file", "unknown")
        if file_path not in summary:
            summary[file_path] = {total_key: 0, types_key: {}}

        summary[file_path][total_key] += 1

        code = issue.get("code", "unknown")
        if code not in summary[file_path][types_key]:
            summary[file_path][types_key][code] = 0
        summary[file_path][types_key][code] += 1

    return summary


def identify_fixed_issues(
    initial_issues: List[Dict[str, Any]], remaining_issues: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Identify which issues were fixed by comparing initial and remaining issues.

    Args:
        initial_issues: List of issues found before fixing
        remaining_issues: List of issues found after fixing

    Returns:
        List of issues that were fixed
    """
    # Create a map of remaining issues for quick lookup
    # Use a more robust signature that takes into account file path and issue code
    # This fixes the problem where line numbers change due to code deletion
    remaining_map = {}
    for issue in remaining_issues:
        file_path = issue.get("file", "")
        code = issue.get("code", "")
        message = issue.get("message", "")

        # Create a composite key that identifies the issue type and content
        # but not its location (since that can change)
        key = f"{file_path}:{code}:{message}"

        if key not in remaining_map:
            remaining_map[key] = 0
        remaining_map[key] += 1

    # Find issues that were truly fixed (not just moved)
    fixed_issues = []
    for issue in initial_issues:
        file_path = issue.get("file", "")
        code = issue.get("code", "")
        message = issue.get("message", "")

        key = f"{file_path}:{code}:{message}"

        if key not in remaining_map or remaining_map[key] == 0:
            # This issue was completely fixed
            fixed_issues.append(issue)
        else:
            # This issue still exists, decrement the count
            remaining_map[key] -= 1

    return fixed_issues


def print_final_report(
    total_issue_count: int,
    fixed_count: int,
    remaining_count: int,
    modified_files: List[str],
    fixed_issues: List[Dict[str, Any]],
    remaining_issues: List[Dict[str, Any]],
    files_summary: Dict[str, Any],
    fixed_issues_summary: Dict[str, Any],
) -> None:
    """Print a comprehensive final report.

    Args:
        total_issue_count: Total number of issues found
        fixed_count: Number of issues fixed
        remaining_count: Number of issues remaining
        modified_files: List of files that were modified
        fixed_issues: List of issues that were fixed
        remaining_issues: List of issues remaining
        files_summary: Summary of remaining issues by file
        fixed_issues_summary: Summary of fixed issues by file
    """
    # Report on issues found, fixed, and remaining
    print(f"\nTotal issues found: {total_issue_count}")
    print(f"Fixed issues: {fixed_count}")
    print(f"Remaining issues: {remaining_count}")

    # Report on fixed issues
    if fixed_count > 0:
        print("\nFixed issues:")
        for issue in fixed_issues:
            file_path = issue.get("file", "unknown")
            code = issue.get("code", "unknown")
            message = issue.get("message", "unknown")
            line = issue.get("line", 0)
            column = issue.get("column", 0)
            print(f"- {file_path} (Line {line}, Col {column}): {code} - {message}")

        # Print summary by file
        if fixed_issues_summary:
            print("\nFixed issues by file:")
            for file_path, summary in fixed_issues_summary.items():
                print(f"- {file_path}: {summary.get('total_fixed', 0)} issues")
                if "fixed_types" in summary:
                    for code, count in summary["fixed_types"].items():
                        print(f"    {code}: {count}")

    # Report on remaining issues
    if remaining_count > 0:
        print("\nRemaining issues:")
        for issue in remaining_issues:
            file_path = issue.get("file", "unknown")
            code = issue.get("code", "unknown")
            message = issue.get("message", "unknown")
            line = issue.get("line", 0)
            column = issue.get("column", 0)
            print(f"- {file_path} (Line {line}, Col {column}): {code} - {message}")

        # Print summary by file
        if files_summary:
            print("\nRemaining issues by file:")
            for file_path, summary in files_summary.items():
                print(f"- {file_path}: {summary.get('total_issues', 0)} issues")
                if "issue_types" in summary:
                    for code, count in summary["issue_types"].items():
                        print(f"    {code}: {count}")

    # Report on modified files
    if modified_files:
        print("\nModified files:")
        for file in modified_files:
            print(f"- {file}")
    else:
        print("\nNo files were modified.")
        if fixed_count > 0:
            print("Note: Some issues were fixed in memory but changes were not written to disk.")
            print("This can happen with certain types of issues that the linter can detect but not automatically fix.")


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/runner.py ===
import asyncio
import glob
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


async def get_python_files(path: Path, patterns: Optional[List[str]] = None) -> List[str]:
    """Get a list of Python files to lint.

    Args:
        path: Project directory path
        file_patterns: Optional list of file patterns to include

    Returns:
        List of Python file paths
    """
    print(f"Looking for Python files in {path}")
    py_files = []

    if not patterns:
        patterns = ["**/*.py"]  # Default to all Python files
        print(f"No patterns provided, using default: {patterns}")
    else:
        print(f"Using provided patterns: {patterns}")

    # Use Python's glob to find files matching patterns
    for pattern in patterns:
        # Handle both absolute and relative paths in patterns
        if os.path.isabs(pattern):
            glob_pattern = pattern
        else:
            glob_pattern = os.path.join(str(path), pattern)

        print(f"Searching with glob pattern: {glob_pattern}")

        # Use glob.glob with recursive=True for ** patterns
        if "**" in pattern:
            matched_files = glob.glob(glob_pattern, recursive=True)
        else:
            matched_files = glob.glob(glob_pattern)

        # Convert to relative paths
        for file in matched_files:
            if file.endswith(".py"):
                try:
                    rel_path = os.path.relpath(file, str(path))
                    # Skip .venv directory and __pycache__
                    if not rel_path.startswith((".venv", "__pycache__")):
                        py_files.append(rel_path)
                except ValueError:
                    # This can happen if the file is on a different drive (Windows)
                    print(f"Skipping file not relative to project path: {file}")

    # Remove duplicates while preserving order
    unique_files = []
    seen = set()
    for file in py_files:
        if file not in seen:
            unique_files.append(file)
            seen.add(file)

    print(f"Found {len(unique_files)} Python files to lint")
    if len(unique_files) < 10:  # Only print all files if there are few
        print(f"Files to lint: {unique_files}")
    else:
        print(f"First 5 files: {unique_files[:5]}")

    return unique_files


async def run_ruff_check(path: Path, py_files: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run Ruff in check mode (no fixing).

    Args:
        path: Project directory path
        py_files: List of Python files to check
        config: Configuration to use

    Returns:
        List of issues found
    """
    # Make sure we have files to check
    if not py_files:
        print("No Python files found to check")
        return []

    # Verify the files exist
    existing_files = []
    for file_path in py_files:
        full_path = path / file_path
        if full_path.exists():
            existing_files.append(file_path)

    if not existing_files:
        print(f"None of the specified Python files exist in {path}")
        return []

    py_files = existing_files
    print(f"Found {len(py_files)} Python files to check")

    # Build the command
    cmd = ["ruff", "check", "--output-format=json"]

    # Add configuration options
    if "select" in config:
        select_value = config["select"]
        if isinstance(select_value, list):
            select_str = ",".join(select_value)
        else:
            select_str = str(select_value)
        cmd.extend(["--select", select_str])

    if "ignore" in config and config["ignore"]:
        if isinstance(config["ignore"], list):
            ignore_str = ",".join(config["ignore"])
        else:
            ignore_str = str(config["ignore"])
        cmd.extend(["--ignore", ignore_str])

    if "line-length" in config:
        cmd.extend(["--line-length", str(config["line-length"])])

    # Add files to check
    cmd.extend(py_files)

    try:
        # Now run the actual check command
        print(f"Running ruff command: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(*cmd, cwd=str(path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_bytes, stderr_bytes = await proc.communicate()

        stdout_text = stdout_bytes.decode().strip() if stdout_bytes else ""
        stderr_text = stderr_bytes.decode().strip() if stderr_bytes else ""

        if proc.returncode != 0 and stderr_text:
            print(f"Ruff command failed with exit code {proc.returncode}: {stderr_text}")
            # Continue processing anyway - non-zero could just mean issues were found

        issues = []

        # Only try to parse JSON if we actually have output
        if stdout_text:
            try:
                json_data = json.loads(stdout_text)
                print(f"Ruff found {len(json_data)} issues")

                for item in json_data:
                    try:
                        # Get location data with proper null handling
                        location = item.get("location") or {}
                        row = location.get("row", 0) if isinstance(location, dict) else 0
                        column = location.get("column", 0) if isinstance(location, dict) else 0

                        # Get fix data with proper null handling
                        fix_data = item.get("fix") or {}
                        fix_applicable = (
                            fix_data.get("applicability", "") == "applicable" if isinstance(fix_data, dict) else False
                        )

                        # Create issue object
                        issues.append({
                            "file": item.get("filename", ""),
                            "line": row,
                            "column": column,
                            "code": item.get("code", ""),
                            "message": item.get("message", ""),
                            "fix_available": fix_applicable,
                        })
                    except Exception as e:
                        print(f"Error processing ruff issue: {e}")
                        # Skip issues we can't parse properly
                        continue
            except json.JSONDecodeError as e:
                print(f"Failed to parse Ruff JSON output: {e}")
                print(f"Raw output: {stdout_text[:200]}...")  # Print first 200 chars
                return []

        return issues

    except Exception as e:
        print(f"Error running Ruff check: {e}")
        return []


async def run_ruff_fix(path: Path, py_files: List[str], config: Dict[str, Any]) -> bool:
    """Run Ruff in fix mode.

    Args:
        path: Project directory path
        py_files: List of Python files to fix
        config: Configuration to use

    Returns:
        True if fixing succeeded, False otherwise
    """
    # Make sure we have files to check
    if not py_files:
        return False

    # Verify the files exist
    existing_files = []
    for file_path in py_files:
        full_path = path / file_path
        if full_path.exists():
            existing_files.append(file_path)

    if not existing_files:
        return False

    py_files = existing_files

    # Build the command
    cmd = ["ruff", "check", "--fix"]

    # Add configuration options
    if "select" in config:
        select_value = config["select"]
        if isinstance(select_value, list):
            select_str = ",".join(select_value)
        else:
            select_str = str(select_value)
        cmd.extend(["--select", select_str])

    if "ignore" in config and config["ignore"]:
        if isinstance(config["ignore"], list):
            ignore_str = ",".join(config["ignore"])
        else:
            ignore_str = str(config["ignore"])
        cmd.extend(["--ignore", ignore_str])

    if "line-length" in config:
        cmd.extend(["--line-length", str(config["line-length"])])

    # Add files to fix
    cmd.extend(py_files)

    try:
        proc = await asyncio.create_subprocess_exec(*cmd, cwd=str(path), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await proc.communicate()

        return proc.returncode == 0

    except Exception:
        return False


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/snippet.py ===
"""Ruff linter implementation for single code snippets."""

import asyncio
import json
import subprocess
from typing import Any, Dict, List, Optional

from python_code_tools.linters.base import CodeLinter, CodeLintResult
from python_code_tools.utils.temp_file import cleanup_temp_file, create_temp_file


class RuffLinter(CodeLinter):
    """Code linter implementation using Ruff."""

    def __init__(self, **kwargs) -> None:
        """Initialize the Ruff linter.

        Args:
            **kwargs: Additional configuration options for Ruff
        """
        super().__init__(name="ruff", **kwargs)

    async def lint_code(self, code: str, fix: bool = True, config: Optional[Dict[str, Any]] = None) -> CodeLintResult:
        """Lint code using Ruff and return the results.

        Args:
            code: The Python code to lint
            fix: Whether to automatically fix issues when possible
            config: Optional configuration settings for Ruff

        Returns:
            A CodeLintResult object containing the fixed code and issue details
        """
        temp_file, file_path = create_temp_file(code, suffix=".py")

        try:
            # First, get original issues (before fixing)
            # Convert Path to string for _get_issues
            initial_issues = await self._get_issues(str(file_path), config)
            initial_count = len(initial_issues)

            print(f"Initial scan found {initial_count} issues")

            # Keep a copy of the original code
            with open(file_path, "r") as f:
                original_code = f.read()

            # Only try to fix if requested and there are issues
            fixed_code = original_code
            remaining_issues = initial_issues
            if fix and initial_count > 0:
                # Run ruff with --fix flag - convert Path to string
                fix_success = await self._run_fix(str(file_path), config)

                if fix_success:
                    # Read the fixed code
                    with open(file_path, "r") as f:
                        fixed_code = f.read()

                    # Get remaining issues after fixing - convert Path to string
                    remaining_issues = await self._get_issues(str(file_path), config)

                print(f"After fixing, {len(remaining_issues)} issues remain")

            # Calculate fixed count
            fixed_count = initial_count - len(remaining_issues)
            remaining_count = len(remaining_issues)

            # Debug info
            print(f"DEBUG: Initial issues: {initial_count}")
            print(f"DEBUG: Fixed issues: {fixed_count}")
            print(f"DEBUG: Remaining issues: {remaining_count}")

            return CodeLintResult(
                fixed_code=fixed_code,
                issues=remaining_issues,
                fixed_count=fixed_count,
                remaining_count=remaining_count,
            )

        finally:
            # Clean up temporary file
            cleanup_temp_file(temp_file, file_path)

    async def _get_issues(self, file_path: str, config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get issues from a file using ruff check with JSON output.

        Args:
            file_path: Path to the Python file
            config: Optional configuration settings for Ruff

        Returns:
            List of issues found
        """
        # Build the ruff command for check only (no fixing)
        cmd = ["ruff", "check", file_path, "--output-format=json"]

        # Add config options if provided
        if config:
            for key, value in config.items():
                if key == "select":
                    value_str = ",".join(value) if isinstance(value, list) else value
                    cmd.extend(["--select", value_str])
                elif key == "ignore":
                    value_str = ",".join(value) if isinstance(value, list) else value
                    cmd.extend(["--ignore", value_str])
                elif key == "line-length":
                    cmd.extend(["--line-length", str(value)])

        try:
            # Run the command
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            stdout_text = stdout.decode().strip() if stdout else ""
            stderr_text = stderr.decode().strip() if stderr else ""

            if stderr_text:
                print(f"WARNING: Ruff stderr: {stderr_text}")

            issues = []

            # Parse JSON output if available
            if stdout_text:
                try:
                    data = json.loads(stdout_text)

                    for item in data:
                        # Extract location data
                        location = item.get("location") or {}
                        row = location.get("row", 0) if isinstance(location, dict) else 0
                        column = location.get("column", 0) if isinstance(location, dict) else 0

                        # Extract fix data
                        fix_data = item.get("fix") or {}
                        fix_applicable = (
                            fix_data.get("applicability", "") == "applicable" if isinstance(fix_data, dict) else False
                        )

                        # Create issue object
                        issues.append({
                            "line": row,
                            "column": column,
                            "code": item.get("code", ""),
                            "message": item.get("message", ""),
                            "fix_available": fix_applicable,
                        })
                except json.JSONDecodeError as e:
                    print(f"ERROR: Failed to parse JSON output: {e}")
                    print(f"Raw output: {stdout_text[:200]}...")

            return issues

        except Exception as e:
            print(f"ERROR: Failed to run ruff check: {e}")
            return []

    async def _run_fix(self, file_path: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """Run ruff with --fix flag to automatically fix issues.

        Args:
            file_path: Path to the Python file
            config: Optional configuration settings for Ruff

        Returns:
            True if fixing succeeded, False otherwise
        """
        # Build the ruff command for fixing
        cmd = ["ruff", "check", file_path, "--fix"]

        # Add config options if provided
        if config:
            for key, value in config.items():
                if key == "select":
                    value_str = ",".join(value) if isinstance(value, list) else value
                    cmd.extend(["--select", value_str])
                elif key == "ignore":
                    value_str = ",".join(value) if isinstance(value, list) else value
                    cmd.extend(["--ignore", value_str])
                elif key == "line-length":
                    cmd.extend(["--line-length", str(value)])

        try:
            # Run the command
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await proc.communicate()

            stderr_text = stderr.decode().strip() if stderr else ""
            if stderr_text:
                print(f"WARNING: Ruff fix stderr: {stderr_text}")

            return proc.returncode == 0

        except Exception as e:
            print(f"ERROR: Failed to run ruff fix: {e}")
            return False


=== File: mcp-servers/python-code-tools/python_code_tools/linters/ruff/utils.py ===
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List


async def get_file_hashes(path: Path, file_paths: List[str]) -> Dict[str, str]:
    """Get MD5 hashes of files for change detection.

    Args:
        path: Project directory path
        file_paths: List of file paths

    Returns:
        Dictionary mapping file paths to MD5 hashes
    """

    hashes = {}

    for file_path in file_paths:
        abs_path = path / file_path
        try:
            with open(abs_path, "rb") as f:
                content = f.read()
                hashes[file_path] = hashlib.md5(content).hexdigest()
        except Exception:
            # Skip files we can't read
            pass

    return hashes


def get_modified_files(before_hashes: Dict[str, str], after_hashes: Dict[str, str]) -> List[str]:
    """Determine which files were modified by comparing hashes.

    Args:
        before_hashes: File hashes before modification
        after_hashes: File hashes after modification

    Returns:
        List of modified file paths
    """
    modified_files = []

    for file_path, before_hash in before_hashes.items():
        if file_path in after_hashes:
            after_hash = after_hashes[file_path]
            if before_hash != after_hash:
                modified_files.append(file_path)

    return modified_files


def make_path_relative(file_path: str, project_path: str) -> str:
    """Convert absolute paths to project-relative paths.

    Args:
        file_path: Absolute or relative file path
        project_path: Base project path

    Returns:
        Path relative to the project directory
    """
    try:
        # If it's already a relative path, return it
        if not os.path.isabs(file_path):
            return file_path

        # Convert absolute path to relative path
        rel_path = os.path.relpath(file_path, project_path)

        # Remove leading ./ if present
        if rel_path.startswith("./"):
            rel_path = rel_path[2:]

        return rel_path
    except Exception:
        # If any error occurs, return the original path
        return file_path


def convert_issue_paths_to_relative(issues: List[Dict[str, Any]], project_path: str) -> List[Dict[str, Any]]:
    """Convert all file paths in issues to be relative to the project path.

    Args:
        issues: List of issue dictionaries
        project_path: Base project path

    Returns:
        List of issues with relative paths
    """
    relative_issues = []
    for issue in issues:
        # Create a copy of the issue
        relative_issue = issue.copy()

        # Convert the file path if present
        if "file" in relative_issue:
            relative_issue["file"] = make_path_relative(relative_issue["file"], project_path)

        relative_issues.append(relative_issue)

    return relative_issues


def convert_summary_paths_to_relative(
    summary: Dict[str, Dict[str, Any]], project_path: str
) -> Dict[str, Dict[str, Any]]:
    """Convert all file paths in a summary dictionary to be relative to the project path.

    Args:
        summary: Dictionary of file paths to summaries
        project_path: Base project path

    Returns:
        Summary dictionary with relative paths
    """
    relative_summary = {}
    for file_path, data in summary.items():
        relative_path = make_path_relative(file_path, project_path)
        relative_summary[relative_path] = data

    return relative_summary


=== File: mcp-servers/python-code-tools/python_code_tools/server.py ===
"""MCP server implementation for Python code tools."""

import argparse
import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from python_code_tools.linters import RuffLinter, RuffProjectLinter


def create_mcp_server(host: str = "localhost", port: int = 3001) -> FastMCP:
    """Create and configure the MCP server.

    Args:
        host: The hostname for the SSE server
        port: The port for the SSE server

    Returns:
        A configured FastMCP server instance
    """
    # Initialize FastMCP server with settings for SSE transport
    mcp = FastMCP("Python Code Tools", host=host, port=port, debug=False, log_level="INFO")

    # Initialize the linters
    ruff_linter = RuffLinter()
    project_linter = RuffProjectLinter()

    @mcp.tool()
    async def lint_code(code: str, fix: bool = True, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Lint Python code and optionally fix issues.

        Args:
            code: The Python code to lint
            fix: Whether to automatically fix issues when possible
            config: Optional configuration settings for the linter

        Returns:
            A dictionary containing the fixed code, issues found, and fix counts
        """
        result = await ruff_linter.lint_code(code, fix, config)
        return result.model_dump()

    @mcp.tool()
    async def lint_project(
        project_path: str,
        file_patterns: Optional[List[str]] = None,
        fix: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Lint a Python project directory and optionally fix issues.

        Args:
            project_path: Path to the project directory
            file_patterns: Optional list of file patterns to include (e.g., ["*.py", "src/**/*.py"])
            fix: Whether to automatically fix issues when possible
            config: Optional configuration settings for the linter

        Returns:
            A dictionary containing issues found, fix counts, and modified files
        """
        try:
            result = await project_linter.lint_project(project_path, file_patterns, fix, config)
            # Explicitly convert to dict to ensure proper serialization
            return result.model_dump()
        except Exception as e:
            # Return a structured error response instead of letting the exception bubble up
            return {
                "error": str(e),
                "project_path": project_path,
                "issues": [],
                "fixed_count": 0,
                "remaining_count": 0,
                "modified_files": [],
            }

    return mcp


def main() -> int:
    """Main entry point for the server CLI.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = argparse.ArgumentParser(description="Python Code Tools MCP Server")
    parser.add_argument(
        "transport",
        choices=["stdio", "sse"],
        help="Transport protocol to use (stdio or sse)",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for SSE server (default: localhost)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="Port for SSE server (default: 3001)",
    )

    args = parser.parse_args()

    try:
        # Create the MCP server with the specified settings
        mcp = create_mcp_server(host=args.host, port=args.port)

        # Run the server with the appropriate transport
        print(f"Starting Python Code Tools MCP server with {args.transport} transport")
        if args.transport == "sse":
            print(f"Server URL: http://{args.host}:{args.port}/sse")

        mcp.run(transport=args.transport)
        return 0
    except KeyboardInterrupt:
        print("Server stopped", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


# For importing in other modules
mcp = create_mcp_server()

if __name__ == "__main__":
    sys.exit(main())


=== File: mcp-servers/python-code-tools/python_code_tools/utils/__init__.py ===
"""Utility functions for Python Code Tools."""

from python_code_tools.utils.temp_file import cleanup_temp_file, create_temp_file

__all__ = ["create_temp_file", "cleanup_temp_file"]


=== File: mcp-servers/python-code-tools/python_code_tools/utils/temp_file.py ===
"""Temporary file handling utilities."""

import os
import tempfile
from pathlib import Path
from typing import IO, Any, Tuple


def create_temp_file(content: str, suffix: str = ".txt") -> Tuple[IO[Any], Path]:
    """Create a temporary file with the given content.

    Args:
        content: The content to write to the file
        suffix: The file suffix/extension

    Returns:
        A tuple containing the temporary file object and the path to the file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    file_path = Path(temp_file.name)

    with open(file_path, "w") as f:
        f.write(content)

    return temp_file, file_path


def cleanup_temp_file(temp_file: IO[Any], file_path: Path) -> None:
    """Clean up a temporary file.

    Args:
        temp_file: The temporary file object
        file_path: The path to the file
    """
    temp_file.close()
    if os.path.exists(file_path):
        os.unlink(file_path)


=== File: mcp-servers/python-code-tools/uv.lock ===
version = 1
requires-python = ">=3.10"

[[package]]
name = "annotated-types"
version = "0.7.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/ee/67/531ea369ba64dcff5ec9c3402f9f51bf748cec26dde048a2f973a4eea7f5/annotated_types-0.7.0.tar.gz", hash = "sha256:aff07c09a53a08bc8cfccb9c85b05f1aa9a2a6f23728d790723543408344ce89", size = 16081 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/78/b6/6307fbef88d9b5ee7421e68d78a9f162e0da4900bc5f5793f6d3d0e34fb8/annotated_types-0.7.0-py3-none-any.whl", hash = "sha256:1f02e8b43a8fbbc3f3e0d4f0f4bfc8131bcb4eebe8849b8e5c773f3a1c582a53", size = 13643 },
]

[[package]]
name = "anyio"
version = "4.9.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "exceptiongroup", marker = "python_full_version < '3.11'" },
    { name = "idna" },
    { name = "sniffio" },
    { name = "typing-extensions", marker = "python_full_version < '3.13'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/95/7d/4c1bd541d4dffa1b52bd83fb8527089e097a106fc90b467a7313b105f840/anyio-4.9.0.tar.gz", hash = "sha256:673c0c244e15788651a4ff38710fea9675823028a6f08a5eda409e0c9840a028", size = 190949 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/a1/ee/48ca1a7c89ffec8b6a0c5d02b89c305671d5ffd8d3c94acf8b8c408575bb/anyio-4.9.0-py3-none-any.whl", hash = "sha256:9f76d541cad6e36af7beb62e978876f3b41e3e04f2c1fbf0884604c0a9c4d93c", size = 100916 },
]

[[package]]
name = "black"
version = "25.1.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "click" },
    { name = "mypy-extensions" },
    { name = "packaging" },
    { name = "pathspec" },
    { name = "platformdirs" },
    { name = "tomli", marker = "python_full_version < '3.11'" },
    { name = "typing-extensions", marker = "python_full_version < '3.11'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/94/49/26a7b0f3f35da4b5a65f081943b7bcd22d7002f5f0fb8098ec1ff21cb6ef/black-25.1.0.tar.gz", hash = "sha256:33496d5cd1222ad73391352b4ae8da15253c5de89b93a80b3e2c8d9a19ec2666", size = 649449 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/4d/3b/4ba3f93ac8d90410423fdd31d7541ada9bcee1df32fb90d26de41ed40e1d/black-25.1.0-cp310-cp310-macosx_10_9_x86_64.whl", hash = "sha256:759e7ec1e050a15f89b770cefbf91ebee8917aac5c20483bc2d80a6c3a04df32", size = 1629419 },
    { url = "https://files.pythonhosted.org/packages/b4/02/0bde0485146a8a5e694daed47561785e8b77a0466ccc1f3e485d5ef2925e/black-25.1.0-cp310-cp310-macosx_11_0_arm64.whl", hash = "sha256:0e519ecf93120f34243e6b0054db49c00a35f84f195d5bce7e9f5cfc578fc2da", size = 1461080 },
    { url = "https://files.pythonhosted.org/packages/52/0e/abdf75183c830eaca7589144ff96d49bce73d7ec6ad12ef62185cc0f79a2/black-25.1.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:055e59b198df7ac0b7efca5ad7ff2516bca343276c466be72eb04a3bcc1f82d7", size = 1766886 },
    { url = "https://files.pythonhosted.org/packages/dc/a6/97d8bb65b1d8a41f8a6736222ba0a334db7b7b77b8023ab4568288f23973/black-25.1.0-cp310-cp310-win_amd64.whl", hash = "sha256:db8ea9917d6f8fc62abd90d944920d95e73c83a5ee3383493e35d271aca872e9", size = 1419404 },
    { url = "https://files.pythonhosted.org/packages/7e/4f/87f596aca05c3ce5b94b8663dbfe242a12843caaa82dd3f85f1ffdc3f177/black-25.1.0-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:a39337598244de4bae26475f77dda852ea00a93bd4c728e09eacd827ec929df0", size = 1614372 },
    { url = "https://files.pythonhosted.org/packages/e7/d0/2c34c36190b741c59c901e56ab7f6e54dad8df05a6272a9747ecef7c6036/black-25.1.0-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:96c1c7cd856bba8e20094e36e0f948718dc688dba4a9d78c3adde52b9e6c2299", size = 1442865 },
    { url = "https://files.pythonhosted.org/packages/21/d4/7518c72262468430ead45cf22bd86c883a6448b9eb43672765d69a8f1248/black-25.1.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:bce2e264d59c91e52d8000d507eb20a9aca4a778731a08cfff7e5ac4a4bb7096", size = 1749699 },
    { url = "https://files.pythonhosted.org/packages/58/db/4f5beb989b547f79096e035c4981ceb36ac2b552d0ac5f2620e941501c99/black-25.1.0-cp311-cp311-win_amd64.whl", hash = "sha256:172b1dbff09f86ce6f4eb8edf9dede08b1fce58ba194c87d7a4f1a5aa2f5b3c2", size = 1428028 },
    { url = "https://files.pythonhosted.org/packages/83/71/3fe4741df7adf015ad8dfa082dd36c94ca86bb21f25608eb247b4afb15b2/black-25.1.0-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:4b60580e829091e6f9238c848ea6750efed72140b91b048770b64e74fe04908b", size = 1650988 },
    { url = "https://files.pythonhosted.org/packages/13/f3/89aac8a83d73937ccd39bbe8fc6ac8860c11cfa0af5b1c96d081facac844/black-25.1.0-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:1e2978f6df243b155ef5fa7e558a43037c3079093ed5d10fd84c43900f2d8ecc", size = 1453985 },
    { url = "https://files.pythonhosted.org/packages/6f/22/b99efca33f1f3a1d2552c714b1e1b5ae92efac6c43e790ad539a163d1754/black-25.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:3b48735872ec535027d979e8dcb20bf4f70b5ac75a8ea99f127c106a7d7aba9f", size = 1783816 },
    { url = "https://files.pythonhosted.org/packages/18/7e/a27c3ad3822b6f2e0e00d63d58ff6299a99a5b3aee69fa77cd4b0076b261/black-25.1.0-cp312-cp312-win_amd64.whl", hash = "sha256:ea0213189960bda9cf99be5b8c8ce66bb054af5e9e861249cd23471bd7b0b3ba", size = 1440860 },
    { url = "https://files.pythonhosted.org/packages/98/87/0edf98916640efa5d0696e1abb0a8357b52e69e82322628f25bf14d263d1/black-25.1.0-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:8f0b18a02996a836cc9c9c78e5babec10930862827b1b724ddfe98ccf2f2fe4f", size = 1650673 },
    { url = "https://files.pythonhosted.org/packages/52/e5/f7bf17207cf87fa6e9b676576749c6b6ed0d70f179a3d812c997870291c3/black-25.1.0-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:afebb7098bfbc70037a053b91ae8437c3857482d3a690fefc03e9ff7aa9a5fd3", size = 1453190 },
    { url = "https://files.pythonhosted.org/packages/e3/ee/adda3d46d4a9120772fae6de454c8495603c37c4c3b9c60f25b1ab6401fe/black-25.1.0-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:030b9759066a4ee5e5aca28c3c77f9c64789cdd4de8ac1df642c40b708be6171", size = 1782926 },
    { url = "https://files.pythonhosted.org/packages/cc/64/94eb5f45dcb997d2082f097a3944cfc7fe87e071907f677e80788a2d7b7a/black-25.1.0-cp313-cp313-win_amd64.whl", hash = "sha256:a22f402b410566e2d1c950708c77ebf5ebd5d0d88a6a2e87c86d9fb48afa0d18", size = 1442613 },
    { url = "https://files.pythonhosted.org/packages/09/71/54e999902aed72baf26bca0d50781b01838251a462612966e9fc4891eadd/black-25.1.0-py3-none-any.whl", hash = "sha256:95e8176dae143ba9097f351d174fdaf0ccd29efb414b362ae3fd72bf0f710717", size = 207646 },
]

[[package]]
name = "certifi"
version = "2025.1.31"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/1c/ab/c9f1e32b7b1bf505bf26f0ef697775960db7932abeb7b516de930ba2705f/certifi-2025.1.31.tar.gz", hash = "sha256:3d5da6925056f6f18f119200434a4780a94263f10d1c21d032a6f6b2baa20651", size = 167577 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/38/fc/bce832fd4fd99766c04d1ee0eead6b0ec6486fb100ae5e74c1d91292b982/certifi-2025.1.31-py3-none-any.whl", hash = "sha256:ca78db4565a652026a4db2bcdf68f2fb589ea80d0be70e03929ed730746b84fe", size = 166393 },
]

[[package]]
name = "click"
version = "8.1.8"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "colorama", marker = "sys_platform == 'win32'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/b9/2e/0090cbf739cee7d23781ad4b89a9894a41538e4fcf4c31dcdd705b78eb8b/click-8.1.8.tar.gz", hash = "sha256:ed53c9d8990d83c2a27deae68e4ee337473f6330c040a31d4225c9574d16096a", size = 226593 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/7e/d4/7ebdbd03970677812aac39c869717059dbb71a4cfc033ca6e5221787892c/click-8.1.8-py3-none-any.whl", hash = "sha256:63c132bbbed01578a06712a2d1f497bb62d9c1c0d329b7903a866228027263b2", size = 98188 },
]

[[package]]
name = "colorama"
version = "0.4.6"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz", hash = "sha256:08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44", size = 27697 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl", hash = "sha256:4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6", size = 25335 },
]

[[package]]
name = "exceptiongroup"
version = "1.2.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/09/35/2495c4ac46b980e4ca1f6ad6db102322ef3ad2410b79fdde159a4b0f3b92/exceptiongroup-1.2.2.tar.gz", hash = "sha256:47c2edf7c6738fafb49fd34290706d1a1a2f4d1c6df275526b62cbb4aa5393cc", size = 28883 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/02/cc/b7e31358aac6ed1ef2bb790a9746ac2c69bcb3c8588b41616914eb106eaf/exceptiongroup-1.2.2-py3-none-any.whl", hash = "sha256:3111b9d131c238bec2f8f516e123e14ba243563fb135d3fe885990585aa7795b", size = 16453 },
]

[[package]]
name = "h11"
version = "0.14.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f5/38/3af3d3633a34a3316095b39c8e8fb4853a28a536e55d347bd8d8e9a14b03/h11-0.14.0.tar.gz", hash = "sha256:8f19fbbe99e72420ff35c00b27a34cb9937e902a8b810e2c88300c6f0a3b699d", size = 100418 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/95/04/ff642e65ad6b90db43e668d70ffb6736436c7ce41fcc549f4e9472234127/h11-0.14.0-py3-none-any.whl", hash = "sha256:e3fe4ac4b851c468cc8363d500db52c2ead036020723024a109d37346efaa761", size = 58259 },
]

[[package]]
name = "httpcore"
version = "1.0.8"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "certifi" },
    { name = "h11" },
]
sdist = { url = "https://files.pythonhosted.org/packages/9f/45/ad3e1b4d448f22c0cff4f5692f5ed0666658578e358b8d58a19846048059/httpcore-1.0.8.tar.gz", hash = "sha256:86e94505ed24ea06514883fd44d2bc02d90e77e7979c8eb71b90f41d364a1bad", size = 85385 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/18/8d/f052b1e336bb2c1fc7ed1aaed898aa570c0b61a09707b108979d9fc6e308/httpcore-1.0.8-py3-none-any.whl", hash = "sha256:5254cf149bcb5f75e9d1b2b9f729ea4a4b883d1ad7379fc632b727cec23674be", size = 78732 },
]

[[package]]
name = "httpx"
version = "0.28.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
    { name = "certifi" },
    { name = "httpcore" },
    { name = "idna" },
]
sdist = { url = "https://files.pythonhosted.org/packages/b1/df/48c586a5fe32a0f01324ee087459e112ebb7224f646c0b5023f5e79e9956/httpx-0.28.1.tar.gz", hash = "sha256:75e98c5f16b0f35b567856f597f06ff2270a374470a5c2392242528e3e3e42fc", size = 141406 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/2a/39/e50c7c3a983047577ee07d2a9e53faf5a69493943ec3f6a384bdc792deb2/httpx-0.28.1-py3-none-any.whl", hash = "sha256:d909fcccc110f8c7faf814ca82a9a4d816bc5a6dbfea25d6591d6985b8ba59ad", size = 73517 },
]

[[package]]
name = "httpx-sse"
version = "0.4.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/4c/60/8f4281fa9bbf3c8034fd54c0e7412e66edbab6bc74c4996bd616f8d0406e/httpx-sse-0.4.0.tar.gz", hash = "sha256:1e81a3a3070ce322add1d3529ed42eb5f70817f45ed6ec915ab753f961139721", size = 12624 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/e1/9b/a181f281f65d776426002f330c31849b86b31fc9d848db62e16f03ff739f/httpx_sse-0.4.0-py3-none-any.whl", hash = "sha256:f329af6eae57eaa2bdfd962b42524764af68075ea87370a2de920af5341e318f", size = 7819 },
]

[[package]]
name = "idna"
version = "3.10"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f1/70/7703c29685631f5a7590aa73f1f1d3fa9a380e654b86af429e0934a32f7d/idna-3.10.tar.gz", hash = "sha256:12f65c9b470abda6dc35cf8e63cc574b1c52b11df2c86030af0ac09b01b13ea9", size = 190490 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/76/c6/c88e154df9c4e1a2a66ccf0005a88dfb2650c1dffb6f5ce603dfbd452ce3/idna-3.10-py3-none-any.whl", hash = "sha256:946d195a0d259cbba61165e88e65941f16e9b36ea6ddb97f00452bae8b1287d3", size = 70442 },
]

[[package]]
name = "iniconfig"
version = "2.1.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f2/97/ebf4da567aa6827c909642694d71c9fcf53e5b504f2d96afea02718862f3/iniconfig-2.1.0.tar.gz", hash = "sha256:3abbd2e30b36733fee78f9c7f7308f2d0050e88f0087fd25c2645f63c773e1c7", size = 4793 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/2c/e1/e6716421ea10d38022b952c159d5161ca1193197fb744506875fbb87ea7b/iniconfig-2.1.0-py3-none-any.whl", hash = "sha256:9deba5723312380e77435581c6bf4935c94cbfab9b1ed33ef8d238ea168eb760", size = 6050 },
]

[[package]]
name = "mcp"
version = "1.6.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
    { name = "httpx" },
    { name = "httpx-sse" },
    { name = "pydantic" },
    { name = "pydantic-settings" },
    { name = "sse-starlette" },
    { name = "starlette" },
    { name = "uvicorn" },
]
sdist = { url = "https://files.pythonhosted.org/packages/95/d2/f587cb965a56e992634bebc8611c5b579af912b74e04eb9164bd49527d21/mcp-1.6.0.tar.gz", hash = "sha256:d9324876de2c5637369f43161cd71eebfd803df5a95e46225cab8d280e366723", size = 200031 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/10/30/20a7f33b0b884a9d14dd3aa94ff1ac9da1479fe2ad66dd9e2736075d2506/mcp-1.6.0-py3-none-any.whl", hash = "sha256:7bd24c6ea042dbec44c754f100984d186620d8b841ec30f1b19eda9b93a634d0", size = 76077 },
]

[[package]]
name = "mypy"
version = "1.15.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "mypy-extensions" },
    { name = "tomli", marker = "python_full_version < '3.11'" },
    { name = "typing-extensions" },
]
sdist = { url = "https://files.pythonhosted.org/packages/ce/43/d5e49a86afa64bd3839ea0d5b9c7103487007d728e1293f52525d6d5486a/mypy-1.15.0.tar.gz", hash = "sha256:404534629d51d3efea5c800ee7c42b72a6554d6c400e6a79eafe15d11341fd43", size = 3239717 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/68/f8/65a7ce8d0e09b6329ad0c8d40330d100ea343bd4dd04c4f8ae26462d0a17/mypy-1.15.0-cp310-cp310-macosx_10_9_x86_64.whl", hash = "sha256:979e4e1a006511dacf628e36fadfecbcc0160a8af6ca7dad2f5025529e082c13", size = 10738433 },
    { url = "https://files.pythonhosted.org/packages/b4/95/9c0ecb8eacfe048583706249439ff52105b3f552ea9c4024166c03224270/mypy-1.15.0-cp310-cp310-macosx_11_0_arm64.whl", hash = "sha256:c4bb0e1bd29f7d34efcccd71cf733580191e9a264a2202b0239da95984c5b559", size = 9861472 },
    { url = "https://files.pythonhosted.org/packages/84/09/9ec95e982e282e20c0d5407bc65031dfd0f0f8ecc66b69538296e06fcbee/mypy-1.15.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:be68172e9fd9ad8fb876c6389f16d1c1b5f100ffa779f77b1fb2176fcc9ab95b", size = 11611424 },
    { url = "https://files.pythonhosted.org/packages/78/13/f7d14e55865036a1e6a0a69580c240f43bc1f37407fe9235c0d4ef25ffb0/mypy-1.15.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:c7be1e46525adfa0d97681432ee9fcd61a3964c2446795714699a998d193f1a3", size = 12365450 },
    { url = "https://files.pythonhosted.org/packages/48/e1/301a73852d40c241e915ac6d7bcd7fedd47d519246db2d7b86b9d7e7a0cb/mypy-1.15.0-cp310-cp310-musllinux_1_2_x86_64.whl", hash = "sha256:2e2c2e6d3593f6451b18588848e66260ff62ccca522dd231cd4dd59b0160668b", size = 12551765 },
    { url = "https://files.pythonhosted.org/packages/77/ba/c37bc323ae5fe7f3f15a28e06ab012cd0b7552886118943e90b15af31195/mypy-1.15.0-cp310-cp310-win_amd64.whl", hash = "sha256:6983aae8b2f653e098edb77f893f7b6aca69f6cffb19b2cc7443f23cce5f4828", size = 9274701 },
    { url = "https://files.pythonhosted.org/packages/03/bc/f6339726c627bd7ca1ce0fa56c9ae2d0144604a319e0e339bdadafbbb599/mypy-1.15.0-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:2922d42e16d6de288022e5ca321cd0618b238cfc5570e0263e5ba0a77dbef56f", size = 10662338 },
    { url = "https://files.pythonhosted.org/packages/e2/90/8dcf506ca1a09b0d17555cc00cd69aee402c203911410136cd716559efe7/mypy-1.15.0-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:2ee2d57e01a7c35de00f4634ba1bbf015185b219e4dc5909e281016df43f5ee5", size = 9787540 },
    { url = "https://files.pythonhosted.org/packages/05/05/a10f9479681e5da09ef2f9426f650d7b550d4bafbef683b69aad1ba87457/mypy-1.15.0-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:973500e0774b85d9689715feeffcc980193086551110fd678ebe1f4342fb7c5e", size = 11538051 },
    { url = "https://files.pythonhosted.org/packages/e9/9a/1f7d18b30edd57441a6411fcbc0c6869448d1a4bacbaee60656ac0fc29c8/mypy-1.15.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:5a95fb17c13e29d2d5195869262f8125dfdb5c134dc8d9a9d0aecf7525b10c2c", size = 12286751 },
    { url = "https://files.pythonhosted.org/packages/72/af/19ff499b6f1dafcaf56f9881f7a965ac2f474f69f6f618b5175b044299f5/mypy-1.15.0-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:1905f494bfd7d85a23a88c5d97840888a7bd516545fc5aaedff0267e0bb54e2f", size = 12421783 },
    { url = "https://files.pythonhosted.org/packages/96/39/11b57431a1f686c1aed54bf794870efe0f6aeca11aca281a0bd87a5ad42c/mypy-1.15.0-cp311-cp311-win_amd64.whl", hash = "sha256:c9817fa23833ff189db061e6d2eff49b2f3b6ed9856b4a0a73046e41932d744f", size = 9265618 },
    { url = "https://files.pythonhosted.org/packages/98/3a/03c74331c5eb8bd025734e04c9840532226775c47a2c39b56a0c8d4f128d/mypy-1.15.0-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:aea39e0583d05124836ea645f412e88a5c7d0fd77a6d694b60d9b6b2d9f184fd", size = 10793981 },
    { url = "https://files.pythonhosted.org/packages/f0/1a/41759b18f2cfd568848a37c89030aeb03534411eef981df621d8fad08a1d/mypy-1.15.0-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:2f2147ab812b75e5b5499b01ade1f4a81489a147c01585cda36019102538615f", size = 9749175 },
    { url = "https://files.pythonhosted.org/packages/12/7e/873481abf1ef112c582db832740f4c11b2bfa510e829d6da29b0ab8c3f9c/mypy-1.15.0-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:ce436f4c6d218a070048ed6a44c0bbb10cd2cc5e272b29e7845f6a2f57ee4464", size = 11455675 },
    { url = "https://files.pythonhosted.org/packages/b3/d0/92ae4cde706923a2d3f2d6c39629134063ff64b9dedca9c1388363da072d/mypy-1.15.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:8023ff13985661b50a5928fc7a5ca15f3d1affb41e5f0a9952cb68ef090b31ee", size = 12410020 },
    { url = "https://files.pythonhosted.org/packages/46/8b/df49974b337cce35f828ba6fda228152d6db45fed4c86ba56ffe442434fd/mypy-1.15.0-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:1124a18bc11a6a62887e3e137f37f53fbae476dc36c185d549d4f837a2a6a14e", size = 12498582 },
    { url = "https://files.pythonhosted.org/packages/13/50/da5203fcf6c53044a0b699939f31075c45ae8a4cadf538a9069b165c1050/mypy-1.15.0-cp312-cp312-win_amd64.whl", hash = "sha256:171a9ca9a40cd1843abeca0e405bc1940cd9b305eaeea2dda769ba096932bb22", size = 9366614 },
    { url = "https://files.pythonhosted.org/packages/6a/9b/fd2e05d6ffff24d912f150b87db9e364fa8282045c875654ce7e32fffa66/mypy-1.15.0-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:93faf3fdb04768d44bf28693293f3904bbb555d076b781ad2530214ee53e3445", size = 10788592 },
    { url = "https://files.pythonhosted.org/packages/74/37/b246d711c28a03ead1fd906bbc7106659aed7c089d55fe40dd58db812628/mypy-1.15.0-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:811aeccadfb730024c5d3e326b2fbe9249bb7413553f15499a4050f7c30e801d", size = 9753611 },
    { url = "https://files.pythonhosted.org/packages/a6/ac/395808a92e10cfdac8003c3de9a2ab6dc7cde6c0d2a4df3df1b815ffd067/mypy-1.15.0-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.manylinux_2_28_aarch64.whl", hash = "sha256:98b7b9b9aedb65fe628c62a6dc57f6d5088ef2dfca37903a7d9ee374d03acca5", size = 11438443 },
    { url = "https://files.pythonhosted.org/packages/d2/8b/801aa06445d2de3895f59e476f38f3f8d610ef5d6908245f07d002676cbf/mypy-1.15.0-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl", hash = "sha256:c43a7682e24b4f576d93072216bf56eeff70d9140241f9edec0c104d0c515036", size = 12402541 },
    { url = "https://files.pythonhosted.org/packages/c7/67/5a4268782eb77344cc613a4cf23540928e41f018a9a1ec4c6882baf20ab8/mypy-1.15.0-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:baefc32840a9f00babd83251560e0ae1573e2f9d1b067719479bfb0e987c6357", size = 12494348 },
    { url = "https://files.pythonhosted.org/packages/83/3e/57bb447f7bbbfaabf1712d96f9df142624a386d98fb026a761532526057e/mypy-1.15.0-cp313-cp313-win_amd64.whl", hash = "sha256:b9378e2c00146c44793c98b8d5a61039a048e31f429fb0eb546d93f4b000bedf", size = 9373648 },
    { url = "https://files.pythonhosted.org/packages/09/4e/a7d65c7322c510de2c409ff3828b03354a7c43f5a8ed458a7a131b41c7b9/mypy-1.15.0-py3-none-any.whl", hash = "sha256:5469affef548bd1895d86d3bf10ce2b44e33d86923c29e4d675b3e323437ea3e", size = 2221777 },
]

[[package]]
name = "mypy-extensions"
version = "1.0.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/98/a4/1ab47638b92648243faf97a5aeb6ea83059cc3624972ab6b8d2316078d3f/mypy_extensions-1.0.0.tar.gz", hash = "sha256:75dbf8955dc00442a438fc4d0666508a9a97b6bd41aa2f0ffe9d2f2725af0782", size = 4433 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/2a/e2/5d3f6ada4297caebe1a2add3b126fe800c96f56dbe5d1988a2cbe0b267aa/mypy_extensions-1.0.0-py3-none-any.whl", hash = "sha256:4392f6c0eb8a5668a69e23d168ffa70f0be9ccfd32b5cc2d26a34ae5b844552d", size = 4695 },
]

[[package]]
name = "packaging"
version = "25.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/a1/d4/1fc4078c65507b51b96ca8f8c3ba19e6a61c8253c72794544580a7b6c24d/packaging-25.0.tar.gz", hash = "sha256:d443872c98d677bf60f6a1f2f8c1cb748e8fe762d2bf9d3148b5599295b0fc4f", size = 165727 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/20/12/38679034af332785aac8774540895e234f4d07f7545804097de4b666afd8/packaging-25.0-py3-none-any.whl", hash = "sha256:29572ef2b1f17581046b3a2227d5c611fb25ec70ca1ba8554b24b0e69331a484", size = 66469 },
]

[[package]]
name = "pathspec"
version = "0.12.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/ca/bc/f35b8446f4531a7cb215605d100cd88b7ac6f44ab3fc94870c120ab3adbf/pathspec-0.12.1.tar.gz", hash = "sha256:a482d51503a1ab33b1c67a6c3813a26953dbdc71c31dacaef9a838c4e29f5712", size = 51043 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/cc/20/ff623b09d963f88bfde16306a54e12ee5ea43e9b597108672ff3a408aad6/pathspec-0.12.1-py3-none-any.whl", hash = "sha256:a0d503e138a4c123b27490a4f7beda6a01c6f288df0e4a8b79c7eb0dc7b4cc08", size = 31191 },
]

[[package]]
name = "platformdirs"
version = "4.3.7"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/b6/2d/7d512a3913d60623e7eb945c6d1b4f0bddf1d0b7ada5225274c87e5b53d1/platformdirs-4.3.7.tar.gz", hash = "sha256:eb437d586b6a0986388f0d6f74aa0cde27b48d0e3d66843640bfb6bdcdb6e351", size = 21291 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/6d/45/59578566b3275b8fd9157885918fcd0c4d74162928a5310926887b856a51/platformdirs-4.3.7-py3-none-any.whl", hash = "sha256:a03875334331946f13c549dbd8f4bac7a13a50a895a0eb1e8c6a8ace80d40a94", size = 18499 },
]

[[package]]
name = "pluggy"
version = "1.5.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/96/2d/02d4312c973c6050a18b314a5ad0b3210edb65a906f868e31c111dede4a6/pluggy-1.5.0.tar.gz", hash = "sha256:2cffa88e94fdc978c4c574f15f9e59b7f4201d439195c3715ca9e2486f1d0cf1", size = 67955 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/88/5f/e351af9a41f866ac3f1fac4ca0613908d9a41741cfcf2228f4ad853b697d/pluggy-1.5.0-py3-none-any.whl", hash = "sha256:44e1ad92c8ca002de6377e165f3e0f1be63266ab4d554740532335b9d75ea669", size = 20556 },
]

[[package]]
name = "pydantic"
version = "2.11.3"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "annotated-types" },
    { name = "pydantic-core" },
    { name = "typing-extensions" },
    { name = "typing-inspection" },
]
sdist = { url = "https://files.pythonhosted.org/packages/10/2e/ca897f093ee6c5f3b0bee123ee4465c50e75431c3d5b6a3b44a47134e891/pydantic-2.11.3.tar.gz", hash = "sha256:7471657138c16adad9322fe3070c0116dd6c3ad8d649300e3cbdfe91f4db4ec3", size = 785513 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b0/1d/407b29780a289868ed696d1616f4aad49d6388e5a77f567dcd2629dcd7b8/pydantic-2.11.3-py3-none-any.whl", hash = "sha256:a082753436a07f9ba1289c6ffa01cd93db3548776088aa917cc43b63f68fa60f", size = 443591 },
]

[[package]]
name = "pydantic-core"
version = "2.33.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "typing-extensions" },
]
sdist = { url = "https://files.pythonhosted.org/packages/17/19/ed6a078a5287aea7922de6841ef4c06157931622c89c2a47940837b5eecd/pydantic_core-2.33.1.tar.gz", hash = "sha256:bcc9c6fdb0ced789245b02b7d6603e17d1563064ddcfc36f046b61c0c05dd9df", size = 434395 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/38/ea/5f572806ab4d4223d11551af814d243b0e3e02cc6913def4d1fe4a5ca41c/pydantic_core-2.33.1-cp310-cp310-macosx_10_12_x86_64.whl", hash = "sha256:3077cfdb6125cc8dab61b155fdd714663e401f0e6883f9632118ec12cf42df26", size = 2044021 },
    { url = "https://files.pythonhosted.org/packages/8c/d1/f86cc96d2aa80e3881140d16d12ef2b491223f90b28b9a911346c04ac359/pydantic_core-2.33.1-cp310-cp310-macosx_11_0_arm64.whl", hash = "sha256:8ffab8b2908d152e74862d276cf5017c81a2f3719f14e8e3e8d6b83fda863927", size = 1861742 },
    { url = "https://files.pythonhosted.org/packages/37/08/fbd2cd1e9fc735a0df0142fac41c114ad9602d1c004aea340169ae90973b/pydantic_core-2.33.1-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:5183e4f6a2d468787243ebcd70cf4098c247e60d73fb7d68d5bc1e1beaa0c4db", size = 1910414 },
    { url = "https://files.pythonhosted.org/packages/7f/73/3ac217751decbf8d6cb9443cec9b9eb0130eeada6ae56403e11b486e277e/pydantic_core-2.33.1-cp310-cp310-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:398a38d323f37714023be1e0285765f0a27243a8b1506b7b7de87b647b517e48", size = 1996848 },
    { url = "https://files.pythonhosted.org/packages/9a/f5/5c26b265cdcff2661e2520d2d1e9db72d117ea00eb41e00a76efe68cb009/pydantic_core-2.33.1-cp310-cp310-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:87d3776f0001b43acebfa86f8c64019c043b55cc5a6a2e313d728b5c95b46969", size = 2141055 },
    { url = "https://files.pythonhosted.org/packages/5d/14/a9c3cee817ef2f8347c5ce0713e91867a0dceceefcb2973942855c917379/pydantic_core-2.33.1-cp310-cp310-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:c566dd9c5f63d22226409553531f89de0cac55397f2ab8d97d6f06cfce6d947e", size = 2753806 },
    { url = "https://files.pythonhosted.org/packages/f2/68/866ce83a51dd37e7c604ce0050ff6ad26de65a7799df89f4db87dd93d1d6/pydantic_core-2.33.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:a0d5f3acc81452c56895e90643a625302bd6be351e7010664151cc55b7b97f89", size = 2007777 },
    { url = "https://files.pythonhosted.org/packages/b6/a8/36771f4404bb3e49bd6d4344da4dede0bf89cc1e01f3b723c47248a3761c/pydantic_core-2.33.1-cp310-cp310-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:d3a07fadec2a13274a8d861d3d37c61e97a816beae717efccaa4b36dfcaadcde", size = 2122803 },
    { url = "https://files.pythonhosted.org/packages/18/9c/730a09b2694aa89360d20756369822d98dc2f31b717c21df33b64ffd1f50/pydantic_core-2.33.1-cp310-cp310-musllinux_1_1_aarch64.whl", hash = "sha256:f99aeda58dce827f76963ee87a0ebe75e648c72ff9ba1174a253f6744f518f65", size = 2086755 },
    { url = "https://files.pythonhosted.org/packages/54/8e/2dccd89602b5ec31d1c58138d02340ecb2ebb8c2cac3cc66b65ce3edb6ce/pydantic_core-2.33.1-cp310-cp310-musllinux_1_1_armv7l.whl", hash = "sha256:902dbc832141aa0ec374f4310f1e4e7febeebc3256f00dc359a9ac3f264a45dc", size = 2257358 },
    { url = "https://files.pythonhosted.org/packages/d1/9c/126e4ac1bfad8a95a9837acdd0963695d69264179ba4ede8b8c40d741702/pydantic_core-2.33.1-cp310-cp310-musllinux_1_1_x86_64.whl", hash = "sha256:fe44d56aa0b00d66640aa84a3cbe80b7a3ccdc6f0b1ca71090696a6d4777c091", size = 2257916 },
    { url = "https://files.pythonhosted.org/packages/7d/ba/91eea2047e681a6853c81c20aeca9dcdaa5402ccb7404a2097c2adf9d038/pydantic_core-2.33.1-cp310-cp310-win32.whl", hash = "sha256:ed3eb16d51257c763539bde21e011092f127a2202692afaeaccb50db55a31383", size = 1923823 },
    { url = "https://files.pythonhosted.org/packages/94/c0/fcdf739bf60d836a38811476f6ecd50374880b01e3014318b6e809ddfd52/pydantic_core-2.33.1-cp310-cp310-win_amd64.whl", hash = "sha256:694ad99a7f6718c1a498dc170ca430687a39894a60327f548e02a9c7ee4b6504", size = 1952494 },
    { url = "https://files.pythonhosted.org/packages/d6/7f/c6298830cb780c46b4f46bb24298d01019ffa4d21769f39b908cd14bbd50/pydantic_core-2.33.1-cp311-cp311-macosx_10_12_x86_64.whl", hash = "sha256:6e966fc3caaf9f1d96b349b0341c70c8d6573bf1bac7261f7b0ba88f96c56c24", size = 2044224 },
    { url = "https://files.pythonhosted.org/packages/a8/65/6ab3a536776cad5343f625245bd38165d6663256ad43f3a200e5936afd6c/pydantic_core-2.33.1-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:bfd0adeee563d59c598ceabddf2c92eec77abcb3f4a391b19aa7366170bd9e30", size = 1858845 },
    { url = "https://files.pythonhosted.org/packages/e9/15/9a22fd26ba5ee8c669d4b8c9c244238e940cd5d818649603ca81d1c69861/pydantic_core-2.33.1-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:91815221101ad3c6b507804178a7bb5cb7b2ead9ecd600041669c8d805ebd595", size = 1910029 },
    { url = "https://files.pythonhosted.org/packages/d5/33/8cb1a62818974045086f55f604044bf35b9342900318f9a2a029a1bec460/pydantic_core-2.33.1-cp311-cp311-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:9fea9c1869bb4742d174a57b4700c6dadea951df8b06de40c2fedb4f02931c2e", size = 1997784 },
    { url = "https://files.pythonhosted.org/packages/c0/ca/49958e4df7715c71773e1ea5be1c74544923d10319173264e6db122543f9/pydantic_core-2.33.1-cp311-cp311-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:1d20eb4861329bb2484c021b9d9a977566ab16d84000a57e28061151c62b349a", size = 2141075 },
    { url = "https://files.pythonhosted.org/packages/7b/a6/0b3a167a9773c79ba834b959b4e18c3ae9216b8319bd8422792abc8a41b1/pydantic_core-2.33.1-cp311-cp311-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:0fb935c5591573ae3201640579f30128ccc10739b45663f93c06796854405505", size = 2745849 },
    { url = "https://files.pythonhosted.org/packages/0b/60/516484135173aa9e5861d7a0663dce82e4746d2e7f803627d8c25dfa5578/pydantic_core-2.33.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:c964fd24e6166420d18fb53996d8c9fd6eac9bf5ae3ec3d03015be4414ce497f", size = 2005794 },
    { url = "https://files.pythonhosted.org/packages/86/70/05b1eb77459ad47de00cf78ee003016da0cedf8b9170260488d7c21e9181/pydantic_core-2.33.1-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:681d65e9011f7392db5aa002b7423cc442d6a673c635668c227c6c8d0e5a4f77", size = 2123237 },
    { url = "https://files.pythonhosted.org/packages/c7/57/12667a1409c04ae7dc95d3b43158948eb0368e9c790be8b095cb60611459/pydantic_core-2.33.1-cp311-cp311-musllinux_1_1_aarch64.whl", hash = "sha256:e100c52f7355a48413e2999bfb4e139d2977a904495441b374f3d4fb4a170961", size = 2086351 },
    { url = "https://files.pythonhosted.org/packages/57/61/cc6d1d1c1664b58fdd6ecc64c84366c34ec9b606aeb66cafab6f4088974c/pydantic_core-2.33.1-cp311-cp311-musllinux_1_1_armv7l.whl", hash = "sha256:048831bd363490be79acdd3232f74a0e9951b11b2b4cc058aeb72b22fdc3abe1", size = 2258914 },
    { url = "https://files.pythonhosted.org/packages/d1/0a/edb137176a1f5419b2ddee8bde6a0a548cfa3c74f657f63e56232df8de88/pydantic_core-2.33.1-cp311-cp311-musllinux_1_1_x86_64.whl", hash = "sha256:bdc84017d28459c00db6f918a7272a5190bec3090058334e43a76afb279eac7c", size = 2257385 },
    { url = "https://files.pythonhosted.org/packages/26/3c/48ca982d50e4b0e1d9954919c887bdc1c2b462801bf408613ccc641b3daa/pydantic_core-2.33.1-cp311-cp311-win32.whl", hash = "sha256:32cd11c5914d1179df70406427097c7dcde19fddf1418c787540f4b730289896", size = 1923765 },
    { url = "https://files.pythonhosted.org/packages/33/cd/7ab70b99e5e21559f5de38a0928ea84e6f23fdef2b0d16a6feaf942b003c/pydantic_core-2.33.1-cp311-cp311-win_amd64.whl", hash = "sha256:2ea62419ba8c397e7da28a9170a16219d310d2cf4970dbc65c32faf20d828c83", size = 1950688 },
    { url = "https://files.pythonhosted.org/packages/4b/ae/db1fc237b82e2cacd379f63e3335748ab88b5adde98bf7544a1b1bd10a84/pydantic_core-2.33.1-cp311-cp311-win_arm64.whl", hash = "sha256:fc903512177361e868bc1f5b80ac8c8a6e05fcdd574a5fb5ffeac5a9982b9e89", size = 1908185 },
    { url = "https://files.pythonhosted.org/packages/c8/ce/3cb22b07c29938f97ff5f5bb27521f95e2ebec399b882392deb68d6c440e/pydantic_core-2.33.1-cp312-cp312-macosx_10_12_x86_64.whl", hash = "sha256:1293d7febb995e9d3ec3ea09caf1a26214eec45b0f29f6074abb004723fc1de8", size = 2026640 },
    { url = "https://files.pythonhosted.org/packages/19/78/f381d643b12378fee782a72126ec5d793081ef03791c28a0fd542a5bee64/pydantic_core-2.33.1-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:99b56acd433386c8f20be5c4000786d1e7ca0523c8eefc995d14d79c7a081498", size = 1852649 },
    { url = "https://files.pythonhosted.org/packages/9d/2b/98a37b80b15aac9eb2c6cfc6dbd35e5058a352891c5cce3a8472d77665a6/pydantic_core-2.33.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:35a5ec3fa8c2fe6c53e1b2ccc2454398f95d5393ab398478f53e1afbbeb4d939", size = 1892472 },
    { url = "https://files.pythonhosted.org/packages/4e/d4/3c59514e0f55a161004792b9ff3039da52448f43f5834f905abef9db6e4a/pydantic_core-2.33.1-cp312-cp312-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:b172f7b9d2f3abc0efd12e3386f7e48b576ef309544ac3a63e5e9cdd2e24585d", size = 1977509 },
    { url = "https://files.pythonhosted.org/packages/a9/b6/c2c7946ef70576f79a25db59a576bce088bdc5952d1b93c9789b091df716/pydantic_core-2.33.1-cp312-cp312-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:9097b9f17f91eea659b9ec58148c0747ec354a42f7389b9d50701610d86f812e", size = 2128702 },
    { url = "https://files.pythonhosted.org/packages/88/fe/65a880f81e3f2a974312b61f82a03d85528f89a010ce21ad92f109d94deb/pydantic_core-2.33.1-cp312-cp312-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:cc77ec5b7e2118b152b0d886c7514a4653bcb58c6b1d760134a9fab915f777b3", size = 2679428 },
    { url = "https://files.pythonhosted.org/packages/6f/ff/4459e4146afd0462fb483bb98aa2436d69c484737feaceba1341615fb0ac/pydantic_core-2.33.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:d5e3d15245b08fa4a84cefc6c9222e6f37c98111c8679fbd94aa145f9a0ae23d", size = 2008753 },
    { url = "https://files.pythonhosted.org/packages/7c/76/1c42e384e8d78452ededac8b583fe2550c84abfef83a0552e0e7478ccbc3/pydantic_core-2.33.1-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:ef99779001d7ac2e2461d8ab55d3373fe7315caefdbecd8ced75304ae5a6fc6b", size = 2114849 },
    { url = "https://files.pythonhosted.org/packages/00/72/7d0cf05095c15f7ffe0eb78914b166d591c0eed72f294da68378da205101/pydantic_core-2.33.1-cp312-cp312-musllinux_1_1_aarch64.whl", hash = "sha256:fc6bf8869e193855e8d91d91f6bf59699a5cdfaa47a404e278e776dd7f168b39", size = 2069541 },
    { url = "https://files.pythonhosted.org/packages/b3/69/94a514066bb7d8be499aa764926937409d2389c09be0b5107a970286ef81/pydantic_core-2.33.1-cp312-cp312-musllinux_1_1_armv7l.whl", hash = "sha256:b1caa0bc2741b043db7823843e1bde8aaa58a55a58fda06083b0569f8b45693a", size = 2239225 },
    { url = "https://files.pythonhosted.org/packages/84/b0/e390071eadb44b41f4f54c3cef64d8bf5f9612c92686c9299eaa09e267e2/pydantic_core-2.33.1-cp312-cp312-musllinux_1_1_x86_64.whl", hash = "sha256:ec259f62538e8bf364903a7d0d0239447059f9434b284f5536e8402b7dd198db", size = 2248373 },
    { url = "https://files.pythonhosted.org/packages/d6/b2/288b3579ffc07e92af66e2f1a11be3b056fe1214aab314748461f21a31c3/pydantic_core-2.33.1-cp312-cp312-win32.whl", hash = "sha256:e14f369c98a7c15772b9da98987f58e2b509a93235582838bd0d1d8c08b68fda", size = 1907034 },
    { url = "https://files.pythonhosted.org/packages/02/28/58442ad1c22b5b6742b992ba9518420235adced665513868f99a1c2638a5/pydantic_core-2.33.1-cp312-cp312-win_amd64.whl", hash = "sha256:1c607801d85e2e123357b3893f82c97a42856192997b95b4d8325deb1cd0c5f4", size = 1956848 },
    { url = "https://files.pythonhosted.org/packages/a1/eb/f54809b51c7e2a1d9f439f158b8dd94359321abcc98767e16fc48ae5a77e/pydantic_core-2.33.1-cp312-cp312-win_arm64.whl", hash = "sha256:8d13f0276806ee722e70a1c93da19748594f19ac4299c7e41237fc791d1861ea", size = 1903986 },
    { url = "https://files.pythonhosted.org/packages/7a/24/eed3466a4308d79155f1cdd5c7432c80ddcc4530ba8623b79d5ced021641/pydantic_core-2.33.1-cp313-cp313-macosx_10_12_x86_64.whl", hash = "sha256:70af6a21237b53d1fe7b9325b20e65cbf2f0a848cf77bed492b029139701e66a", size = 2033551 },
    { url = "https://files.pythonhosted.org/packages/ab/14/df54b1a0bc9b6ded9b758b73139d2c11b4e8eb43e8ab9c5847c0a2913ada/pydantic_core-2.33.1-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:282b3fe1bbbe5ae35224a0dbd05aed9ccabccd241e8e6b60370484234b456266", size = 1852785 },
    { url = "https://files.pythonhosted.org/packages/fa/96/e275f15ff3d34bb04b0125d9bc8848bf69f25d784d92a63676112451bfb9/pydantic_core-2.33.1-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:4b315e596282bbb5822d0c7ee9d255595bd7506d1cb20c2911a4da0b970187d3", size = 1897758 },
    { url = "https://files.pythonhosted.org/packages/b7/d8/96bc536e975b69e3a924b507d2a19aedbf50b24e08c80fb00e35f9baaed8/pydantic_core-2.33.1-cp313-cp313-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:1dfae24cf9921875ca0ca6a8ecb4bb2f13c855794ed0d468d6abbec6e6dcd44a", size = 1986109 },
    { url = "https://files.pythonhosted.org/packages/90/72/ab58e43ce7e900b88cb571ed057b2fcd0e95b708a2e0bed475b10130393e/pydantic_core-2.33.1-cp313-cp313-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:6dd8ecfde08d8bfadaea669e83c63939af76f4cf5538a72597016edfa3fad516", size = 2129159 },
    { url = "https://files.pythonhosted.org/packages/dc/3f/52d85781406886c6870ac995ec0ba7ccc028b530b0798c9080531b409fdb/pydantic_core-2.33.1-cp313-cp313-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:2f593494876eae852dc98c43c6f260f45abdbfeec9e4324e31a481d948214764", size = 2680222 },
    { url = "https://files.pythonhosted.org/packages/f4/56/6e2ef42f363a0eec0fd92f74a91e0ac48cd2e49b695aac1509ad81eee86a/pydantic_core-2.33.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:948b73114f47fd7016088e5186d13faf5e1b2fe83f5e320e371f035557fd264d", size = 2006980 },
    { url = "https://files.pythonhosted.org/packages/4c/c0/604536c4379cc78359f9ee0aa319f4aedf6b652ec2854953f5a14fc38c5a/pydantic_core-2.33.1-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:e11f3864eb516af21b01e25fac915a82e9ddad3bb0fb9e95a246067398b435a4", size = 2120840 },
    { url = "https://files.pythonhosted.org/packages/1f/46/9eb764814f508f0edfb291a0f75d10854d78113fa13900ce13729aaec3ae/pydantic_core-2.33.1-cp313-cp313-musllinux_1_1_aarch64.whl", hash = "sha256:549150be302428b56fdad0c23c2741dcdb5572413776826c965619a25d9c6bde", size = 2072518 },
    { url = "https://files.pythonhosted.org/packages/42/e3/fb6b2a732b82d1666fa6bf53e3627867ea3131c5f39f98ce92141e3e3dc1/pydantic_core-2.33.1-cp313-cp313-musllinux_1_1_armv7l.whl", hash = "sha256:495bc156026efafd9ef2d82372bd38afce78ddd82bf28ef5276c469e57c0c83e", size = 2248025 },
    { url = "https://files.pythonhosted.org/packages/5c/9d/fbe8fe9d1aa4dac88723f10a921bc7418bd3378a567cb5e21193a3c48b43/pydantic_core-2.33.1-cp313-cp313-musllinux_1_1_x86_64.whl", hash = "sha256:ec79de2a8680b1a67a07490bddf9636d5c2fab609ba8c57597e855fa5fa4dacd", size = 2254991 },
    { url = "https://files.pythonhosted.org/packages/aa/99/07e2237b8a66438d9b26482332cda99a9acccb58d284af7bc7c946a42fd3/pydantic_core-2.33.1-cp313-cp313-win32.whl", hash = "sha256:ee12a7be1742f81b8a65b36c6921022301d466b82d80315d215c4c691724986f", size = 1915262 },
    { url = "https://files.pythonhosted.org/packages/8a/f4/e457a7849beeed1e5defbcf5051c6f7b3c91a0624dd31543a64fc9adcf52/pydantic_core-2.33.1-cp313-cp313-win_amd64.whl", hash = "sha256:ede9b407e39949d2afc46385ce6bd6e11588660c26f80576c11c958e6647bc40", size = 1956626 },
    { url = "https://files.pythonhosted.org/packages/20/d0/e8d567a7cff7b04e017ae164d98011f1e1894269fe8e90ea187a3cbfb562/pydantic_core-2.33.1-cp313-cp313-win_arm64.whl", hash = "sha256:aa687a23d4b7871a00e03ca96a09cad0f28f443690d300500603bd0adba4b523", size = 1909590 },
    { url = "https://files.pythonhosted.org/packages/ef/fd/24ea4302d7a527d672c5be06e17df16aabfb4e9fdc6e0b345c21580f3d2a/pydantic_core-2.33.1-cp313-cp313t-macosx_11_0_arm64.whl", hash = "sha256:401d7b76e1000d0dd5538e6381d28febdcacb097c8d340dde7d7fc6e13e9f95d", size = 1812963 },
    { url = "https://files.pythonhosted.org/packages/5f/95/4fbc2ecdeb5c1c53f1175a32d870250194eb2fdf6291b795ab08c8646d5d/pydantic_core-2.33.1-cp313-cp313t-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:7aeb055a42d734c0255c9e489ac67e75397d59c6fbe60d155851e9782f276a9c", size = 1986896 },
    { url = "https://files.pythonhosted.org/packages/71/ae/fe31e7f4a62431222d8f65a3bd02e3fa7e6026d154a00818e6d30520ea77/pydantic_core-2.33.1-cp313-cp313t-win_amd64.whl", hash = "sha256:338ea9b73e6e109f15ab439e62cb3b78aa752c7fd9536794112e14bee02c8d18", size = 1931810 },
    { url = "https://files.pythonhosted.org/packages/9c/c7/8b311d5adb0fe00a93ee9b4e92a02b0ec08510e9838885ef781ccbb20604/pydantic_core-2.33.1-pp310-pypy310_pp73-macosx_10_12_x86_64.whl", hash = "sha256:5c834f54f8f4640fd7e4b193f80eb25a0602bba9e19b3cd2fc7ffe8199f5ae02", size = 2041659 },
    { url = "https://files.pythonhosted.org/packages/8a/d6/4f58d32066a9e26530daaf9adc6664b01875ae0691570094968aaa7b8fcc/pydantic_core-2.33.1-pp310-pypy310_pp73-macosx_11_0_arm64.whl", hash = "sha256:049e0de24cf23766f12cc5cc71d8abc07d4a9deb9061b334b62093dedc7cb068", size = 1873294 },
    { url = "https://files.pythonhosted.org/packages/f7/3f/53cc9c45d9229da427909c751f8ed2bf422414f7664ea4dde2d004f596ba/pydantic_core-2.33.1-pp310-pypy310_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:1a28239037b3d6f16916a4c831a5a0eadf856bdd6d2e92c10a0da3a59eadcf3e", size = 1903771 },
    { url = "https://files.pythonhosted.org/packages/f0/49/bf0783279ce674eb9903fb9ae43f6c614cb2f1c4951370258823f795368b/pydantic_core-2.33.1-pp310-pypy310_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:9d3da303ab5f378a268fa7d45f37d7d85c3ec19769f28d2cc0c61826a8de21fe", size = 2083558 },
    { url = "https://files.pythonhosted.org/packages/9c/5b/0d998367687f986c7d8484a2c476d30f07bf5b8b1477649a6092bd4c540e/pydantic_core-2.33.1-pp310-pypy310_pp73-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:25626fb37b3c543818c14821afe0fd3830bc327a43953bc88db924b68c5723f1", size = 2118038 },
    { url = "https://files.pythonhosted.org/packages/b3/33/039287d410230ee125daee57373ac01940d3030d18dba1c29cd3089dc3ca/pydantic_core-2.33.1-pp310-pypy310_pp73-musllinux_1_1_aarch64.whl", hash = "sha256:3ab2d36e20fbfcce8f02d73c33a8a7362980cff717926bbae030b93ae46b56c7", size = 2079315 },
    { url = "https://files.pythonhosted.org/packages/1f/85/6d8b2646d99c062d7da2d0ab2faeb0d6ca9cca4c02da6076376042a20da3/pydantic_core-2.33.1-pp310-pypy310_pp73-musllinux_1_1_armv7l.whl", hash = "sha256:2f9284e11c751b003fd4215ad92d325d92c9cb19ee6729ebd87e3250072cdcde", size = 2249063 },
    { url = "https://files.pythonhosted.org/packages/17/d7/c37d208d5738f7b9ad8f22ae8a727d88ebf9c16c04ed2475122cc3f7224a/pydantic_core-2.33.1-pp310-pypy310_pp73-musllinux_1_1_x86_64.whl", hash = "sha256:048c01eee07d37cbd066fc512b9d8b5ea88ceeb4e629ab94b3e56965ad655add", size = 2254631 },
    { url = "https://files.pythonhosted.org/packages/13/e0/bafa46476d328e4553b85ab9b2f7409e7aaef0ce4c937c894821c542d347/pydantic_core-2.33.1-pp310-pypy310_pp73-win_amd64.whl", hash = "sha256:5ccd429694cf26af7997595d627dd2637e7932214486f55b8a357edaac9dae8c", size = 2080877 },
    { url = "https://files.pythonhosted.org/packages/0b/76/1794e440c1801ed35415238d2c728f26cd12695df9057154ad768b7b991c/pydantic_core-2.33.1-pp311-pypy311_pp73-macosx_10_12_x86_64.whl", hash = "sha256:3a371dc00282c4b84246509a5ddc808e61b9864aa1eae9ecc92bb1268b82db4a", size = 2042858 },
    { url = "https://files.pythonhosted.org/packages/73/b4/9cd7b081fb0b1b4f8150507cd59d27b275c3e22ad60b35cb19ea0977d9b9/pydantic_core-2.33.1-pp311-pypy311_pp73-macosx_11_0_arm64.whl", hash = "sha256:f59295ecc75a1788af8ba92f2e8c6eeaa5a94c22fc4d151e8d9638814f85c8fc", size = 1873745 },
    { url = "https://files.pythonhosted.org/packages/e1/d7/9ddb7575d4321e40d0363903c2576c8c0c3280ebea137777e5ab58d723e3/pydantic_core-2.33.1-pp311-pypy311_pp73-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:08530b8ac922003033f399128505f513e30ca770527cc8bbacf75a84fcc2c74b", size = 1904188 },
    { url = "https://files.pythonhosted.org/packages/d1/a8/3194ccfe461bb08da19377ebec8cb4f13c9bd82e13baebc53c5c7c39a029/pydantic_core-2.33.1-pp311-pypy311_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:bae370459da6a5466978c0eacf90690cb57ec9d533f8e63e564ef3822bfa04fe", size = 2083479 },
    { url = "https://files.pythonhosted.org/packages/42/c7/84cb569555d7179ca0b3f838cef08f66f7089b54432f5b8599aac6e9533e/pydantic_core-2.33.1-pp311-pypy311_pp73-manylinux_2_5_i686.manylinux1_i686.whl", hash = "sha256:e3de2777e3b9f4d603112f78006f4ae0acb936e95f06da6cb1a45fbad6bdb4b5", size = 2118415 },
    { url = "https://files.pythonhosted.org/packages/3b/67/72abb8c73e0837716afbb58a59cc9e3ae43d1aa8677f3b4bc72c16142716/pydantic_core-2.33.1-pp311-pypy311_pp73-musllinux_1_1_aarch64.whl", hash = "sha256:3a64e81e8cba118e108d7126362ea30e021291b7805d47e4896e52c791be2761", size = 2079623 },
    { url = "https://files.pythonhosted.org/packages/0b/cd/c59707e35a47ba4cbbf153c3f7c56420c58653b5801b055dc52cccc8e2dc/pydantic_core-2.33.1-pp311-pypy311_pp73-musllinux_1_1_armv7l.whl", hash = "sha256:52928d8c1b6bda03cc6d811e8923dffc87a2d3c8b3bfd2ce16471c7147a24850", size = 2250175 },
    { url = "https://files.pythonhosted.org/packages/84/32/e4325a6676b0bed32d5b084566ec86ed7fd1e9bcbfc49c578b1755bde920/pydantic_core-2.33.1-pp311-pypy311_pp73-musllinux_1_1_x86_64.whl", hash = "sha256:1b30d92c9412beb5ac6b10a3eb7ef92ccb14e3f2a8d7732e2d739f58b3aa7544", size = 2254674 },
    { url = "https://files.pythonhosted.org/packages/12/6f/5596dc418f2e292ffc661d21931ab34591952e2843e7168ea5a52591f6ff/pydantic_core-2.33.1-pp311-pypy311_pp73-win_amd64.whl", hash = "sha256:f995719707e0e29f0f41a8aa3bcea6e761a36c9136104d3189eafb83f5cec5e5", size = 2080951 },
]

[[package]]
name = "pydantic-settings"
version = "2.9.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "pydantic" },
    { name = "python-dotenv" },
    { name = "typing-inspection" },
]
sdist = { url = "https://files.pythonhosted.org/packages/67/1d/42628a2c33e93f8e9acbde0d5d735fa0850f3e6a2f8cb1eb6c40b9a732ac/pydantic_settings-2.9.1.tar.gz", hash = "sha256:c509bf79d27563add44e8446233359004ed85066cd096d8b510f715e6ef5d268", size = 163234 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b6/5f/d6d641b490fd3ec2c4c13b4244d68deea3a1b970a97be64f34fb5504ff72/pydantic_settings-2.9.1-py3-none-any.whl", hash = "sha256:59b4f431b1defb26fe620c71a7d3968a710d719f5f4cdbbdb7926edeb770f6ef", size = 44356 },
]

[[package]]
name = "pytest"
version = "8.3.5"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "colorama", marker = "sys_platform == 'win32'" },
    { name = "exceptiongroup", marker = "python_full_version < '3.11'" },
    { name = "iniconfig" },
    { name = "packaging" },
    { name = "pluggy" },
    { name = "tomli", marker = "python_full_version < '3.11'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/ae/3c/c9d525a414d506893f0cd8a8d0de7706446213181570cdbd766691164e40/pytest-8.3.5.tar.gz", hash = "sha256:f4efe70cc14e511565ac476b57c279e12a855b11f48f212af1080ef2263d3845", size = 1450891 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/30/3d/64ad57c803f1fa1e963a7946b6e0fea4a70df53c1a7fed304586539c2bac/pytest-8.3.5-py3-none-any.whl", hash = "sha256:c69214aa47deac29fad6c2a4f590b9c4a9fdb16a403176fe154b79c0b4d4d820", size = 343634 },
]

[[package]]
name = "python-code-tools"
version = "0.1.0"
source = { editable = "." }
dependencies = [
    { name = "mcp" },
    { name = "pydantic" },
    { name = "ruff" },
    { name = "tomli" },
]

[package.optional-dependencies]
dev = [
    { name = "black" },
    { name = "mypy" },
    { name = "pytest" },
]

[package.metadata]
requires-dist = [
    { name = "black", marker = "extra == 'dev'", specifier = ">=23.0.0" },
    { name = "mcp", specifier = ">=1.6.0" },
    { name = "mypy", marker = "extra == 'dev'", specifier = ">=1.0.0" },
    { name = "pydantic", specifier = ">=2.7.2,<3.0.0" },
    { name = "pytest", marker = "extra == 'dev'", specifier = ">=7.0.0" },
    { name = "ruff", specifier = ">=0.1.0" },
    { name = "tomli", specifier = ">=2.2.1" },
]

[[package]]
name = "python-dotenv"
version = "1.1.0"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/88/2c/7bb1416c5620485aa793f2de31d3df393d3686aa8a8506d11e10e13c5baf/python_dotenv-1.1.0.tar.gz", hash = "sha256:41f90bc6f5f177fb41f53e87666db362025010eb28f60a01c9143bfa33a2b2d5", size = 39920 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/1e/18/98a99ad95133c6a6e2005fe89faedf294a748bd5dc803008059409ac9b1e/python_dotenv-1.1.0-py3-none-any.whl", hash = "sha256:d7c01d9e2293916c18baf562d95698754b0dbbb5e74d457c45d4f6561fb9d55d", size = 20256 },
]

[[package]]
name = "ruff"
version = "0.11.6"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/d9/11/bcef6784c7e5d200b8a1f5c2ddf53e5da0efec37e6e5a44d163fb97e04ba/ruff-0.11.6.tar.gz", hash = "sha256:bec8bcc3ac228a45ccc811e45f7eb61b950dbf4cf31a67fa89352574b01c7d79", size = 4010053 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/6e/1f/8848b625100ebcc8740c8bac5b5dd8ba97dd4ee210970e98832092c1635b/ruff-0.11.6-py3-none-linux_armv6l.whl", hash = "sha256:d84dcbe74cf9356d1bdb4a78cf74fd47c740bf7bdeb7529068f69b08272239a1", size = 10248105 },
    { url = "https://files.pythonhosted.org/packages/e0/47/c44036e70c6cc11e6ee24399c2a1e1f1e99be5152bd7dff0190e4b325b76/ruff-0.11.6-py3-none-macosx_10_12_x86_64.whl", hash = "sha256:9bc583628e1096148011a5d51ff3c836f51899e61112e03e5f2b1573a9b726de", size = 11001494 },
    { url = "https://files.pythonhosted.org/packages/ed/5b/170444061650202d84d316e8f112de02d092bff71fafe060d3542f5bc5df/ruff-0.11.6-py3-none-macosx_11_0_arm64.whl", hash = "sha256:f2959049faeb5ba5e3b378709e9d1bf0cab06528b306b9dd6ebd2a312127964a", size = 10352151 },
    { url = "https://files.pythonhosted.org/packages/ff/91/f02839fb3787c678e112c8865f2c3e87cfe1744dcc96ff9fc56cfb97dda2/ruff-0.11.6-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:63c5d4e30d9d0de7fedbfb3e9e20d134b73a30c1e74b596f40f0629d5c28a193", size = 10541951 },
    { url = "https://files.pythonhosted.org/packages/9e/f3/c09933306096ff7a08abede3cc2534d6fcf5529ccd26504c16bf363989b5/ruff-0.11.6-py3-none-manylinux_2_17_armv7l.manylinux2014_armv7l.whl", hash = "sha256:26a4b9a4e1439f7d0a091c6763a100cef8fbdc10d68593df6f3cfa5abdd9246e", size = 10079195 },
    { url = "https://files.pythonhosted.org/packages/e0/0d/a87f8933fccbc0d8c653cfbf44bedda69c9582ba09210a309c066794e2ee/ruff-0.11.6-py3-none-manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:b5edf270223dd622218256569636dc3e708c2cb989242262fe378609eccf1308", size = 11698918 },
    { url = "https://files.pythonhosted.org/packages/52/7d/8eac0bd083ea8a0b55b7e4628428203441ca68cd55e0b67c135a4bc6e309/ruff-0.11.6-py3-none-manylinux_2_17_ppc64.manylinux2014_ppc64.whl", hash = "sha256:f55844e818206a9dd31ff27f91385afb538067e2dc0beb05f82c293ab84f7d55", size = 12319426 },
    { url = "https://files.pythonhosted.org/packages/c2/dc/d0c17d875662d0c86fadcf4ca014ab2001f867621b793d5d7eef01b9dcce/ruff-0.11.6-py3-none-manylinux_2_17_ppc64le.manylinux2014_ppc64le.whl", hash = "sha256:1d8f782286c5ff562e4e00344f954b9320026d8e3fae2ba9e6948443fafd9ffc", size = 11791012 },
    { url = "https://files.pythonhosted.org/packages/f9/f3/81a1aea17f1065449a72509fc7ccc3659cf93148b136ff2a8291c4bc3ef1/ruff-0.11.6-py3-none-manylinux_2_17_s390x.manylinux2014_s390x.whl", hash = "sha256:01c63ba219514271cee955cd0adc26a4083df1956d57847978383b0e50ffd7d2", size = 13949947 },
    { url = "https://files.pythonhosted.org/packages/61/9f/a3e34de425a668284e7024ee6fd41f452f6fa9d817f1f3495b46e5e3a407/ruff-0.11.6-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:15adac20ef2ca296dd3d8e2bedc6202ea6de81c091a74661c3666e5c4c223ff6", size = 11471753 },
    { url = "https://files.pythonhosted.org/packages/df/c5/4a57a86d12542c0f6e2744f262257b2aa5a3783098ec14e40f3e4b3a354a/ruff-0.11.6-py3-none-musllinux_1_2_aarch64.whl", hash = "sha256:4dd6b09e98144ad7aec026f5588e493c65057d1b387dd937d7787baa531d9bc2", size = 10417121 },
    { url = "https://files.pythonhosted.org/packages/58/3f/a3b4346dff07ef5b862e2ba06d98fcbf71f66f04cf01d375e871382b5e4b/ruff-0.11.6-py3-none-musllinux_1_2_armv7l.whl", hash = "sha256:45b2e1d6c0eed89c248d024ea95074d0e09988d8e7b1dad8d3ab9a67017a5b03", size = 10073829 },
    { url = "https://files.pythonhosted.org/packages/93/cc/7ed02e0b86a649216b845b3ac66ed55d8aa86f5898c5f1691797f408fcb9/ruff-0.11.6-py3-none-musllinux_1_2_i686.whl", hash = "sha256:bd40de4115b2ec4850302f1a1d8067f42e70b4990b68838ccb9ccd9f110c5e8b", size = 11076108 },
    { url = "https://files.pythonhosted.org/packages/39/5e/5b09840fef0eff1a6fa1dea6296c07d09c17cb6fb94ed5593aa591b50460/ruff-0.11.6-py3-none-musllinux_1_2_x86_64.whl", hash = "sha256:77cda2dfbac1ab73aef5e514c4cbfc4ec1fbef4b84a44c736cc26f61b3814cd9", size = 11512366 },
    { url = "https://files.pythonhosted.org/packages/6f/4c/1cd5a84a412d3626335ae69f5f9de2bb554eea0faf46deb1f0cb48534042/ruff-0.11.6-py3-none-win32.whl", hash = "sha256:5151a871554be3036cd6e51d0ec6eef56334d74dfe1702de717a995ee3d5b287", size = 10485900 },
    { url = "https://files.pythonhosted.org/packages/42/46/8997872bc44d43df986491c18d4418f1caff03bc47b7f381261d62c23442/ruff-0.11.6-py3-none-win_amd64.whl", hash = "sha256:cce85721d09c51f3b782c331b0abd07e9d7d5f775840379c640606d3159cae0e", size = 11558592 },
    { url = "https://files.pythonhosted.org/packages/d7/6a/65fecd51a9ca19e1477c3879a7fda24f8904174d1275b419422ac00f6eee/ruff-0.11.6-py3-none-win_arm64.whl", hash = "sha256:3567ba0d07fb170b1b48d944715e3294b77f5b7679e8ba258199a250383ccb79", size = 10682766 },
]

[[package]]
name = "sniffio"
version = "1.3.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/a2/87/a6771e1546d97e7e041b6ae58d80074f81b7d5121207425c964ddf5cfdbd/sniffio-1.3.1.tar.gz", hash = "sha256:f4324edc670a0f49750a81b895f35c3adb843cca46f0530f79fc1babb23789dc", size = 20372 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/e9/44/75a9c9421471a6c4805dbf2356f7c181a29c1879239abab1ea2cc8f38b40/sniffio-1.3.1-py3-none-any.whl", hash = "sha256:2f6da418d1f1e0fddd844478f41680e794e6051915791a034ff65e5f100525a2", size = 10235 },
]

[[package]]
name = "sse-starlette"
version = "2.2.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
    { name = "starlette" },
]
sdist = { url = "https://files.pythonhosted.org/packages/71/a4/80d2a11af59fe75b48230846989e93979c892d3a20016b42bb44edb9e398/sse_starlette-2.2.1.tar.gz", hash = "sha256:54470d5f19274aeed6b2d473430b08b4b379ea851d953b11d7f1c4a2c118b419", size = 17376 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/d9/e0/5b8bd393f27f4a62461c5cf2479c75a2cc2ffa330976f9f00f5f6e4f50eb/sse_starlette-2.2.1-py3-none-any.whl", hash = "sha256:6410a3d3ba0c89e7675d4c273a301d64649c03a5ef1ca101f10b47f895fd0e99", size = 10120 },
]

[[package]]
name = "starlette"
version = "0.46.2"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "anyio" },
]
sdist = { url = "https://files.pythonhosted.org/packages/ce/20/08dfcd9c983f6a6f4a1000d934b9e6d626cff8d2eeb77a89a68eef20a2b7/starlette-0.46.2.tar.gz", hash = "sha256:7f7361f34eed179294600af672f565727419830b54b7b084efe44bb82d2fccd5", size = 2580846 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/8b/0c/9d30a4ebeb6db2b25a841afbb80f6ef9a854fc3b41be131d249a977b4959/starlette-0.46.2-py3-none-any.whl", hash = "sha256:595633ce89f8ffa71a015caed34a5b2dc1c0cdb3f0f1fbd1e69339cf2abeec35", size = 72037 },
]

[[package]]
name = "tomli"
version = "2.2.1"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/18/87/302344fed471e44a87289cf4967697d07e532f2421fdaf868a303cbae4ff/tomli-2.2.1.tar.gz", hash = "sha256:cd45e1dc79c835ce60f7404ec8119f2eb06d38b1deba146f07ced3bbc44505ff", size = 17175 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/43/ca/75707e6efa2b37c77dadb324ae7d9571cb424e61ea73fad7c56c2d14527f/tomli-2.2.1-cp311-cp311-macosx_10_9_x86_64.whl", hash = "sha256:678e4fa69e4575eb77d103de3df8a895e1591b48e740211bd1067378c69e8249", size = 131077 },
    { url = "https://files.pythonhosted.org/packages/c7/16/51ae563a8615d472fdbffc43a3f3d46588c264ac4f024f63f01283becfbb/tomli-2.2.1-cp311-cp311-macosx_11_0_arm64.whl", hash = "sha256:023aa114dd824ade0100497eb2318602af309e5a55595f76b626d6d9f3b7b0a6", size = 123429 },
    { url = "https://files.pythonhosted.org/packages/f1/dd/4f6cd1e7b160041db83c694abc78e100473c15d54620083dbd5aae7b990e/tomli-2.2.1-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:ece47d672db52ac607a3d9599a9d48dcb2f2f735c6c2d1f34130085bb12b112a", size = 226067 },
    { url = "https://files.pythonhosted.org/packages/a9/6b/c54ede5dc70d648cc6361eaf429304b02f2871a345bbdd51e993d6cdf550/tomli-2.2.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:6972ca9c9cc9f0acaa56a8ca1ff51e7af152a9f87fb64623e31d5c83700080ee", size = 236030 },
    { url = "https://files.pythonhosted.org/packages/1f/47/999514fa49cfaf7a92c805a86c3c43f4215621855d151b61c602abb38091/tomli-2.2.1-cp311-cp311-manylinux_2_5_i686.manylinux1_i686.manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:c954d2250168d28797dd4e3ac5cf812a406cd5a92674ee4c8f123c889786aa8e", size = 240898 },
    { url = "https://files.pythonhosted.org/packages/73/41/0a01279a7ae09ee1573b423318e7934674ce06eb33f50936655071d81a24/tomli-2.2.1-cp311-cp311-musllinux_1_2_aarch64.whl", hash = "sha256:8dd28b3e155b80f4d54beb40a441d366adcfe740969820caf156c019fb5c7ec4", size = 229894 },
    { url = "https://files.pythonhosted.org/packages/55/18/5d8bc5b0a0362311ce4d18830a5d28943667599a60d20118074ea1b01bb7/tomli-2.2.1-cp311-cp311-musllinux_1_2_i686.whl", hash = "sha256:e59e304978767a54663af13c07b3d1af22ddee3bb2fb0618ca1593e4f593a106", size = 245319 },
    { url = "https://files.pythonhosted.org/packages/92/a3/7ade0576d17f3cdf5ff44d61390d4b3febb8a9fc2b480c75c47ea048c646/tomli-2.2.1-cp311-cp311-musllinux_1_2_x86_64.whl", hash = "sha256:33580bccab0338d00994d7f16f4c4ec25b776af3ffaac1ed74e0b3fc95e885a8", size = 238273 },
    { url = "https://files.pythonhosted.org/packages/72/6f/fa64ef058ac1446a1e51110c375339b3ec6be245af9d14c87c4a6412dd32/tomli-2.2.1-cp311-cp311-win32.whl", hash = "sha256:465af0e0875402f1d226519c9904f37254b3045fc5084697cefb9bdde1ff99ff", size = 98310 },
    { url = "https://files.pythonhosted.org/packages/6a/1c/4a2dcde4a51b81be3530565e92eda625d94dafb46dbeb15069df4caffc34/tomli-2.2.1-cp311-cp311-win_amd64.whl", hash = "sha256:2d0f2fdd22b02c6d81637a3c95f8cd77f995846af7414c5c4b8d0545afa1bc4b", size = 108309 },
    { url = "https://files.pythonhosted.org/packages/52/e1/f8af4c2fcde17500422858155aeb0d7e93477a0d59a98e56cbfe75070fd0/tomli-2.2.1-cp312-cp312-macosx_10_13_x86_64.whl", hash = "sha256:4a8f6e44de52d5e6c657c9fe83b562f5f4256d8ebbfe4ff922c495620a7f6cea", size = 132762 },
    { url = "https://files.pythonhosted.org/packages/03/b8/152c68bb84fc00396b83e7bbddd5ec0bd3dd409db4195e2a9b3e398ad2e3/tomli-2.2.1-cp312-cp312-macosx_11_0_arm64.whl", hash = "sha256:8d57ca8095a641b8237d5b079147646153d22552f1c637fd3ba7f4b0b29167a8", size = 123453 },
    { url = "https://files.pythonhosted.org/packages/c8/d6/fc9267af9166f79ac528ff7e8c55c8181ded34eb4b0e93daa767b8841573/tomli-2.2.1-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:4e340144ad7ae1533cb897d406382b4b6fede8890a03738ff1683af800d54192", size = 233486 },
    { url = "https://files.pythonhosted.org/packages/5c/51/51c3f2884d7bab89af25f678447ea7d297b53b5a3b5730a7cb2ef6069f07/tomli-2.2.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:db2b95f9de79181805df90bedc5a5ab4c165e6ec3fe99f970d0e302f384ad222", size = 242349 },
    { url = "https://files.pythonhosted.org/packages/ab/df/bfa89627d13a5cc22402e441e8a931ef2108403db390ff3345c05253935e/tomli-2.2.1-cp312-cp312-manylinux_2_5_i686.manylinux1_i686.manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:40741994320b232529c802f8bc86da4e1aa9f413db394617b9a256ae0f9a7f77", size = 252159 },
    { url = "https://files.pythonhosted.org/packages/9e/6e/fa2b916dced65763a5168c6ccb91066f7639bdc88b48adda990db10c8c0b/tomli-2.2.1-cp312-cp312-musllinux_1_2_aarch64.whl", hash = "sha256:400e720fe168c0f8521520190686ef8ef033fb19fc493da09779e592861b78c6", size = 237243 },
    { url = "https://files.pythonhosted.org/packages/b4/04/885d3b1f650e1153cbb93a6a9782c58a972b94ea4483ae4ac5cedd5e4a09/tomli-2.2.1-cp312-cp312-musllinux_1_2_i686.whl", hash = "sha256:02abe224de6ae62c19f090f68da4e27b10af2b93213d36cf44e6e1c5abd19fdd", size = 259645 },
    { url = "https://files.pythonhosted.org/packages/9c/de/6b432d66e986e501586da298e28ebeefd3edc2c780f3ad73d22566034239/tomli-2.2.1-cp312-cp312-musllinux_1_2_x86_64.whl", hash = "sha256:b82ebccc8c8a36f2094e969560a1b836758481f3dc360ce9a3277c65f374285e", size = 244584 },
    { url = "https://files.pythonhosted.org/packages/1c/9a/47c0449b98e6e7d1be6cbac02f93dd79003234ddc4aaab6ba07a9a7482e2/tomli-2.2.1-cp312-cp312-win32.whl", hash = "sha256:889f80ef92701b9dbb224e49ec87c645ce5df3fa2cc548664eb8a25e03127a98", size = 98875 },
    { url = "https://files.pythonhosted.org/packages/ef/60/9b9638f081c6f1261e2688bd487625cd1e660d0a85bd469e91d8db969734/tomli-2.2.1-cp312-cp312-win_amd64.whl", hash = "sha256:7fc04e92e1d624a4a63c76474610238576942d6b8950a2d7f908a340494e67e4", size = 109418 },
    { url = "https://files.pythonhosted.org/packages/04/90/2ee5f2e0362cb8a0b6499dc44f4d7d48f8fff06d28ba46e6f1eaa61a1388/tomli-2.2.1-cp313-cp313-macosx_10_13_x86_64.whl", hash = "sha256:f4039b9cbc3048b2416cc57ab3bda989a6fcf9b36cf8937f01a6e731b64f80d7", size = 132708 },
    { url = "https://files.pythonhosted.org/packages/c0/ec/46b4108816de6b385141f082ba99e315501ccd0a2ea23db4a100dd3990ea/tomli-2.2.1-cp313-cp313-macosx_11_0_arm64.whl", hash = "sha256:286f0ca2ffeeb5b9bd4fcc8d6c330534323ec51b2f52da063b11c502da16f30c", size = 123582 },
    { url = "https://files.pythonhosted.org/packages/a0/bd/b470466d0137b37b68d24556c38a0cc819e8febe392d5b199dcd7f578365/tomli-2.2.1-cp313-cp313-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:a92ef1a44547e894e2a17d24e7557a5e85a9e1d0048b0b5e7541f76c5032cb13", size = 232543 },
    { url = "https://files.pythonhosted.org/packages/d9/e5/82e80ff3b751373f7cead2815bcbe2d51c895b3c990686741a8e56ec42ab/tomli-2.2.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:9316dc65bed1684c9a98ee68759ceaed29d229e985297003e494aa825ebb0281", size = 241691 },
    { url = "https://files.pythonhosted.org/packages/05/7e/2a110bc2713557d6a1bfb06af23dd01e7dde52b6ee7dadc589868f9abfac/tomli-2.2.1-cp313-cp313-manylinux_2_5_i686.manylinux1_i686.manylinux_2_17_i686.manylinux2014_i686.whl", hash = "sha256:e85e99945e688e32d5a35c1ff38ed0b3f41f43fad8df0bdf79f72b2ba7bc5272", size = 251170 },
    { url = "https://files.pythonhosted.org/packages/64/7b/22d713946efe00e0adbcdfd6d1aa119ae03fd0b60ebed51ebb3fa9f5a2e5/tomli-2.2.1-cp313-cp313-musllinux_1_2_aarch64.whl", hash = "sha256:ac065718db92ca818f8d6141b5f66369833d4a80a9d74435a268c52bdfa73140", size = 236530 },
    { url = "https://files.pythonhosted.org/packages/38/31/3a76f67da4b0cf37b742ca76beaf819dca0ebef26d78fc794a576e08accf/tomli-2.2.1-cp313-cp313-musllinux_1_2_i686.whl", hash = "sha256:d920f33822747519673ee656a4b6ac33e382eca9d331c87770faa3eef562aeb2", size = 258666 },
    { url = "https://files.pythonhosted.org/packages/07/10/5af1293da642aded87e8a988753945d0cf7e00a9452d3911dd3bb354c9e2/tomli-2.2.1-cp313-cp313-musllinux_1_2_x86_64.whl", hash = "sha256:a198f10c4d1b1375d7687bc25294306e551bf1abfa4eace6650070a5c1ae2744", size = 243954 },
    { url = "https://files.pythonhosted.org/packages/5b/b9/1ed31d167be802da0fc95020d04cd27b7d7065cc6fbefdd2f9186f60d7bd/tomli-2.2.1-cp313-cp313-win32.whl", hash = "sha256:d3f5614314d758649ab2ab3a62d4f2004c825922f9e370b29416484086b264ec", size = 98724 },
    { url = "https://files.pythonhosted.org/packages/c7/32/b0963458706accd9afcfeb867c0f9175a741bf7b19cd424230714d722198/tomli-2.2.1-cp313-cp313-win_amd64.whl", hash = "sha256:a38aa0308e754b0e3c67e344754dff64999ff9b513e691d0e786265c93583c69", size = 109383 },
    { url = "https://files.pythonhosted.org/packages/6e/c2/61d3e0f47e2b74ef40a68b9e6ad5984f6241a942f7cd3bbfbdbd03861ea9/tomli-2.2.1-py3-none-any.whl", hash = "sha256:cb55c73c5f4408779d0cf3eef9f762b9c9f147a77de7b258bef0a5628adc85cc", size = 14257 },
]

[[package]]
name = "typing-extensions"
version = "4.13.2"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/packages/f6/37/23083fcd6e35492953e8d2aaaa68b860eb422b34627b13f2ce3eb6106061/typing_extensions-4.13.2.tar.gz", hash = "sha256:e6c81219bd689f51865d9e372991c540bda33a0379d5573cddb9a3a23f7caaef", size = 106967 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/8b/54/b1ae86c0973cc6f0210b53d508ca3641fb6d0c56823f288d108bc7ab3cc8/typing_extensions-4.13.2-py3-none-any.whl", hash = "sha256:a439e7c04b49fec3e5d3e2beaa21755cadbbdc391694e28ccdd36ca4a1408f8c", size = 45806 },
]

[[package]]
name = "typing-inspection"
version = "0.4.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "typing-extensions" },
]
sdist = { url = "https://files.pythonhosted.org/packages/82/5c/e6082df02e215b846b4b8c0b887a64d7d08ffaba30605502639d44c06b82/typing_inspection-0.4.0.tar.gz", hash = "sha256:9765c87de36671694a67904bf2c96e395be9c6439bb6c87b5142569dcdd65122", size = 76222 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/31/08/aa4fdfb71f7de5176385bd9e90852eaf6b5d622735020ad600f2bab54385/typing_inspection-0.4.0-py3-none-any.whl", hash = "sha256:50e72559fcd2a6367a19f7a7e610e6afcb9fac940c650290eed893d61386832f", size = 14125 },
]

[[package]]
name = "uvicorn"
version = "0.34.2"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "click" },
    { name = "h11" },
    { name = "typing-extensions", marker = "python_full_version < '3.11'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/a6/ae/9bbb19b9e1c450cf9ecaef06463e40234d98d95bf572fab11b4f19ae5ded/uvicorn-0.34.2.tar.gz", hash = "sha256:0e929828f6186353a80b58ea719861d2629d766293b6d19baf086ba31d4f3328", size = 76815 }
wheels = [
    { url = "https://files.pythonhosted.org/packages/b1/4b/4cef6ce21a2aaca9d852a6e84ef4f135d99fcd74fa75105e2fc0c8308acd/uvicorn-0.34.2-py3-none-any.whl", hash = "sha256:deb49af569084536d269fe0a6d67e3754f104cf03aba7c11c40f01aadf33c403", size = 62483 },
]


