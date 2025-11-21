#!/bin/bash
# OpenSpec MCP - 一键更新版本并发布到 NPM
# 支持自动更新 patch/minor/major 版本

set -e  # 遇到错误立即退出

echo "🔄 OpenSpec MCP - 版本更新和发布脚本"
echo "================================"
echo ""

# 获取当前版本号
CURRENT_VERSION=$(node -p "require('./package.json').version")
PACKAGE_NAME=$(node -p "require('./package.json').name")

echo "📦 包名: $PACKAGE_NAME"
echo "📌 当前版本: v$CURRENT_VERSION"
echo ""

# 1. 选择版本更新类型
echo "🎯 步骤 1/8: 选择版本更新类型"
echo ""
echo "请选择版本更新类型："
echo "  1) patch  - 修复 bug (${CURRENT_VERSION} -> $(npm version patch --no-git-tag-version 2>/dev/null && npm version $(node -p "require('./package.json').version") --no-git-tag-version --allow-same-version 2>/dev/null || echo 'error'))"
git checkout package.json 2>/dev/null || true
echo "  2) minor  - 新增功能 (${CURRENT_VERSION} -> $(npm version minor --no-git-tag-version 2>/dev/null && npm version $(node -p "require('./package.json').version") --no-git-tag-version --allow-same-version 2>/dev/null || echo 'error'))"
git checkout package.json 2>/dev/null || true
echo "  3) major  - 破坏性更新 (${CURRENT_VERSION} -> $(npm version major --no-git-tag-version 2>/dev/null && npm version $(node -p "require('./package.json').version") --no-git-tag-version --allow-same-version 2>/dev/null || echo 'error'))"
git checkout package.json 2>/dev/null || true
echo "  4) 自定义版本号"
echo ""
read -p "请选择 (1-4): " choice

case $choice in
    1)
        VERSION_TYPE="patch"
        ;;
    2)
        VERSION_TYPE="minor"
        ;;
    3)
        VERSION_TYPE="major"
        ;;
    4)
        read -p "请输入新版本号 (例如: 1.2.0): " CUSTOM_VERSION
        VERSION_TYPE="custom"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
echo ""

# 2. 更新 package.json 版本
echo "📝 步骤 2/8: 更新 package.json..."
if [ "$VERSION_TYPE" = "custom" ]; then
    npm version $CUSTOM_VERSION --no-git-tag-version
else
    npm version $VERSION_TYPE --no-git-tag-version
fi
NEW_VERSION=$(node -p "require('./package.json').version")
echo "✅ package.json 版本已更新: v$CURRENT_VERSION -> v$NEW_VERSION"
echo ""

# 3. 更新 pyproject.toml 版本
echo "📝 步骤 3/8: 更新 pyproject.toml..."
if [ -f "pyproject.toml" ]; then
    sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    echo "✅ pyproject.toml 版本已更新: v$NEW_VERSION"
else
    echo "⚠️  未找到 pyproject.toml"
fi
echo ""

# 4. 更新 CHANGELOG.md
echo "📝 步骤 4/8: 更新 CHANGELOG.md..."
if [ -f "CHANGELOG.md" ]; then
    TODAY=$(date +%Y-%m-%d)
    
    # 在文件开头插入新版本条目
    TMP_FILE=$(mktemp)
    {
        head -n 5 CHANGELOG.md
        echo ""
        echo "## [$NEW_VERSION] - $TODAY"
        echo ""
        echo "### ✨ 新增"
        echo "- TODO: 添加新功能说明"
        echo ""
        echo "### 🎯 改进"
        echo "- TODO: 添加改进说明"
        echo ""
        echo "### 🐛 修复"
        echo "- TODO: 添加修复说明"
        echo ""
        tail -n +6 CHANGELOG.md
    } > "$TMP_FILE"
    mv "$TMP_FILE" CHANGELOG.md
    
    echo "✅ CHANGELOG.md 已更新（请编辑 TODO 部分）"
    echo ""
    echo "⏸️  暂停 10 秒，请编辑 CHANGELOG.md..."
    sleep 10
else
    echo "⚠️  未找到 CHANGELOG.md"
fi
echo ""

# 5. 清理临时文件
echo "🧹 步骤 5/8: 清理临时文件..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
rm -rf src/openspec_mcp.egg-info/ 2>/dev/null || true
rm -f *.tgz 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 6. 提交更改并打标签
echo "📦 步骤 6/8: Git 提交和打标签..."
echo ""
echo "将要提交的更改："
git diff package.json pyproject.toml CHANGELOG.md 2>/dev/null || true
echo ""
read -p "是否提交这些更改？(yes/no): " git_confirm

if [ "$git_confirm" = "yes" ] || [ "$git_confirm" = "y" ]; then
    git add package.json pyproject.toml CHANGELOG.md 2>/dev/null || true
    git commit -m "chore: bump version to $NEW_VERSION"
    git tag "v$NEW_VERSION"
    echo "✅ 已提交并打标签: v$NEW_VERSION"
else
    echo "⏭️  跳过 Git 提交"
fi
echo ""

# 7. 验证登录状态
echo "🔐 步骤 7/8: 验证 NPM 登录状态..."
if npm whoami > /dev/null 2>&1; then
    echo "✅ 已登录为: $(npm whoami)"
else
    echo "⚠️  未登录，开始登录流程..."
    npm login
fi
echo ""

# 8. 发布到 NPM
echo "🚀 步骤 8/8: 发布到 NPM..."
echo ""
echo "即将发布："
echo "  包名: $PACKAGE_NAME"
echo "  旧版本: v$CURRENT_VERSION"
echo "  新版本: v$NEW_VERSION"
echo ""
read -p "确认发布到 NPM？(yes/no): " publish_confirm

if [ "$publish_confirm" = "yes" ] || [ "$publish_confirm" = "y" ]; then
    echo ""
    echo "🚀 发布中..."
    npm publish
    
    echo ""
    echo "================================"
    echo "🎉 版本更新并发布成功！"
    echo "================================"
    echo ""
    echo "📊 更新信息："
    echo "  包名: $PACKAGE_NAME"
    echo "  旧版本: v$CURRENT_VERSION"
    echo "  新版本: v$NEW_VERSION"
    echo "  时间: $(date)"
    echo ""
    echo "🔗 后续步骤："
    echo ""
    echo "1. 验证发布:"
    echo "   npm info $PACKAGE_NAME"
    echo ""
    echo "2. 测试新版本:"
    echo "   npx $PACKAGE_NAME@$NEW_VERSION"
    echo ""
    echo "3. 推送到 GitHub:"
    echo "   git push origin main --tags"
    echo ""
    echo "4. 创建 GitHub Release:"
    echo "   https://github.com/ElliotLion-ing/OpenSpec-mcp-x/releases/new"
    echo "   标签: v$NEW_VERSION"
    echo ""
    echo "5. 访问 NPM 页面:"
    echo "   https://www.npmjs.com/package/$PACKAGE_NAME"
    echo ""
else
    echo ""
    echo "❌ 已取消发布"
    echo ""
    echo "⚠️  注意: 版本号已更新但未发布"
    echo "📝 已更新的文件:"
    echo "  - package.json (v$NEW_VERSION)"
    echo "  - pyproject.toml (v$NEW_VERSION)"
    echo "  - CHANGELOG.md"
    echo ""
    echo "💡 如需回滚，运行:"
    echo "   git checkout package.json pyproject.toml CHANGELOG.md"
    echo "   git tag -d v$NEW_VERSION"
    exit 1
fi

