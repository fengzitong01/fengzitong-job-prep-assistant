#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户反馈收集模块
收集用户对资讯、面试问题、公司库的反馈
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class FeedbackCollector:
    """用户反馈收集器"""

    def __init__(self, config_path: str = None):
        """
        初始化反馈收集器

        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, '..', 'config.json')

        self.config_path = config_path
        self.feedback_dir = os.path.join(os.path.dirname(config_path), 'feedback')
        self.feedback_file = os.path.join(self.feedback_dir, 'user_feedback.json')

        # 确保反馈目录存在
        os.makedirs(self.feedback_dir, exist_ok=True)

        # 加载现有反馈
        self.feedback = self._load_feedback()

    def _load_feedback(self) -> Dict[str, Any]:
        """加载用户反馈"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0.0",
            "last_updated": None,
            "news_feedback": [],
            "interview_feedback": [],
            "company_feedback": [],
            "suggestions": []
        }

    def _save_feedback(self):
        """保存用户反馈"""
        self.feedback["last_updated"] = datetime.now().isoformat()
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback, f, ensure_ascii=False, indent=2)

    def add_news_feedback(self, news_id: str, useful: bool,
                         category: str = None, comment: str = None):
        """
        添加资讯反馈

        Args:
            news_id: 资讯ID
            useful: 是否有用
            category: 资讯类别
            comment: 用户评论
        """
        feedback_item = {
            "id": len(self.feedback["news_feedback"]) + 1,
            "news_id": news_id,
            "useful": useful,
            "category": category,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback["news_feedback"].append(feedback_item)
        self._save_feedback()
        return feedback_item

    def add_interview_feedback(self, question_id: str, helpful: bool,
                               difficulty: int = None, comment: str = None):
        """
        添加面试问题反馈

        Args:
            question_id: 问题ID
            helpful: 是否有帮助
            difficulty: 难度评分 (1-5)
            comment: 用户评论
        """
        feedback_item = {
            "id": len(self.feedback["interview_feedback"]) + 1,
            "question_id": question_id,
            "helpful": helpful,
            "difficulty": difficulty,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback["interview_feedback"].append(feedback_item)
        self._save_feedback()
        return feedback_item

    def add_company_feedback(self, company_name: str, rating: int,
                           accurate: bool = None, comment: str = None):
        """
        添加公司信息反馈

        Args:
            company_name: 公司名称
            rating: 评分 (1-5)
            accurate: 信息是否准确
            comment: 用户评论
        """
        feedback_item = {
            "id": len(self.feedback["company_feedback"]) + 1,
            "company_name": company_name,
            "rating": rating,
            "accurate": accurate,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.feedback["company_feedback"].append(feedback_item)
        self._save_feedback()
        return feedback_item

    def add_suggestion(self, suggestion_type: str, content: str,
                      priority: int = 1):
        """
        添加用户建议

        Args:
            suggestion_type: 建议类型 (company/news/feature)
            content: 建议内容
            priority: 优先级 (1-5)
        """
        suggestion_item = {
            "id": len(self.feedback["suggestions"]) + 1,
            "type": suggestion_type,
            "content": content,
            "priority": priority,
            "status": "pending",
            "timestamp": datetime.now().isoformat()
        }
        self.feedback["suggestions"].append(suggestion_item)
        self._save_feedback()
        return suggestion_item

    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        获取反馈摘要

        Returns:
            反馈统计摘要
        """
        summary = {
            "total_feedback": 0,
            "news_feedback": {
                "total": len(self.feedback["news_feedback"]),
                "useful": sum(1 for f in self.feedback["news_feedback"] if f["useful"]),
                "not_useful": sum(1 for f in self.feedback["news_feedback"] if not f["useful"])
            },
            "interview_feedback": {
                "total": len(self.feedback["interview_feedback"]),
                "helpful": sum(1 for f in self.feedback["interview_feedback"] if f["helpful"]),
                "not_helpful": sum(1 for f in self.feedback["interview_feedback"] if not f["helpful"]),
                "avg_difficulty": None
            },
            "company_feedback": {
                "total": len(self.feedback["company_feedback"]),
                "avg_rating": None
            },
            "suggestions": {
                "total": len(self.feedback["suggestions"]),
                "pending": sum(1 for s in self.feedback["suggestions"] if s["status"] == "pending")
            }
        }

        # 计算平均难度
        difficulties = [f["difficulty"] for f in self.feedback["interview_feedback"] if f["difficulty"]]
        if difficulties:
            summary["interview_feedback"]["avg_difficulty"] = sum(difficulties) / len(difficulties)

        # 计算平均评分
        ratings = [f["rating"] for f in self.feedback["company_feedback"] if f["rating"]]
        if ratings:
            summary["company_feedback"]["avg_rating"] = sum(ratings) / len(ratings)

        summary["total_feedback"] = (
            summary["news_feedback"]["total"] +
            summary["interview_feedback"]["total"] +
            summary["company_feedback"]["total"] +
            summary["suggestions"]["total"]
        )

        return summary

    def export_feedback(self, output_path: str = None):
        """
        导出反馈数据

        Args:
            output_path: 输出文件路径
        """
        if output_path is None:
            output_path = os.path.join(self.feedback_dir, 'feedback_export.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.feedback, f, ensure_ascii=False, indent=2)

        return output_path


def main():
    """主函数 - 演示反馈收集功能"""
    collector = FeedbackCollector()

    print("=== 用户反馈收集演示 ===")
    print()

    # 添加资讯反馈
    print("1. 添加资讯反馈...")
    collector.add_news_feedback(
        news_id="news_001",
        useful=True,
        category="行业趋势",
        comment="这个资讯很有用，帮我了解了最新动态"
    )

    # 添加面试问题反馈
    print("2. 添加面试问题反馈...")
    collector.add_interview_feedback(
        question_id="interview_001",
        helpful=True,
        difficulty=3,
        comment="问题很有代表性"
    )

    # 添加公司信息反馈
    print("3. 添加公司信息反馈...")
    collector.add_company_feedback(
        company_name="字节跳动",
        rating=5,
        accurate=True,
        comment="信息准确，很有帮助"
    )

    # 添加用户建议
    print("4. 添加用户建议...")
    collector.add_suggestion(
        suggestion_type="company",
        content="希望能增加更多消费电子公司",
        priority=3
    )

    # 显示反馈摘要
    print()
    print("=== 反馈摘要 ===")
    summary = collector.get_feedback_summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 导出反馈
    print()
    print("=== 导出反馈 ===")
    export_path = collector.export_feedback()
    print(f"反馈已导出到: {export_path}")


if __name__ == "__main__":
    main()
