#!/bin/bash
# 求职准备助手 - 安装脚本
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

# 显示欢迎信息
echo "================================================================================"
echo "                                                                              "
echo "                      🎯 求职准备助手 - 安装程序                              "
echo "                                                                              "
echo "                         版本: 1.0.0                                          "
echo "                         作者: 冯梓桐                                         "
echo "                                                                              "
echo "================================================================================"
echo ""

# 检查操作系统
log_info "检查系统环境..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="MacOS"
else
    log_warning "未知操作系统: $OSTYPE"
    OS="Unknown"
fi
log_success "检测到操作系统: $OS"

# 检查Python版本
log_info "检查Python版本..."
if ! command -v python3 &> /dev/null; then
    log_error "未找到Python3，请先安装Python 3.8或更高版本"
    log_info "安装方法: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d '.' -f 1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d '.' -f 2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    log_error "Python版本过低: $PYTHON_VERSION，需要Python 3.8或更高版本"
    exit 1
fi
log_success "Python版本: $PYTHON_VERSION ✓"

# 检查pip
log_info "检查pip..."
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    log_error "未找到pip，请先安装pip"
    exit 1
fi
log_success "pip已安装 ✓"

# 设置Skill目录
SKILL_NAME="job-preparation-assistant"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"

log_info "安装目录: $SKILL_DIR"

# 检查是否已安装
if [ -d "$SKILL_DIR" ]; then
    log_warning "检测到已有安装，将进行更新..."
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "安装已取消"
        exit 0
    fi
    # 备份旧配置
    if [ -f "$SKILL_DIR/config.json" ]; then
        BACKUP_FILE="$SKILL_DIR/config.json.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$SKILL_DIR/config.json" "$BACKUP_FILE"
        log_success "已备份配置文件到: $BACKUP_FILE"
    fi
fi

# 创建目录
log_info "创建目录结构..."
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/scripts"
mkdir -p "$SKILL_DIR/templates"
mkdir -p "$SKILL_DIR/data"
mkdir -p "$SKILL_DIR/output"
mkdir -p "$SKILL_DIR/examples"
log_success "目录创建完成 ✓"

# 复制文件
log_info "复制Skill文件..."

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 复制所有文件
if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/"
    log_success "复制 SKILL.md ✓"
fi

if [ -f "$SCRIPT_DIR/package.json" ]; then
    cp "$SCRIPT_DIR/package.json" "$SKILL_DIR/"
    log_success "复制 package.json ✓"
fi

if [ -f "$SCRIPT_DIR/README.md" ]; then
    cp "$SCRIPT_DIR/README.md" "$SKILL_DIR/"
    log_success "复制 README.md ✓"
fi

if [ -f "$SCRIPT_DIR/config.json" ]; then
    cp "$SCRIPT_DIR/config.json" "$SKILL_DIR/"
    log_success "复制 config.json ✓"
fi

# 复制scripts
if [ -d "$SCRIPT_DIR/scripts" ]; then
    cp -r "$SCRIPT_DIR/scripts/"*.py "$SKILL_DIR/scripts/" 2>/dev/null || true
    log_success "复制脚本文件 ✓"
fi

# 复制templates
if [ -d "$SCRIPT_DIR/templates" ]; then
    cp -r "$SCRIPT_DIR/templates/"*.md "$SKILL_DIR/templates/" 2>/dev/null || true
    log_success "复制模板文件 ✓"
fi

# 复制examples
if [ -d "$SCRIPT_DIR/examples" ]; then
    cp -r "$SCRIPT_DIR/examples/"*.json "$SKILL_DIR/examples/" 2>/dev/null || true
    log_success "复制示例文件 ✓"
fi

# 设置权限
log_info "设置文件权限..."
chmod +x "$SKILL_DIR/scripts/"*.py 2>/dev/null || true
log_success "权限设置完成 ✓"

# 安装Python依赖
log_info "安装Python依赖包..."
DEPENDENCIES="requests python-dateutil"
for dep in $DEPENDENCIES; do
    if python3 -c "import $dep" 2>/dev/null; then
        log_success "$dep 已安装 ✓"
    else
        log_info "安装 $dep..."
        pip3 install $dep --quiet 2>/dev/null || pip install $dep --quiet 2>/dev/null || {
            log_warning "无法安装 $dep，某些功能可能受限"
        }
    fi
done

# 创建默认配置（如果不存在）
if [ ! -f "$SKILL_DIR/config.json" ]; then
    if [ -f "$SKILL_DIR/examples/config.example.json" ]; then
        cp "$SKILL_DIR/examples/config.example.json" "$SKILL_DIR/config.json"
        log_success "创建默认配置文件 ✓"
    fi
fi

# 创建定时任务（可选）
log_info "配置自动化任务..."
read -p "是否创建每日定时任务（每天早上8:00运行）？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    CRON_JOB="0 8 * * * python3 $SKILL_DIR/scripts/daily_brief.py"
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "job-preparation-assistant"; then
        log_warning "定时任务已存在，跳过创建"
    else
        # 添加定时任务
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        log_success "定时任务创建成功 ✓"
        log_info "每天早上8:00将自动运行每日简报"
    fi
fi

# 显示安装信息
echo ""
echo "================================================================================"
echo "                                                                              "
echo "                      ✅ 安装完成！                                           "
echo "                                                                              "
echo "================================================================================"
echo ""
log_success "求职准备助手已成功安装！"
echo ""
echo "📚 使用说明:"
echo "   - 查看文档: cat $SKILL_DIR/README.md"
echo "   - 编辑配置: nano $SKILL_DIR/config.json"
echo "   - 运行测试: python3 $SKILL_DIR/scripts/daily_brief.py"
echo ""
echo "🎯 快速开始:"
echo "   1. 编辑配置文件: nano $SKILL_DIR/config.json"
echo "   2. 设置你的求职目标、目标公司等信息"
echo "   3. 运行每日简报: python3 $SKILL_DIR/scripts/daily_brief.py"
echo ""
echo "📖 文档链接:"
echo "   - GitHub: https://github.com/fengzitong/job-preparation-assistant"
echo "   - 问题反馈: https://github.com/fengzitong/job-preparation-assistant/issues"
echo ""
echo "💡 提示: 首次使用请先编辑config.json配置文件！"
echo ""
echo "================================================================================"
