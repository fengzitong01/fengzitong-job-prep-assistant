#!/bin/bash
# 求职准备助手 - 卸载脚本
# 作者: 冯梓桐
# 版本: 1.0.0

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示卸载信息
echo "================================================================================"
echo "                                                                              "
echo "                      🎯 求职准备助手 - 卸载程序                              "
echo "                                                                              "
echo "================================================================================"
echo ""

# 设置Skill目录
SKILL_NAME="job-preparation-assistant"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"

# 检查是否已安装
if [ ! -d "$SKILL_DIR" ]; then
    log_warning "求职准备助手未安装"
    exit 0
fi

log_info "安装目录: $SKILL_DIR"

# 确认卸载
log_warning "即将卸载求职准备助手，这将删除所有相关文件"
read -p "是否继续？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "卸载已取消"
    exit 0
fi

# 备份配置文件（如果存在）
if [ -f "$SKILL_DIR/config.json" ]; then
    BACKUP_DIR="$HOME/.openclaw/backups"
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/job-preparation-assistant_config_$(date +%Y%m%d_%H%M%S).json"
    cp "$SKILL_DIR/config.json" "$BACKUP_FILE"
    log_success "配置文件已备份到: $BACKUP_FILE"
fi

# 询问是否删除定时任务
if crontab -l 2>/dev/null | grep -q "job-preparation-assistant"; then
    read -p "是否删除定时任务？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        crontab -l 2>/dev/null | grep -v "job-preparation-assistant" | crontab -
        log_success "定时任务已删除 ✓"
    fi
fi

# 询问是否删除输出文件
if [ -d "$SKILL_DIR/output" ]; then
    OUTPUT_COUNT=$(find "$SKILL_DIR/output" -type f | wc -l)
    if [ "$OUTPUT_COUNT" -gt 0 ]; then
        read -p "是否删除输出文件（$OUTPUT_COUNT个文件）？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "删除输出文件..."
            rm -rf "$SKILL_DIR/output"/*
            log_success "输出文件已删除 ✓"
        else
            log_info "保留输出文件"
        fi
    fi
fi

# 删除Skill目录
log_info "删除Skill文件..."
rm -rf "$SKILL_DIR"
log_success "Skill文件已删除 ✓"

# 显示完成信息
echo ""
echo "================================================================================"
echo "                                                                              "
echo "                      ✅ 卸载完成！                                           "
echo "                                                                              "
echo "================================================================================"
echo ""
log_success "求职准备助手已成功卸载！"
echo ""
if [ -f "$BACKUP_FILE" ]; then
    echo "📦 配置文件已备份到: $BACKUP_FILE"
    echo "   如需重新安装，可以使用此配置文件"
fi
echo ""
echo "💡 如需重新安装，请运行:"
echo "   git clone https://github.com/fengzitong/job-preparation-assistant.git"
echo "   cd job-preparation-assistant"
echo "   bash install.sh"
echo ""
echo "================================================================================"
