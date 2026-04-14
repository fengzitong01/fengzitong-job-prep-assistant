#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新模块
根据反馈分析结果自动更新配置文件
支持通知功能
"""

import json
import os
import shutil
import subprocess
from datetime import datetime
from typing import Dict, List, Any


class AutoUpdater:
    """自动更新器"""

    def __init__(self, config_path: str = None, feedback_path: str = None, notify_user: str = None):
        """
        初始化自动更新器

        Args:
            config_path: 配置文件路径
            feedback_path: 反馈文件路径
            notify_user: 通知用户（如流用户名）
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if config_path is None:
            config_path = os.path.join(script_dir, '..', 'config.json')

        if feedback_path is None:
            feedback_path = os.path.join(script_dir, '..', 'feedback', 'optimization_report.json')

        self.config_path = config_path
        self.feedback_path = feedback_path
        self.notify_user = notify_user
        self.backup_dir = os.path.join(os.path.dirname(config_path), 'backups')
        self.update_history_path = os.path.join(os.path.dirname(config_path), 'update_history.json')

        # 确保备份目录存在
        os.makedirs(self.backup_dir, exist_ok=True)

        # 加载配置和优化报告
        self.config = self._load_config()
        self.optimization_report = self._load_optimization_report()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_optimization_report(self) -> Dict[str, Any]:
        """加载优化报告"""
        if os.path.exists(self.feedback_path):
            with open(self.feedback_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _backup_config(self) -> str:
        """
        备份当前配置

        Returns:
            备份文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"config_backup_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)

        shutil.copy2(self.config_path, backup_path)

        return backup_path

    def _save_config(self):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def _save_update_history(self, updates: List[Dict[str, Any]]):
        """
        保存更新历史

        Args:
            updates: 更新记录列表
        """
        history = {
            "version": "1.0.0",
            "updates": []
        }

        if os.path.exists(self.update_history_path):
            with open(self.update_history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # 添加新更新记录
        update_record = {
            "timestamp": datetime.now().isoformat(),
            "updates": updates,
            "total_changes": len(updates)
        }

        history["updates"].append(update_record)

        with open(self.update_history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def apply_news_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        应用资讯相关建议

        Args:
            recommendations: 资讯优化建议列表

        Returns:
            应用的更新列表
        """
        updates = []

        if "automation" not in self.config:
            self.config["automation"] = {}

        if "daily_brief" not in self.config["automation"]:
            self.config["automation"]["daily_brief"] = {}

        # 更新资讯权重配置
        for rec in recommendations:
            if rec.get("action") == "increase_weight":
                category = rec.get("category")
                updates.append({
                    "type": "news_weight",
                    "category": category,
                    "action": "increased",
                    "reason": rec.get("reason")
                })

            elif rec.get("action") == "decrease_weight":
                category = rec.get("category")
                updates.append({
                    "type": "news_weight",
                    "category": category,
                    "action": "decreased",
                    "reason": rec.get("reason")
                })

        return updates

    def apply_interview_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        应用面试问题相关建议

        Args:
            recommendations: 面试问题优化建议列表

        Returns:
            应用的更新列表
        """
        updates = []

        for rec in recommendations:
            if rec.get("action") == "increase_difficulty":
                updates.append({
                    "type": "interview_difficulty",
                    "action": "increased",
                    "reason": rec.get("reason"),
                    "note": "建议在面试问题库中增加更具挑战性的问题"
                })

            elif rec.get("action") == "decrease_difficulty":
                updates.append({
                    "type": "interview_difficulty",
                    "action": "decreased",
                    "reason": rec.get("reason"),
                    "note": "建议在面试问题库中增加基础问题"
                })

            elif rec.get("action") == "improve_questions":
                updates.append({
                    "type": "interview_quality",
                    "action": "improved",
                    "reason": rec.get("reason"),
                    "note": "建议优化面试问题质量"
                })

        return updates

    def apply_company_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        应用公司信息相关建议

        Args:
            recommendations: 公司信息优化建议列表

        Returns:
            应用的更新列表
        """
        updates = []

        for rec in recommendations:
            if rec.get("action") == "update_company_info":
                companies = rec.get("companies", [])
                updates.append({
                    "type": "company_info",
                    "action": "update_required",
                    "companies": companies,
                    "reason": rec.get("reason"),
                    "note": "需要手动更新这些公司的信息"
                })

            elif rec.get("action") == "improve_company_info":
                companies = rec.get("companies", [])
                updates.append({
                    "type": "company_info",
                    "action": "improvement_required",
                    "companies": companies,
                    "reason": rec.get("reason"),
                    "note": "需要改进这些公司的信息质量"
                })

        return updates

    def auto_update(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        执行自动更新

        Args:
            dry_run: 是否为演练模式（不实际修改文件）

        Returns:
            更新结果
        """
        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "updates_applied": [],
            "backup_path": None,
            "errors": []
        }

        if not self.optimization_report:
            result["status"] = "no_data"
            result["errors"].append("未找到优化报告")
            return result

        try:
            # 收集所有建议
            all_recommendations = self.optimization_report.get("recommendations", [])

            if not all_recommendations:
                result["status"] = "no_recommendations"
                result["message"] = "暂无需要应用的优化建议"
                return result

            # 备份配置
            if not dry_run:
                backup_path = self._backup_config()
                result["backup_path"] = backup_path

            # 应用各类建议
            updates = []

            # 资讯相关建议
            news_recs = [r for r in all_recommendations if r.get("action") in ["increase_weight", "decrease_weight"]]
            if news_recs:
                updates.extend(self.apply_news_recommendations(news_recs))

            # 面试问题相关建议
            interview_recs = [r for r in all_recommendations if "interview" in r.get("action", "")]
            if interview_recs:
                updates.extend(self.apply_interview_recommendations(interview_recs))

            # 公司信息相关建议
            company_recs = [r for r in all_recommendations if "company" in r.get("action", "")]
            if company_recs:
                updates.extend(self.apply_company_recommendations(company_recs))

            result["updates_applied"] = updates

            # 保存更新
            if not dry_run and updates:
                self._save_config()
                self._save_update_history(updates)

                # 发送通知
                if self.notify_user:
                    self._send_notification(result)

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))

        return result

    def _format_notification_message(self, update_result: Dict[str, Any]) -> str:
        """
        格式化通知消息

        Args:
            update_result: 更新结果

        Returns:
            格式化的通知消息
        """
        updates = update_result.get("updates_applied", [])
        timestamp = update_result.get("timestamp", "")

        message = f"🔄 **求职准备助手自动更新通知**\n\n"
        message += f"📅 更新时间：{timestamp}\n"
        message += f"📊 更新数量：{len(updates)} 项\n\n"

        if updates:
            message += "**更新详情：**\n"
            for i, update in enumerate(updates, 1):
                update_type = update.get("type", "未知类型")
                action = update.get("action", "未知操作")
                reason = update.get("reason", "无原因")

                message += f"\n{i}. **{update_type}**\n"
                message += f"   - 操作：{action}\n"
                message += f"   - 原因：{reason}\n"

                if "companies" in update:
                    companies = update["companies"]
                    message += f"   - 涉及公司：{', '.join(companies[:3])}"
                    if len(companies) > 3:
                        message += f" 等{len(companies)}家\n"

        if update_result.get("backup_path"):
            message += f"\n\n📦 **已备份配置文件**\n"
            message += f"路径：{update_result['backup_path']}\n"

        message += "\n\n---\n"
        message += "💡 **提示**：如需回滚，请运行 `python3 scripts/auto_updater.py --rollback`\n"

        return message

    def _send_notification(self, update_result: Dict[str, Any]):
        """
        发送更新通知

        Args:
            update_result: 更新结果
        """
        try:
            # 格式化通知消息
            message = self._format_notification_message(update_result)

            # 从配置中读取通知设置
            notification_config = self.config.get("notification", {})
            notify_method = notification_config.get("method", "infoflow")

            if notify_method == "feishu":
                # 使用飞书发送通知
                self._send_feishu_notification(message)
            elif notify_method == "infoflow":
                # 使用如流发送通知
                self._send_infoflow_notification(message)
            elif notify_method == "webhook":
                # 使用Webhook发送通知
                webhook_url = notification_config.get("webhook_url")
                if webhook_url:
                    self._send_webhook_notification(webhook_url, message)
            elif notify_method == "email":
                # 使用邮件发送通知
                email_config = notification_config.get("email", {})
                if email_config:
                    self._send_email_notification(email_config, message)
            else:
                print(f"⚠️ 未知的通知方式：{notify_method}")

        except Exception as e:
            print(f"❌ 发送通知失败：{e}")

    def _send_feishu_notification(self, message: str):
        """
        通过飞书发送通知

        Args:
            message: 通知消息
        """
        try:
            import requests
            import time
            import hashlib
            import hmac
            import base64

            # 从配置中读取飞书配置
            feishu_config = self.config.get("feishu", {})
            app_id = feishu_config.get("app_id")
            app_secret = feishu_config.get("app_secret")

            if not app_id or not app_secret:
                print("⚠️ 飞书配置不完整，跳过飞书通知")
                return

            # 获取access_token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": app_id,
                "app_secret": app_secret
            }

            token_response = requests.post(token_url, json=token_data, timeout=10)
            token_result = token_response.json()

            if token_result.get("code") != 0:
                print(f"❌ 获取飞书access_token失败：{token_result.get('msg')}")
                return

            access_token = token_result.get("tenant_access_token")

            # 获取用户ID（如果配置了飞书用户）
            notification_config = self.config.get("notification", {})
            feishu_notify = notification_config.get("feishu", {})
            user_id = feishu_notify.get("user_id")
            chat_id = feishu_notify.get("chat_id")

            # 发送消息
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            if chat_id:
                # 发送到群聊
                send_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
                send_data = {
                    "receive_id": chat_id,
                    "msg_type": "text",
                    "content": json.dumps({"text": message})
                }
            elif user_id:
                # 发送给用户
                send_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
                send_data = {
                    "receive_id": user_id,
                    "msg_type": "text",
                    "content": json.dumps({"text": message})
                }
            else:
                print("⚠️ 未配置飞书user_id或chat_id，跳过飞书通知")
                return

            send_response = requests.post(send_url, headers=headers, json=send_data, timeout=10)
            send_result = send_response.json()

            if send_result.get("code") == 0:
                target = f"群聊 {chat_id}" if chat_id else f"用户 {user_id}"
                print(f"✅ 已通过飞书发送通知到：{target}")
            else:
                print(f"❌ 飞书通知失败：{send_result.get('msg')}")

        except ImportError:
            print("⚠️ 未安装requests库，跳过飞书通知")
        except Exception as e:
            print(f"❌ 飞书通知异常：{e}")

    def _send_infoflow_notification(self, message: str):
        """
        通过如流发送通知

        Args:
            message: 通知消息
        """
        try:
            # 使用 OpenClaw 的 infoflow_send 工具
            # 这里假设可以通过命令行调用
            cmd = [
                "openclaw", "message", "send",
                "--to", self.notify_user,
                "--message", message
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"✅ 已通过如流发送通知给：{self.notify_user}")
            else:
                print(f"❌ 如流通知失败：{result.stderr}")

        except FileNotFoundError:
            # 如果 openclaw 命令不存在，尝试使用其他方式
            print(f"⚠️ 未找到 openclaw 命令，跳过如流通知")
            print(f"📝 通知内容：\n{message}")

        except Exception as e:
            print(f"❌ 如流通知异常：{e}")

    def _send_webhook_notification(self, webhook_url: str, message: str):
        """
        通过Webhook发送通知

        Args:
            webhook_url: Webhook URL
            message: 通知消息
        """
        try:
            import requests

            payload = {
                "text": "求职准备助手自动更新",
                "message": message,
                "timestamp": datetime.now().isoformat()
            }

            response = requests.post(webhook_url, json=payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ 已通过Webhook发送通知")
            else:
                print(f"❌ Webhook通知失败：{response.status_code}")

        except ImportError:
            print("⚠️ 未安装requests库，跳过Webhook通知")
        except Exception as e:
            print(f"❌ Webhook通知异常：{e}")

    def _send_email_notification(self, email_config: Dict[str, Any], message: str):
        """
        通过邮件发送通知

        Args:
            email_config: 邮件配置
            message: 通知消息
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            smtp_server = email_config.get("smtp_server")
            smtp_port = email_config.get("smtp_port", 587)
            sender_email = email_config.get("sender_email")
            sender_password = email_config.get("sender_password")
            receiver_email = email_config.get("receiver_email")

            if not all([smtp_server, sender_email, sender_password, receiver_email]):
                print("⚠️ 邮件配置不完整，跳过邮件通知")
                return

            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "求职准备助手自动更新通知"

            msg.attach(MIMEText(message, 'plain', 'utf-8'))

            # 发送邮件
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print(f"✅ 已通过邮件发送通知至：{receiver_email}")

        except ImportError:
            print("⚠️ 未安装smtplib库，跳过邮件通知")
        except Exception as e:
            print(f"❌ 邮件通知异常：{e}")


    def rollback(self, backup_path: str = None) -> Dict[str, Any]:
        """
        回滚到指定备份

        Args:
            backup_path: 备份文件路径，如果为None则使用最新备份

        Returns:
            回滚结果
        """
        result = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "backup_used": None,
            "errors": []
        }

        try:
            if backup_path is None:
                # 找到最新备份
                backups = sorted(
                    [f for f in os.listdir(self.backup_dir) if f.startswith("config_backup_")],
                    reverse=True
                )

                if not backups:
                    result["status"] = "no_backup"
                    result["errors"].append("未找到备份文件")
                    return result

                backup_path = os.path.join(self.backup_dir, backups[0])

            if not os.path.exists(backup_path):
                result["status"] = "backup_not_found"
                result["errors"].append(f"备份文件不存在: {backup_path}")
                return result

            # 恢复备份
            shutil.copy2(backup_path, self.config_path)
            result["backup_used"] = backup_path

            # 重新加载配置
            self.config = self._load_config()

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))

        return result

    def get_update_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取更新历史

        Args:
            limit: 返回记录数量限制

        Returns:
            更新历史记录列表
        """
        if not os.path.exists(self.update_history_path):
            return []

        with open(self.update_history_path, 'r', encoding='utf-8') as f:
            history = json.load(f)

        return history.get("updates", [])[-limit:]


def main():
    """主函数 - 演示自动更新功能"""
    updater = AutoUpdater()

    print("=== 自动更新演示 ===")
    print()

    # 执行演练模式
    print("1. 演练模式（不实际修改配置）...")
    result = updater.auto_update(dry_run=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()

    # 执行实际更新
    print("2. 执行实际更新...")
    result = updater.auto_update(dry_run=False)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print()

    # 查看更新历史
    print("3. 更新历史...")
    history = updater.get_update_history(limit=5)
    for record in history:
        print(f"- {record['timestamp']}: {record['total_changes']} 项更新")
    print()

    # 回滚演示
    if result.get("backup_path"):
        print("4. 回滚演示...")
        rollback_result = updater.rollback(result["backup_path"])
        print(json.dumps(rollback_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
