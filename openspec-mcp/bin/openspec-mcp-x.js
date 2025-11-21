#!/usr/bin/env node

/**
 * OpenSpec MCP Server - NPX Wrapper
 * 
 * This script wraps the Python MCP server for NPX distribution.
 * It handles:
 * - Python version detection
 * - Environment setup
 * - Process spawning and stdio forwarding
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Color output helpers
const colors = {
  red: (text) => `\x1b[31m${text}\x1b[0m`,
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
};

/**
 * Find Python executable
 */
function findPython() {
  const candidates = ['python3', 'python'];
  
  for (const cmd of candidates) {
    try {
      const result = require('child_process').spawnSync(cmd, ['--version'], {
        stdio: 'pipe',
        encoding: 'utf-8',
      });
      
      if (result.status === 0) {
        const versionOutput = result.stdout || result.stderr;
        const match = versionOutput.match(/Python (\d+)\.(\d+)/);
        
        if (match) {
          const major = parseInt(match[1]);
          const minor = parseInt(match[2]);
          
          // Require Python 3.10+
          if (major === 3 && minor >= 10) {
            return cmd;
          } else if (major > 3) {
            return cmd;
          } else {
            console.error(colors.yellow(`⚠️  Found ${cmd} (${versionOutput.trim()}), but Python 3.10+ is required`));
          }
        }
      }
    } catch (e) {
      // Continue to next candidate
    }
  }
  
  return null;
}

/**
 * Check if Python package 'mcp' is installed
 */
function checkMcpInstalled(pythonCmd) {
  try {
    const result = require('child_process').spawnSync(
      pythonCmd,
      ['-c', 'import mcp; print(mcp.__version__)'],
      {
        stdio: 'pipe',
        encoding: 'utf-8',
      }
    );
    
    return result.status === 0;
  } catch (e) {
    return false;
  }
}

/**
 * Check if requests library is installed
 */
function checkRequestsInstalled(pythonCmd) {
  try {
    const result = require('child_process').spawnSync(
      pythonCmd,
      ['-c', 'import requests'],
      {
        stdio: 'pipe',
        encoding: 'utf-8',
      }
    );
    
    return result.status === 0;
  } catch (e) {
    return false;
  }
}

/**
 * Main entry point
 */
async function main() {
  // Find Python
  const pythonCmd = findPython();
  
  if (!pythonCmd) {
    console.error(colors.red('❌ Error: Python 3.10+ not found'));
    console.error('');
    console.error('OpenSpec MCP requires Python 3.10 or higher.');
    console.error('');
    console.error('Please install Python:');
    console.error('  • macOS: brew install python@3.11');
    console.error('  • Ubuntu/Debian: sudo apt install python3.11');
    console.error('  • Windows: https://www.python.org/downloads/');
    console.error('');
    process.exit(1);
  }
  
  // Check and install dependencies
  let needsWait = false;
  
  if (!checkMcpInstalled(pythonCmd)) {
    // Install mcp package silently
    const installResult = require('child_process').spawnSync(
      pythonCmd,
      ['-m', 'pip', 'install', '-q', 'mcp>=0.9.0'],
      {
        stdio: ['ignore', 'ignore', 'ignore'],
      }
    );
    
    if (installResult.status !== 0) {
      console.error('');
      console.error(colors.red('❌ Failed to install Python package "mcp"'));
      console.error('');
      console.error('Please install manually:');
      console.error(`  ${pythonCmd} -m pip install mcp>=0.9.0`);
      console.error('');
      process.exit(1);
    }
    needsWait = true;
  }
  
  if (!checkRequestsInstalled(pythonCmd)) {
    // Install requests package silently
    const installResult = require('child_process').spawnSync(
      pythonCmd,
      ['-m', 'pip', 'install', '-q', 'requests>=2.31.0'],
      {
        stdio: ['ignore', 'ignore', 'ignore'],
      }
    );
    
    if (installResult.status !== 0) {
      console.error('');
      console.error(colors.red('❌ Failed to install Python package "requests"'));
      console.error('');
      console.error('Please install manually:');
      console.error(`  ${pythonCmd} -m pip install requests>=2.31.0`);
      console.error('');
      process.exit(1);
    }
    needsWait = true;
  }
  
  // Wait a bit if we installed packages
  if (needsWait) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Determine the path to the Python server module
  const packageRoot = path.resolve(__dirname, '..');
  const srcPath = path.join(packageRoot, 'src');
  const serverModule = 'openspec_mcp.server';
  
  // Verify the Python module exists
  const modulePath = path.join(srcPath, 'openspec_mcp', 'server.py');
  if (!fs.existsSync(modulePath)) {
    console.error(colors.red(`❌ Error: Server module not found at ${modulePath}`));
    process.exit(1);
  }
  
  // Set up environment
  const env = {
    ...process.env,
    PYTHONPATH: srcPath,
  };
  
  // Spawn Python process
  const pythonProcess = spawn(
    pythonCmd,
    ['-m', serverModule],
    {
      stdio: 'inherit', // Forward stdin, stdout, stderr
      env: env,
    }
  );
  
  // Handle process exit
  pythonProcess.on('exit', (code, signal) => {
    if (signal) {
      process.exit(1);
    } else {
      process.exit(code || 0);
    }
  });
  
  // Handle termination signals
  process.on('SIGINT', () => {
    pythonProcess.kill('SIGINT');
  });
  
  process.on('SIGTERM', () => {
    pythonProcess.kill('SIGTERM');
  });
}

// Run main function
main().catch(error => {
  console.error(`❌ Error: ${error.message}`);
  process.exit(1);
});

