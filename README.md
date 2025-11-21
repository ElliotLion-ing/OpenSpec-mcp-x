# OpenSpec MCP - NPX Package

OpenSpec MCP Server for Cursor IDE - AI-powered API specification generation and management. Now available as an NPX package for easy installation!

## About OpenSpec

OpenSpec is an AI-powered tool for generating, managing, and validating API specifications. This MCP server provides seamless integration with Cursor IDE.

- **GitHub**: https://github.com/Fission-AI/OpenSpec
- **NPM Package**: https://www.npmjs.com/package/openspec-mcp-x
- **Features**: Automatic API spec generation, validation, and management

## 🚀 Quick Start (NPX Method - Recommended)

The easiest way to use OpenSpec MCP is via NPX. No manual installation required!

### 1. Configure Cursor

Open or create `~/.cursor/mcp.json`:

**Windows:** `C:\Users\<YourUsername>\.cursor\mcp.json`  
**macOS/Linux:** `~/.cursor/mcp.json`

Add the OpenSpec MCP configuration:

```json
{
  "mcpServers": {
    "openspec": {
      "command": "npx",
      "args": ["-y", "openspec-mcp-x@latest"],
      "env": {}
    }
  }
}
```

⚠️ **If you already have other MCP servers**, add the `"openspec"` entry to your existing `"mcpServers"` object (don't replace the entire file).

### 2. Restart Cursor

Completely quit and restart Cursor IDE.

### 3. Verify Installation

In Cursor, ask the AI:
```
Check OpenSpec installation status
```

That's it! The NPX package will automatically:
- ✅ Detect and use your Python installation (3.10+)
- ✅ Install required Python dependencies (mcp, requests)
- ✅ Set up the MCP server for you

### 4. Install OpenSpec CLI (Required)

OpenSpec MCP requires the OpenSpec CLI tool. Install it with:

```bash
npm install -g @fission-ai/openspec
```

Verify installation:
```bash
openspec --version
```

## Requirements

### 1. Python 3.10+
For running the MCP server.

**Check if installed:**
```bash
python --version
# or
python3 --version
```

If not installed or version is below 3.10:
- **Windows**: Visit https://www.python.org/downloads/ (⚠️ Check "Add Python to PATH" during installation)
- **macOS**: Use Homebrew: `brew install python@3.12` or download from https://www.python.org/downloads/

### 2. Node.js & npm
Required for OpenSpec CLI to work.

**Check if installed:**
```bash
node --version
npm --version
```

**If not installed, follow the installation guide for your platform:**

#### 🪟 Windows Installation

> **⚠️ IMPORTANT FOR WINDOWS**: All commands below include non-interactive flags to avoid installation prompts. This is crucial when AI assistants execute these commands.

**Method 1: winget (Recommended - Windows 10+)**
```powershell
# Install Node.js LTS with non-interactive flags
# These flags prevent interactive prompts that would block automated installation
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

# After installation, restart your terminal and verify
node --version
npm --version
```

**Method 2: Chocolatey**
```powershell
# Install Node.js LTS with -y flag to skip confirmation
choco install nodejs-lts -y

# Verify installation
node --version
npm --version
```

**Method 3: Scoop**
```powershell
# Scoop is non-interactive by default
scoop install nodejs-lts
node --version
npm --version
```

**Method 4: Manual Download**
1. Visit https://nodejs.org/
2. Download the **LTS (Long Term Support)** version installer
3. Run the installer (requires administrator privileges)
4. Follow the installation wizard
5. Restart your terminal after installation
6. Verify: `node --version` and `npm --version`

> **📝 Note:** After installation on Windows, you MUST restart your terminal or IDE for the PATH environment variable to be updated. If commands still don't work, restart your computer.

#### 🍎 macOS Installation

**Method 1: Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js LTS
brew install node@20

# Verify installation
node --version
npm --version
```

**Method 2: nvm (Node Version Manager)**
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or reload shell configuration
source ~/.bashrc  # or ~/.zshrc for zsh

# Install Node.js LTS
nvm install --lts
nvm use --lts

# Verify installation
node --version
npm --version
```

**Method 3: Manual Download**
1. Visit https://nodejs.org/
2. Download the **LTS** version for macOS
3. Open the .pkg file and follow the installer
4. Verify: `node --version` and `npm --version`

#### ✅ Post-Installation Verification

After installing Node.js and npm, verify the installation:

```bash
# Check Node.js version (should be 18.x or higher)
node --version

# Check npm version
npm --version

# Optional: Update npm to latest version
npm install -g npm@latest
```

#### 🔧 Troubleshooting Node.js Installation

**Windows - Command not found after installation:**
1. Close all terminal windows completely
2. Open a new terminal/PowerShell window
3. Try again: `node --version`
4. If still not working, restart your computer
5. Environment variable refresh is required on Windows

**macOS - Permission errors with npm:**
```bash
# Fix npm permissions for global packages
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile
```

**Verify PATH:**
- Node.js should be added to your system PATH automatically
- If commands don't work, check if the installation directory is in your PATH
  - **Windows**: `C:\Program Files\nodejs\`
  - **macOS (Homebrew)**: `/usr/local/bin/` or `/opt/homebrew/bin/`

### 3. Cursor IDE
The IDE this MCP server integrates with.

---

## 🤖 For AI Assistants: Automated Prerequisite Installation

If you're an AI assistant helping users set up OpenSpec MCP, follow this automated workflow:

### Step 1: Check Current System

First, detect the platform and check what's already installed:

```bash
# Windows: Check winget availability
winget --version

# macOS: Check if Homebrew is available
brew --version
```

### Step 2: Auto-detect Missing Prerequisites

Check each requirement:

```bash
# Check Python (required: 3.10+)
python --version || python3 --version

# Check Node.js (required: 18.x+)
node --version

# Check npm (bundled with Node.js)
npm --version

# Check pip (Python package manager)
pip --version || pip3 --version
```

### Step 3: Install Missing Components

Based on detection results, use the appropriate commands from the platform-specific sections above.

#### 🪟 Windows Workflow (Non-Interactive Commands)

> **⚠️ CRITICAL FOR WINDOWS**: ALWAYS use non-interactive flags to prevent installation prompts!

```powershell
# If Node.js/npm is missing, use winget with non-interactive flags:
winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements

# Alternative with Chocolatey (if available):
choco install nodejs-lts -y

# After installation, MUST restart terminal or commands won't be found
# Remind user to close and reopen terminal/IDE

# Then verify installation:
node --version
npm --version
```

**Why non-interactive flags are essential on Windows:**
- `--accept-package-agreements`: Auto-accepts package license agreements
- `--accept-source-agreements`: Auto-accepts source agreements (e.g., Microsoft Store terms)
- Without these flags, the command will pause and wait for user input, blocking automated installations

#### 🍎 macOS Workflow

```bash
# Ensure Homebrew is installed first
brew --version || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js if needed
brew install node@20

# Verify
node --version
npm --version
```

### Step 4: Install OpenSpec CLI

After ensuring Node.js and npm are installed:

```bash
# Install OpenSpec globally
npm install -g @fission-ai/openspec

# Verify OpenSpec installation
openspec --version
```

**Important for Windows users:**
- On Windows, if `openspec` command is not found after installation, the user needs to restart their terminal
- npm global packages are installed to: `C:\Users\<Username>\AppData\Roaming\npm`
- This path should be in the system PATH after Node.js installation

### Step 5: Proceed with MCP Server Setup

Once all prerequisites are confirmed, continue with the [Installation](#installation) section below.

### 💡 Essential Tips for AI Assistants

**For Windows:**
1. ⚠️ **ALWAYS use non-interactive flags**: `--accept-package-agreements --accept-source-agreements`
2. ⚠️ **ALWAYS remind users to restart terminal** after Node.js installation
3. Environment variables only refresh after terminal restart
4. If user reports "command not found" after installation → they need to restart terminal

**For macOS:**
1. Check if Homebrew is installed before using it
2. Use `python3` and `pip3` commands (not `python` and `pip`)
3. npm permission issues can be fixed with the npm-global setup (see troubleshooting section)

**General:**
1. Always verify each component after installation before proceeding
2. Check version numbers to ensure requirements are met (Python 3.10+, Node.js 18+)
3. If a command fails, provide the relevant troubleshooting section link
4. Test OpenSpec CLI installation before proceeding to MCP server setup

---

## 📦 Alternative Installation Methods

### Method 1: NPX (Recommended - See Quick Start Above)

The NPX method is the easiest and doesn't require manual installation. See the [Quick Start](#-quick-start-npx-method---recommended) section above.

### Method 2: Manual Installation (Advanced)

If you prefer to install manually or need a development setup:

#### 1. Verify Your Python Command

First, check which Python command works on your system:

```bash
# Try these commands one by one:
python --version
python3 --version
```

**Remember which command works** (either `python` or `python3`), you'll need it in step 3.

#### 2. Install Python Package

Navigate to the openspec-mcp directory and install:

```bash
cd D:\Tools\0mcp\openspec-mcp
pip install -e .
```

#### 3. Configure Cursor

##### Configuration File Location

**All platforms:** `~/.cursor/mcp.json`

- **macOS/Linux:** `~/.cursor/mcp.json`
- **Windows:** `C:\Users\<YourUsername>\.cursor\mcp.json`

💡 **Tip:** This is Cursor's main MCP configuration file, shared by all MCP servers.

##### ⚠️ IMPORTANT: Adding vs. Creating Configuration

**Option A: If the configuration file does NOT exist (first MCP server):**

Create the file `~/.cursor/mcp.json` with this content:

```json
{
  "mcpServers": {
    "openspec": {
      "command": "REPLACE_WITH_YOUR_PYTHON_COMMAND",
      "args": ["-m", "openspec_mcp.server"],
      "env": {}
    }
  }
}
```

⚠️ **Replace `REPLACE_WITH_YOUR_PYTHON_COMMAND`** with the command you verified in step 1 (`python` or `python3`).

**Option B: If the configuration file ALREADY exists (adding to existing MCP servers):**

⚠️ **DO NOT replace the entire file!** Only add the `"openspec"` entry inside the existing `"mcpServers"` object.

Example - if your current config has other servers:

```json
{
  "mcpServers": {
    "some-other-server": {
      "command": "...",
      "args": ["..."],
      "env": {}
    }
  }
}
```

Add the openspec entry like this (add a comma after the previous server):

```json
{
  "mcpServers": {
    "some-other-server": {
      "command": "...",
      "args": ["..."],
      "env": {}
    },
    "openspec": {
      "command": "REPLACE_WITH_YOUR_PYTHON_COMMAND",
      "args": ["-m", "openspec_mcp.server"],
      "env": {}
    }
  }
}
```

⚠️ **Remember to replace `REPLACE_WITH_YOUR_PYTHON_COMMAND`** with your verified Python command.

✅ **Multiple MCP servers can coexist in the same configuration file!**

#### 4. Restart Cursor

Completely quit and restart Cursor.

---

## ✅ Verification

After installation (either NPX or manual method), verify in Cursor:

```
Check OpenSpec installation status
```

Or use the tool directly:
```
Use check_openspec_status tool
```

This will confirm:
- ✅ Python is installed and accessible
- ✅ MCP dependencies are installed
- ✅ OpenSpec CLI is available
- ✅ MCP server is running correctly

## Available Tools

- `check_openspec_status` - Check if OpenSpec is installed and get version info
- `openspec_init` - Initialize OpenSpec in a directory
- `openspec_generate` - Generate API specification
- `openspec_validate` - Validate an API specification file
- `openspec_help` - Get help information about OpenSpec commands

## Usage Examples

### Check Installation Status

```
Use check_openspec_status tool
```

This will check if OpenSpec CLI is installed and show version info.

### Install OpenSpec CLI

Make sure Node.js and npm are installed first (see [Requirements](#requirements) section).

Install OpenSpec CLI using npm:

```bash
npm install -g @fission-ai/openspec
```

Verify installation:
```bash
openspec --version
```

### Initialize OpenSpec in a Project

```
Use openspec_init tool with:
- directory: ./my-project
```

### Generate API Specification

```
Use openspec_generate tool with:
- directory: ./my-project
- output: ./api/openapi.yaml
- format: openapi
```

### Validate Specification

```
Use openspec_validate tool with:
- file_path: ./api/openapi.yaml
```

## Workflow

1. **Install Node.js and npm** (if not already installed):
   - Visit https://nodejs.org/ and download the LTS version, or
   - Use package managers (see [Requirements](#requirements) section)

2. **Install OpenSpec CLI** (first time only):
   ```bash
   npm install -g @fission-ai/openspec
   ```

3. **Check installation**:
   ```
   Use check_openspec_status tool
   ```

4. **Initialize in your project**:
   ```
   Use openspec_init tool with directory: ./my-project
   ```

5. **Generate specifications**:
   ```
   Use openspec_generate tool with directory: ./my-project
   ```

6. **Validate specifications**:
   ```
   Use openspec_validate tool with file_path: ./api/spec.yaml
   ```

## Troubleshooting

### MCP Server Not Showing

1. Check Python version: `python --version` or `python3 --version` (must be 3.10+)
2. Verify configuration file path
3. Restart Cursor completely
4. Check Cursor developer console for errors

### Dependency Installation Failed

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Reinstall
pip install -e .
```

### OpenSpec CLI Not Found

**1. Check if Node.js and npm are installed:**
```bash
node --version
npm --version
```

If not found, install Node.js from https://nodejs.org/ or use package managers (see [Requirements](#requirements)).

**2. Install OpenSpec CLI:**
```bash
npm install -g @fission-ai/openspec
```

**3. Verify installation:**
```bash
openspec --version
```

**4. Test with MCP:**
```
Use check_openspec_status tool
```

### npm Permission Errors (macOS/Linux)

```bash
# Use npx instead, or fix npm permissions:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile
```

## Configuration

OpenSpec can be configured through its configuration files. After running `openspec_init`, you'll find configuration files in your project directory.

Refer to the [OpenSpec documentation](https://github.com/Fission-AI/OpenSpec) for detailed configuration options.

## License

MIT

## 📦 Package Information

### NPX Package

```bash
# Install globally (optional)
npm install -g openspec-mcp-x

# Or use directly with NPX (recommended)
npx openspec-mcp-x@latest
```

### Version History

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.

### Publishing

For maintainers:

```bash
# First-time publish
./publish.sh

# Update version and publish
./update.sh
```

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [OpenAPI Specification](https://swagger.io/specification/)
- [NPM Package](https://www.npmjs.com/package/openspec-mcp-x)

## Support

For issues related to:
- **MCP integration**: Open an issue in this repository
- **OpenSpec functionality**: Visit https://github.com/Fission-AI/OpenSpec
- **NPM package**: https://www.npmjs.com/package/openspec-mcp-x



