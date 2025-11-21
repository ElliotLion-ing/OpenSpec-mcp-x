#!/bin/bash
# OpenSpec MCP - 一键发布到 NPM
# 用于首次发布或重新发布当前版本

set -e  # 遇到错误立即退出

echo "🚀 OpenSpec MCP - NPM 发布脚本"
echo "================================"
echo ""

# 获取当前版本号
VERSION=$(node -p "require('./package.json').version")
PACKAGE_NAME=$(node -p "require('./package.json').name")

echo "📦 包名: $PACKAGE_NAME"
echo "📌 当前版本: v$VERSION"
echo ""

# 1. 清理临时文件
echo "🧹 步骤 1/6: 清理临时文件..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
rm -rf src/openspec_mcp.egg-info/ 2>/dev/null || true
rm -f *.tgz 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 2. 验证登录状态
echo "🔐 步骤 2/6: 验证 NPM 登录状态..."
if npm whoami > /dev/null 2>&1; then
    echo "✅ 已登录为: $(npm whoami)"
else
    echo "⚠️  未登录，开始登录流程..."
    npm login
fi
echo ""

# 3. 检查包名状态
echo "🔍 步骤 3/6: 检查包状态..."
if npm info $PACKAGE_NAME > /dev/null 2>&1; then
    PUBLISHED_VERSION=$(npm info $PACKAGE_NAME version 2>/dev/null)
    echo "ℹ️  包 '$PACKAGE_NAME' 已存在"
    echo "📌 已发布版本: v$PUBLISHED_VERSION"
    echo "📌 当前版本: v$VERSION"
    
    if [ "$PUBLISHED_VERSION" = "$VERSION" ]; then
        echo ""
        echo "⚠️  警告: 版本 v$VERSION 已发布到 NPM"
        echo ""
        read -p "是否要继续（这会失败）？(yes/no): " confirm
        if [ "$confirm" != "yes" ] && [ "$confirm" != "y" ]; then
            echo "❌ 已取消发布"
            echo ""
            echo "💡 提示: 使用 ./update.sh 来更新版本并发布"
            exit 1
        fi
    fi
else
    echo "✅ 包名 '$PACKAGE_NAME' 可用（首次发布）"
fi
echo ""

# 4. 预览包内容
echo "📦 步骤 4/6: 预览包内容..."
echo "--- 将要发布的文件 ---"
npm pack --dry-run 2>&1 | grep -E "npm notice" | head -20
echo ""

# 5. 运行测试（如果有）
echo "🧪 步骤 5/6: 运行测试..."
if [ -f "package.json" ] && grep -q '"test":' package.json; then
    echo "运行 npm test..."
    npm test || {
        echo "⚠️  测试失败，但继续发布"
    }
else
    echo "⏭️  跳过测试（未配置）"
fi
echo ""

# 6. 确认发布
echo "🎯 步骤 6/6: 准备发布..."
echo ""
echo "即将发布："
echo "  包名: $PACKAGE_NAME"
echo "  版本: v$VERSION"
echo ""
read -p "确认发布到 NPM？(yes/no): " confirm

if [ "$confirm" = "yes" ] || [ "$confirm" = "y" ]; then
    echo ""
    echo "🚀 发布中..."
    npm publish
    
    echo ""
    echo "================================"
    echo "🎉 发布成功！"
    echo "================================"
    echo ""
    echo "📊 发布信息："
    echo "  包名: $PACKAGE_NAME"
    echo "  版本: v$VERSION"
    echo "  时间: $(date)"
    echo ""
    echo "🔗 后续步骤："
    echo ""
    echo "1. 验证发布:"
    echo "   npm info $PACKAGE_NAME"
    echo ""
    echo "2. 测试安装:"
    echo "   npx $PACKAGE_NAME@latest"
    echo ""
    echo "3. 访问 NPM 页面:"
    echo "   https://www.npmjs.com/package/$PACKAGE_NAME"
    echo ""
    echo "4. 推送到 GitHub:"
    echo "   git push origin main --tags"
    echo ""
    echo "5. 创建 GitHub Release:"
    echo "   https://github.com/ElliotLion-ing/OpenSpec-mcp-x/releases/new"
    echo ""
else
    echo ""
    echo "❌ 已取消发布"
    exit 1
fi

