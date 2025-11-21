# OpenSpec MCP - NPX 包设置指南

## 📦 已创建的文件结构

```
openspec-mcp/
├── bin/
│   └── openspec-mcp-x.js      # Node.js wrapper 脚本 (NPX 入口点)
├── src/
│   └── openspec_mcp/
│       ├── __init__.py
│       └── server.py           # Python MCP 服务器
├── package.json                # NPM 包配置
├── pyproject.toml              # Python 包配置 (保留)
├── .npmignore                  # NPM 发布忽略文件
├── CHANGELOG.md                # 版本变更日志
├── README.md                   # 使用文档 (已更新)
├── publish.sh                  # 发布脚本
└── update.sh                   # 版本更新脚本
```

## ✅ 完成的工作

### 1. ✅ Node.js Wrapper (`bin/openspec-mcp-x.js`)

**功能**:
- 自动检测 Python 3.10+ 版本
- 自动安装 Python 依赖 (mcp >= 0.9.0, requests >= 2.31.0)
- 设置 PYTHONPATH 并启动 Python MCP 服务器
- 转发 stdio 用于 MCP 通信
- 跨平台支持 (macOS, Linux, Windows)

### 2. ✅ NPM 包配置 (`package.json`)

**配置**:
- 包名: `openspec-mcp-x`
- 版本: `1.0.0`
- 主入口: `bin/openspec-mcp-x.js`
- NPX 命令: `npx openspec-mcp-x@latest`
- 包含文件: bin/, src/, README.md, CHANGELOG.md
- 关键词: mcp, openspec, api, specification, openapi, swagger, cursor

### 3. ✅ 发布脚本 (`publish.sh`)

**功能**:
- 清理临时文件 (__pycache__, *.pyc)
- 验证 NPM 登录状态
- 检查包名和版本状态
- 预览包内容
- 运行测试（如果有）
- 确认后发布到 NPM
- 提供后续步骤指引

### 4. ✅ 版本更新脚本 (`update.sh`)

**功能**:
- 交互式选择版本类型 (patch/minor/major/custom)
- 自动更新 package.json 版本号
- 自动更新 pyproject.toml 版本号
- 自动更新 CHANGELOG.md 并插入新版本条目
- Git 提交和打标签
- 验证 NPM 登录
- 发布到 NPM
- 提供完整的后续步骤指引

### 5. ✅ 忽略文件配置 (`.npmignore`)

**排除内容**:
- Python 缓存和构建文件
- 开发和测试文件
- IDE 配置文件
- Git 相关文件
- CI/CD 配置
- 文档目录 (保留 README 和 CHANGELOG)
- 测试文件
- manifest.json (仅用于 Cursor MCP registry)
- 发布脚本 (publish.sh, update.sh)

### 6. ✅ 变更日志 (`CHANGELOG.md`)

**内容**:
- 遵循 Keep a Changelog 格式
- 使用语义化版本控制
- 已记录 1.0.0 初始版本
- 包含功能列表和技术细节

### 7. ✅ 更新 README.md

**新增内容**:
- 🚀 Quick Start 章节 (NPX 方法)
- 简化的 Cursor 配置说明
- NPX 安装步骤 (只需 2 步)
- 自动依赖管理说明
- 📦 Alternative Installation Methods 章节
- ✅ Verification 章节增强
- 📦 Package Information 章节
- 发布脚本使用说明
- NPM 包链接

## 🚀 使用方法

### 用户安装 (NPX 方法)

1. **配置 Cursor** (`~/.cursor/mcp.json`):
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

2. **重启 Cursor**

3. **验证安装**:
```
Check OpenSpec installation status
```

### 维护者发布流程

#### 首次发布

```bash
cd /Users/ElliotDing/SourceCode/MCP-Package-Deploy/openspec-mcp

# 确保所有文件已提交到 Git
git add .
git commit -m "feat: initial NPX package setup"

# 运行发布脚本
./publish.sh

# 按照提示确认发布
```

#### 版本更新和发布

```bash
# 运行更新脚本
./update.sh

# 选择版本类型:
# 1 - patch (bug 修复): 1.0.0 -> 1.0.1
# 2 - minor (新功能): 1.0.0 -> 1.1.0
# 3 - major (破坏性更新): 1.0.0 -> 2.0.0
# 4 - 自定义版本号

# 脚本会自动:
# - 更新 package.json 版本
# - 更新 pyproject.toml 版本
# - 更新 CHANGELOG.md
# - Git 提交和打标签
# - 发布到 NPM
```

## 🔧 技术细节

### NPX 执行流程

1. 用户在 Cursor 中使用 MCP 功能
2. Cursor 执行: `npx -y openspec-mcp-x@latest`
3. NPX 下载/缓存包到 `~/.npm/_npx/`
4. 执行 `bin/openspec-mcp-x.js`
5. Node.js 脚本:
   - 检测 Python 3.10+
   - 安装 mcp 和 requests (如果缺失)
   - 设置 PYTHONPATH 指向 src/
   - 启动 `python -m openspec_mcp.server`
6. Python MCP 服务器通过 stdio 与 Cursor 通信

### 依赖管理

**运行时依赖** (自动安装):
- Python 3.10+ (需要预装)
- mcp >= 0.9.0 (Node.js wrapper 自动安装)
- requests >= 2.31.0 (Node.js wrapper 自动安装)

**外部依赖** (用户需手动安装):
- OpenSpec CLI: `npm install -g @fission-ai/openspec`

### 跨平台兼容性

- ✅ macOS (darwin)
- ✅ Linux
- ✅ Windows (win32)

所有脚本都使用跨平台命令和路径。

## 📊 发布检查清单

在发布前确认:

- [ ] 所有代码已提交到 Git
- [ ] 版本号已更新 (package.json, pyproject.toml)
- [ ] CHANGELOG.md 已更新
- [ ] README.md 准确无误
- [ ] 本地测试通过 (`npx ./bin/openspec-mcp-x.js`)
- [ ] 已登录 NPM (`npm whoami`)
- [ ] Git tags 已推送

## 🔗 相关链接

- **NPM 包**: https://www.npmjs.com/package/openspec-mcp-x
- **GitHub**: https://github.com/ElliotLion-ing/OpenSpec-mcp-x
- **OpenSpec**: https://github.com/Fission-AI/OpenSpec
- **MCP 协议**: https://modelcontextprotocol.io/

## 📝 注意事项

1. **版本同步**: package.json 和 pyproject.toml 版本号应保持一致
2. **Git 标签**: 每次发布都会创建 `v{version}` 标签
3. **NPM 缓存**: 用户使用 `@latest` 标签确保获取最新版本
4. **Python 依赖**: 首次运行时会自动安装，可能需要几秒钟
5. **OpenSpec CLI**: 需要用户单独安装，MCP 服务器只是包装器

## ❓ 常见问题

### Q: 如何测试本地开发版本？

A: 使用相对路径:
```json
{
  "mcpServers": {
    "openspec": {
      "command": "node",
      "args": ["/path/to/openspec-mcp/bin/openspec-mcp-x.js"],
      "env": {}
    }
  }
}
```

### Q: 如何回滚版本？

A:
```bash
npm unpublish openspec-mcp-x@{version}
git tag -d v{version}
git push origin :refs/tags/v{version}
```

### Q: 用户报告 Python 依赖安装失败？

A: 检查:
1. Python 版本是否 >= 3.10
2. pip 是否可用: `python -m pip --version`
3. 网络连接是否正常
4. 建议用户手动安装: `pip install mcp requests`

## 🎉 完成！

OpenSpec MCP 现在已经完全配置为 NPX 包模式，可以轻松发布和分发！

