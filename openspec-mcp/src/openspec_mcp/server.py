#!/usr/bin/env python3
"""
OpenSpec MCP Server
A Model Context Protocol server for OpenSpec - AI-powered API specification tool
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Initialize MCP server
app = Server("openspec-mcp-x")


def run_command(cmd: list[str], cwd: Optional[str] = None) -> tuple[bool, str, str]:
    """Run a shell command and return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out after 5 minutes"
    except Exception as e:
        return False, "", str(e)


def check_openspec_installed() -> bool:
    """Check if OpenSpec CLI is installed."""
    try:
        result = subprocess.run(
            ["openspec", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="check_openspec_status",
            description=(
                "Check if OpenSpec is installed and get version information. "
                "⚠️ Only call this once at the beginning or when user explicitly asks."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="openspec_init",
            description=(
                "Initialize OpenSpec in a directory. "
                "This runs: openspec init . --tools cursor"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to initialize OpenSpec (default: current directory)",
                        "default": ".",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_update",
            description=(
                "Update OpenSpec instruction files. "
                "This runs: openspec update [path]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to update (default: current directory)",
                        "default": ".",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_list",
            description=(
                "List changes or specs. "
                "This runs: openspec list [--specs|--changes]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["changes", "specs"],
                        "description": "List changes or specs (default: changes)",
                        "default": "changes",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_show",
            description=(
                "Show a change or spec. "
                "This runs: openspec show [item-name]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "item_name": {
                        "type": "string",
                        "description": "Name of the change or spec to show",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "markdown"],
                        "description": "Output format (optional)",
                    },
                },
                "required": ["item_name"],
            },
        ),
        Tool(
            name="openspec_change_show",
            description=(
                "Show a change proposal in JSON or markdown format. "
                "This runs: openspec change show [change-name]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "change_name": {
                        "type": "string",
                        "description": "Name of the change proposal to show",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "markdown"],
                        "description": "Output format (optional)",
                    },
                },
                "required": ["change_name"],
            },
        ),
        Tool(
            name="openspec_change_validate",
            description=(
                "Validate a change proposal. "
                "This runs: openspec change validate [change-name]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "change_name": {
                        "type": "string",
                        "description": "Name of the change proposal to validate (optional)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_spec_show",
            description=(
                "Display a specific specification. "
                "This runs: openspec spec show [spec-id]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "spec_id": {
                        "type": "string",
                        "description": "ID of the specification to show",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "markdown"],
                        "description": "Output format (optional)",
                    },
                },
                "required": ["spec_id"],
            },
        ),
        Tool(
            name="openspec_spec_list",
            description=(
                "List all available specifications. "
                "This runs: openspec spec list"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_spec_validate",
            description=(
                "Validate a specification structure. "
                "This runs: openspec spec validate [spec-id]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "spec_id": {
                        "type": "string",
                        "description": "ID of the specification to validate (optional)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_validate",
            description=(
                "Validate changes and specs. "
                "This runs: openspec validate [item-name]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "item_name": {
                        "type": "string",
                        "description": "Name of the item to validate (optional)",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="openspec_archive",
            description=(
                "Archive a completed change and update main specs. "
                "This runs: openspec archive [change-name]"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Working directory (default: current directory)",
                        "default": ".",
                    },
                    "change_name": {
                        "type": "string",
                        "description": "Name of the change to archive",
                    },
                },
                "required": ["change_name"],
            },
        ),
        Tool(
            name="openspec_help",
            description="Get help information about OpenSpec commands",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Specific command to get help for (optional)",
                    },
                },
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests."""
    try:
        if name == "check_openspec_status":
            return await check_openspec_status(arguments)
        elif name == "openspec_init":
            return await openspec_init(arguments)
        elif name == "openspec_update":
            return await openspec_update(arguments)
        elif name == "openspec_list":
            return await openspec_list(arguments)
        elif name == "openspec_show":
            return await openspec_show(arguments)
        elif name == "openspec_change_show":
            return await openspec_change_show(arguments)
        elif name == "openspec_change_validate":
            return await openspec_change_validate(arguments)
        elif name == "openspec_spec_show":
            return await openspec_spec_show(arguments)
        elif name == "openspec_spec_list":
            return await openspec_spec_list(arguments)
        elif name == "openspec_spec_validate":
            return await openspec_spec_validate(arguments)
        elif name == "openspec_validate":
            return await openspec_validate(arguments)
        elif name == "openspec_archive":
            return await openspec_archive(arguments)
        elif name == "openspec_help":
            return await openspec_help(arguments)
        else:
            return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


async def check_openspec_status(args: dict) -> list[TextContent]:
    """Check OpenSpec installation status."""
    is_installed = check_openspec_installed()
    
    if is_installed:
        success, stdout, stderr = run_command(["openspec", "--version"])
        version_info = stdout.strip() if success else "Unknown"
        
        result = "✅ OpenSpec is installed!\n\n"
        result += f"📦 Version: {version_info}\n\n"
        result += "You can now use OpenSpec commands through this MCP server."
    else:
        result = "❌ OpenSpec is not installed.\n\n"
        result += "Please install OpenSpec manually:\n"
        result += "```bash\n"
        result += "npm install -g @fission-ai/openspec\n"
        result += "```\n\n"
        result += "📝 Note: Node.js and npm are required. Visit https://nodejs.org/ to install.\n"
    
    return [TextContent(type="text", text=result)]


async def openspec_init(args: dict) -> list[TextContent]:
    """Initialize OpenSpec in a directory."""
    directory = os.path.expanduser(args.get("directory", "."))
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    # Use --tools cursor to configure for cursor non-interactively
    cmd = ["openspec", "init", ".", "--tools", "cursor"]
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ OpenSpec initialized in: {directory}\n\n{stdout}"
        result += "\n\n📋 Next steps:\n"
        result += "1. Use 'openspec_list' to list changes and specs\n"
        result += "2. Use 'openspec_change_show' to view change proposals\n"
        result += "3. Use 'openspec_validate' to validate your work\n"
    else:
        result = f"❌ Initialization failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_update(args: dict) -> list[TextContent]:
    """Update OpenSpec instruction files."""
    directory = os.path.expanduser(args.get("directory", "."))
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "update", "."]
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ OpenSpec instruction files updated!\n\n{stdout}"
    else:
        result = f"❌ Update failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_list(args: dict) -> list[TextContent]:
    """List changes or specs."""
    directory = os.path.expanduser(args.get("directory", "."))
    list_type = args.get("type", "changes")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "list"]
    if list_type == "specs":
        cmd.append("--specs")
    elif list_type == "changes":
        cmd.append("--changes")
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ List of {list_type}:\n\n{stdout}"
    else:
        result = f"❌ Failed to list {list_type}:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_show(args: dict) -> list[TextContent]:
    """Show a change or spec."""
    directory = os.path.expanduser(args.get("directory", "."))
    item_name = args.get("item_name")
    format_type = args.get("format")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "show", item_name, "--no-interactive"]
    if format_type == "json":
        cmd.append("--json")
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Item: {item_name}\n\n{stdout}"
    else:
        result = f"❌ Failed to show item:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_change_show(args: dict) -> list[TextContent]:
    """Show a change proposal."""
    directory = os.path.expanduser(args.get("directory", "."))
    change_name = args.get("change_name")
    format_type = args.get("format")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "change", "show", change_name, "--no-interactive"]
    if format_type == "json":
        cmd.append("--json")
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Change proposal: {change_name}\n\n{stdout}"
    else:
        result = f"❌ Failed to show change:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_change_validate(args: dict) -> list[TextContent]:
    """Validate a change proposal."""
    directory = os.path.expanduser(args.get("directory", "."))
    change_name = args.get("change_name")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "change", "validate", "--no-interactive"]
    if change_name:
        cmd.insert(3, change_name)  # Insert before --no-interactive
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Change validation successful!\n\n{stdout}"
    else:
        result = f"❌ Change validation failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_spec_show(args: dict) -> list[TextContent]:
    """Display a specific specification."""
    directory = os.path.expanduser(args.get("directory", "."))
    spec_id = args.get("spec_id")
    format_type = args.get("format")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "spec", "show", spec_id, "--no-interactive"]
    if format_type == "json":
        cmd.append("--json")
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Specification: {spec_id}\n\n{stdout}"
    else:
        result = f"❌ Failed to show spec:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_spec_list(args: dict) -> list[TextContent]:
    """List all available specifications."""
    directory = os.path.expanduser(args.get("directory", "."))
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "spec", "list"]
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Available specifications:\n\n{stdout}"
    else:
        result = f"❌ Failed to list specs:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_spec_validate(args: dict) -> list[TextContent]:
    """Validate a specification structure."""
    directory = os.path.expanduser(args.get("directory", "."))
    spec_id = args.get("spec_id")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "spec", "validate", "--no-interactive"]
    if spec_id:
        cmd.insert(3, spec_id)  # Insert before --no-interactive
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Spec validation successful!\n\n{stdout}"
    else:
        result = f"❌ Spec validation failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_archive(args: dict) -> list[TextContent]:
    """Archive a completed change and update main specs."""
    directory = os.path.expanduser(args.get("directory", "."))
    change_name = args.get("change_name")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    # Use -y to skip confirmation prompts
    cmd = ["openspec", "archive", change_name, "-y"]
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Change archived successfully: {change_name}\n\n{stdout}"
    else:
        result = f"❌ Archive failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_validate(args: dict) -> list[TextContent]:
    """Validate changes and specs."""
    directory = os.path.expanduser(args.get("directory", "."))
    item_name = args.get("item_name")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    if not os.path.exists(directory):
        return [TextContent(type="text", text=f"❌ Directory not found: {directory}")]
    
    cmd = ["openspec", "validate", "--no-interactive"]
    if item_name:
        cmd.insert(2, item_name)  # Insert before --no-interactive
    
    success, stdout, stderr = run_command(cmd, cwd=directory)
    
    if success:
        result = f"✅ Validation successful!\n\n{stdout}"
    else:
        result = f"❌ Validation failed:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def openspec_help(args: dict) -> list[TextContent]:
    """Get OpenSpec help information."""
    command = args.get("command")
    
    if not check_openspec_installed():
        return [TextContent(
            type="text",
            text="❌ OpenSpec is not installed. Please install it manually: npm install -g @fission-ai/openspec"
        )]
    
    cmd = ["openspec", "--help"]
    if command:
        cmd = ["openspec", command, "--help"]
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        result = f"📖 OpenSpec Help:\n\n```\n{stdout}\n```"
    else:
        result = f"❌ Failed to get help:\n\n{stderr}"
    
    return [TextContent(type="text", text=result)]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="openspec-mcp-x",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())


