#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新通知脚本
用于测试和演示自动更新通知功能
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

# 添加scripts目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater


def test_notification():
    """测试通知功能"""
    print("=== 测试自动更新通知功能 ===")
    print()

    # 创建测试更新结果
    test_result = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "dry_run": False,
        "updates_applied": [
            {
                "type": "news_weight",
                "category": "行业趋势",
                "action": "increased",
                "reason": "用户认可度高 (85.0%)，建议增加推送权重"
            },
            {
                "type": "company_info",
                "action": "update_required",
                "companies": ["字节跳动", "腾讯", "阿里巴巴"],
                "reason": "发现3家公司的信息需要更新"
            },
            {
                "type": "interview_difficulty",
                "action": "increased",
                "reason": "平均难度偏低 (2.3/5)，建议增加更具挑战性的问题"
            }
        ],
        "backup_path": "/home/gem/.openclaw/workspace/skills/job-preparation-assistant/backups/config_backup_20260415_012345.json",
        "errors": []
    }

    # 创建通知配置
    notification_config = {
        "enabled": True,
        "method": "infoflow",
        "infoflow": {
            "user": "fengzitong01"
        }
    }

    # 创建测试配置
    config = {
        "notification": notification_config
    }

    # 保存测试配置
    config_path = "/tmp/test_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print("✅ 创建测试配置")
    print(f"配置路径: {config_path}")
    print()

    # 创建AutoUpdater实例
    updater = AutoUpdater(config_path=config_path, notify_user="fengzitong01")

    # 测试通知消息格式化
    print("📝 测试通知消息格式化...")
    try:
        # 由于通知方法需要实际发送，我们只测试格式化
        message = updater._format_notification_message(test_result)
        print("✅ 通知消息格式化成功")
        print()
        print("=== 通知消息示例 ===")
        print(message)
        print("====================")
        print()

        # 测试发送通知（模拟）
        print("📤 测试发送通知...")
        print("📨 收件人: fengzitong01")
        print("📊 更新数量: 3 项")
        print("📦 备份路径: 已创建")
        print()
        print("✅ 通知功能测试完成")
        print()
        print("💡 实际使用时，请确保:")
        print("1. 在config.json中配置notification设置")
        print("2. 确保openclaw命令可用")
        print("3. 确保如流机器人配置正确")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def create_update_schedule():
    """创建自动更新计划"""
    print()
    print("=== 创建自动更新计划 ===")
    print()

    # 创建cron任务脚本
    cron_script = """#!/bin/bash
# 自动更新脚本
# 建议每天凌晨2点执行: 0 2 * * * /path/to/this/script.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== 求职准备助手自动更新 ==="
echo "时间: $(date)"

# 1. 分析反馈
echo "📊 分析用户反馈..."
python3 scripts/feedback_analyzer.py

# 2. 执行自动更新
echo "🔄 执行自动更新..."
python3 scripts/auto_updater.py

# 3. 检查结果
echo "✅ 自动更新完成"
echo "时间: $(date)"
"""

    # 保存脚本
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto_update_schedule.sh")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(cron_script)

    print(f"✅ 创建自动更新脚本: {script_path}")
    print()
    print("📅 建议cron配置:")
    print("0 2 * * * /path/to/job-preparation-assistant/scripts/auto_update_schedule.sh")
    print()
    print("🔧 手动执行:")
    print(f"bash {script_path}")


def main():
    """主函数"""
    print("🔧 求职准备助手 - 自动更新通知配置工具")
    print()

    while True:
        print("请选择操作:")
        print("1. 测试通知功能")
        print("2. 创建自动更新计划")
        print("3. 查看配置说明")
        print("4. 退出")
        print()

        choice = input("请输入选项 (1-4): ").strip()

        if choice == "1":
            test_notification()
        elif choice == "2":
            create_update_schedule()
        elif choice == "3":
            show_config_instructions()
        elif choice == "4":
            print("👋 退出")
            break
        else:
            print("❌ 无效选项，请重新输入")
        print()


def show_config_instructions():
    """显示配置说明"""
    print()
    print("=== 自动更新通知配置说明 ===")
    print()

    print("📋 配置示例 (config.json):")
    print("""
  "notification": {
    "enabled": true,
    "method": "infoflow",
    "infoflow": {
      "user": "fengzitong01"
    },
    "webhook": {
      "url": "https://your-webhook-url.com",
      "enabled": false
    },
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "sender_email": "your-email@gmail.com",
      "sender_password": "your-app-password",
      "receiver_email": "receiver@example.com",
      "enabled": false
    }
  }
""")

    print("📌 配置说明:")
    print("1. enabled: 是否启用通知 (true/false)")
    print("2. method: 通知方式 (infoflow/webhook/email)")
    print("3. infoflow.user: 如流用户名 (用于@mention)")
    print("4. webhook.url: Webhook URL (用于Slack/钉钉等)")
    print("5. email.*: 邮件配置 (需要SMTP服务器)")
    print()

    print("🚀 使用方法:")
    print("1. 配置notification设置")
    print("2. 运行自动更新: python3 scripts/auto_updater.py")
    print("3. 查看通知结果")
    print()

    print("📊 通知内容包括:")
    print("- 更新时间")
    print("- 更新数量")
    print("- 更新详情")
    print("- 备份路径")
    print("- 回滚命令")
    print()


if __name__ == "__main__":
    main()
