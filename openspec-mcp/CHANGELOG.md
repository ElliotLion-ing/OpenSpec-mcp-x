# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-21

### ✨ Initial Release

- Initial NPX package distribution of OpenSpec MCP Server
- Node.js wrapper for seamless Python server execution
- Automatic Python dependency management (mcp, requests)
- Support for all OpenSpec CLI commands through MCP protocol
- Cross-platform support (macOS, Linux, Windows)

### 🎯 Features

- **OpenSpec Integration**: Full support for OpenSpec API specification workflow
- **Auto-dependency Management**: Automatic installation of Python dependencies
- **Easy Installation**: Simple `npx openspec-mcp-x@latest` usage
- **Python Version Detection**: Automatic detection of Python 3.10+
- **Stdio Forwarding**: Seamless MCP protocol communication

### 📦 Available Tools

- `check_openspec_status` - Check OpenSpec installation and version
- `openspec_init` - Initialize OpenSpec in a project
- `openspec_update` - Update OpenSpec instruction files
- `openspec_list` - List changes or specs
- `openspec_show` - Display change or spec details
- `openspec_change_show` - Show change proposals
- `openspec_change_validate` - Validate changes
- `openspec_spec_show` - Display specifications
- `openspec_spec_list` - List all specifications
- `openspec_spec_validate` - Validate specs
- `openspec_validate` - General validation
- `openspec_archive` - Archive completed changes
- `openspec_help` - Get help information

### 🔧 Technical Details

- Requires Python 3.10+ for MCP server
- Requires Node.js 14+ for NPX distribution
- Uses stdio transport for MCP communication
- Automatic PYTHONPATH configuration

