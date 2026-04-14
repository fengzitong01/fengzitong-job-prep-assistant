#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新模块
根据反馈分析结果自动更新配置文件
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Any


class AutoUpdater:
    """自动更新器"""

    def __init__(self, config_path: str = None, feedback_path: str = None):
        """
        初始化自动更新器

        Args:
            config_path: 配置文件路径
            feedback_path: 反馈文件路径
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if config_path is None:
            config_path = os.path.join(script_dir, '..', 'config.json')

        if feedback_path is None:
            feedback_path = os.path.join(script_dir, '..', 'feedback', 'optimization_report.json')

        self.config_path = config_path
        self.feedback_path = feedback_path
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

        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))

        return result

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
