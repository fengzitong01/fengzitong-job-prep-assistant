#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户反馈分析模块
分析用户反馈并生成优化建议
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict


class FeedbackAnalyzer:
    """用户反馈分析器"""

    def __init__(self, feedback_path: str = None, config_path: str = None):
        """
        初始化反馈分析器

        Args:
            feedback_path: 反馈文件路径
            config_path: 配置文件路径
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if feedback_path is None:
            feedback_path = os.path.join(script_dir, '..', 'feedback', 'user_feedback.json')

        if config_path is None:
            config_path = os.path.join(script_dir, '..', 'config.json')

        self.feedback_path = feedback_path
        self.config_path = config_path
        self.feedback = self._load_feedback()
        self.config = self._load_config()

    def _load_feedback(self) -> Dict[str, Any]:
        """加载用户反馈"""
        if os.path.exists(self.feedback_path):
            with open(self.feedback_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "news_feedback": [],
            "interview_feedback": [],
            "company_feedback": [],
            "suggestions": []
        }

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def analyze_news_feedback(self) -> Dict[str, Any]:
        """
        分析资讯反馈

        Returns:
            资讯反馈分析结果
        """
        news_feedback = self.feedback.get("news_feedback", [])

        if not news_feedback:
            return {"status": "no_data", "message": "暂无资讯反馈数据"}

        # 按类别统计
        category_stats = defaultdict(lambda: {"useful": 0, "not_useful": 0, "total": 0})

        for feedback in news_feedback:
            category = feedback.get("category", "未分类")
            useful = feedback.get("useful", False)

            category_stats[category]["total"] += 1
            if useful:
                category_stats[category]["useful"] += 1
            else:
                category_stats[category]["not_useful"] += 1

        # 计算每类的有用率
        for category, stats in category_stats.items():
            stats["useful_rate"] = (
                stats["useful"] / stats["total"] * 100
                if stats["total"] > 0 else 0
            )

        # 找出最有价值的类别
        sorted_categories = sorted(
            category_stats.items(),
            key=lambda x: x[1]["useful_rate"],
            reverse=True
        )

        # 分析建议
        recommendations = []
        for category, stats in sorted_categories:
            if stats["useful_rate"] >= 70:
                recommendations.append({
                    "action": "increase_weight",
                    "category": category,
                    "reason": f"用户认可度高 ({stats['useful_rate']:.1f}%)，建议增加推送权重"
                })
            elif stats["useful_rate"] <= 30:
                recommendations.append({
                    "action": "decrease_weight",
                    "category": category,
                    "reason": f"用户认可度低 ({stats['useful_rate']:.1f}%)，建议减少推送频率"
                })

        return {
            "status": "success",
            "total_feedback": len(news_feedback),
            "category_stats": dict(category_stats),
            "top_categories": [cat for cat, _ in sorted_categories[:5]],
            "recommendations": recommendations
        }

    def analyze_interview_feedback(self) -> Dict[str, Any]:
        """
        分析面试问题反馈

        Returns:
            面试问题反馈分析结果
        """
        interview_feedback = self.feedback.get("interview_feedback", [])

        if not interview_feedback:
            return {"status": "no_data", "message": "暂无面试问题反馈数据"}

        # 统计帮助度
        helpful_count = sum(1 for f in interview_feedback if f.get("helpful", False))
        not_helpful_count = len(interview_feedback) - helpful_count

        # 计算平均难度
        difficulties = [f["difficulty"] for f in interview_feedback if f.get("difficulty")]
        avg_difficulty = sum(difficulties) / len(difficulties) if difficulties else None

        # 分析难度分布
        difficulty_distribution = defaultdict(int)
        for feedback in interview_feedback:
            difficulty = feedback.get("difficulty")
            if difficulty:
                difficulty_distribution[difficulty] += 1

        # 生成建议
        recommendations = []

        if avg_difficulty and avg_difficulty < 2.5:
            recommendations.append({
                "action": "increase_difficulty",
                "reason": f"平均难度偏低 ({avg_difficulty:.1f}/5)，建议增加更具挑战性的问题"
            })
        elif avg_difficulty and avg_difficulty > 4.0:
            recommendations.append({
                "action": "decrease_difficulty",
                "reason": f"平均难度偏高 ({avg_difficulty:.1f}/5)，建议增加基础问题"
            })

        if helpful_count / len(interview_feedback) < 0.5:
            recommendations.append({
                "action": "improve_questions",
                "reason": f"问题帮助度低 ({helpful_count}/{len(interview_feedback)})，建议优化问题质量"
            })

        return {
            "status": "success",
            "total_feedback": len(interview_feedback),
            "helpful": helpful_count,
            "not_helpful": not_helpful_count,
            "helpful_rate": helpful_count / len(interview_feedback) * 100 if interview_feedback else 0,
            "avg_difficulty": avg_difficulty,
            "difficulty_distribution": dict(difficulty_distribution),
            "recommendations": recommendations
        }

    def analyze_company_feedback(self) -> Dict[str, Any]:
        """
        分析公司信息反馈

        Returns:
            公司信息反馈分析结果
        """
        company_feedback = self.feedback.get("company_feedback", [])

        if not company_feedback:
            return {"status": "no_data", "message": "暂无公司信息反馈数据"}

        # 按公司统计评分
        company_ratings = defaultdict(list)
        company_accuracy = defaultdict(lambda: {"accurate": 0, "inaccurate": 0})

        for feedback in company_feedback:
            company = feedback.get("company_name", "未知公司")

            if feedback.get("rating"):
                company_ratings[company].append(feedback["rating"])

            if feedback.get("accurate") is not None:
                if feedback["accurate"]:
                    company_accuracy[company]["accurate"] += 1
                else:
                    company_accuracy[company]["inaccurate"] += 1

        # 计算每家公司的平均评分
        company_avg_ratings = {}
        for company, ratings in company_ratings.items():
            company_avg_ratings[company] = {
                "avg_rating": sum(ratings) / len(ratings),
                "rating_count": len(ratings)
            }

        # 找出评分最高的公司
        top_rated = sorted(
            company_avg_ratings.items(),
            key=lambda x: x[1]["avg_rating"],
            reverse=True
        )[:5]

        # 找出信息不准确的反馈
        inaccurate_info = []
        for company, stats in company_accuracy.items():
            if stats["inaccurate"] > 0:
                inaccurate_info.append({
                    "company": company,
                    "accurate_count": stats["accurate"],
                    "inaccurate_count": stats["inaccurate"],
                    "accuracy_rate": stats["accurate"] / (stats["accurate"] + stats["inaccurate"]) * 100
                })

        # 生成建议
        recommendations = []

        if inaccurate_info:
            recommendations.append({
                "action": "update_company_info",
                "reason": f"发现{len(inaccurate_info)}家公司的信息需要更新",
                "companies": [item["company"] for item in inaccurate_info]
            })

        low_rated = [company for company, data in company_avg_ratings.items() if data["avg_rating"] < 3]
        if low_rated:
            recommendations.append({
                "action": "improve_company_info",
                "reason": f"发现{len(low_rated)}家公司的信息评分较低",
                "companies": low_rated
            })

        return {
            "status": "success",
            "total_feedback": len(company_feedback),
            "company_ratings": company_avg_ratings,
            "top_rated_companies": top_rated,
            "inaccurate_info": inaccurate_info,
            "recommendations": recommendations
        }

    def analyze_suggestions(self) -> Dict[str, Any]:
        """
        分析用户建议

        Returns:
            用户建议分析结果
        """
        suggestions = self.feedback.get("suggestions", [])

        if not suggestions:
            return {"status": "no_data", "message": "暂无用户建议"}

        # 按类型统计
        type_stats = defaultdict(int)
        pending_suggestions = []

        for suggestion in suggestions:
            suggestion_type = suggestion.get("type", "其他")
            type_stats[suggestion_type] += 1

            if suggestion.get("status") == "pending":
                pending_suggestions.append(suggestion)

        # 按优先级排序
        high_priority = [s for s in pending_suggestions if s.get("priority", 1) >= 4]
        medium_priority = [s for s in pending_suggestions if 2 <= s.get("priority", 1) < 4]
        low_priority = [s for s in pending_suggestions if s.get("priority", 1) < 2]

        return {
            "status": "success",
            "total_suggestions": len(suggestions),
            "pending": len(pending_suggestions),
            "type_distribution": dict(type_stats),
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority
        }

    def generate_optimization_report(self) -> Dict[str, Any]:
        """
        生成优化报告

        Returns:
            综合优化报告
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_feedback": 0,
                "feedback_types": {}
            },
            "analysis": {
                "news": self.analyze_news_feedback(),
                "interview": self.analyze_interview_feedback(),
                "company": self.analyze_company_feedback(),
                "suggestions": self.analyze_suggestions()
            },
            "recommendations": []
        }

        # 计算总反馈数
        report["summary"]["total_feedback"] = (
            len(self.feedback.get("news_feedback", [])) +
            len(self.feedback.get("interview_feedback", [])) +
            len(self.feedback.get("company_feedback", [])) +
            len(self.feedback.get("suggestions", []))
        )

        # 收集所有建议
        for analysis in report["analysis"].values():
            if isinstance(analysis, dict) and "recommendations" in analysis:
                report["recommendations"].extend(analysis["recommendations"])

        # 按优先级排序建议
        priority_map = {"increase_weight": 5, "update_company_info": 4, "improve_questions": 3}
        report["recommendations"].sort(
            key=lambda x: priority_map.get(x.get("action", ""), 0),
            reverse=True
        )

        return report

    def save_optimization_report(self, output_path: str = None):
        """
        保存优化报告

        Args:
            output_path: 输出文件路径
        """
        if output_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, '..', 'feedback', 'optimization_report.json')

        report = self.generate_optimization_report()

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return output_path, report


def main():
    """主函数 - 演示反馈分析功能"""
    analyzer = FeedbackAnalyzer()

    print("=== 用户反馈分析演示 ===")
    print()

    # 分析资讯反馈
    print("1. 资讯反馈分析...")
    news_analysis = analyzer.analyze_news_feedback()
    print(json.dumps(news_analysis, ensure_ascii=False, indent=2))
    print()

    # 分析面试问题反馈
    print("2. 面试问题反馈分析...")
    interview_analysis = analyzer.analyze_interview_feedback()
    print(json.dumps(interview_analysis, ensure_ascii=False, indent=2))
    print()

    # 分析公司信息反馈
    print("3. 公司信息反馈分析...")
    company_analysis = analyzer.analyze_company_feedback()
    print(json.dumps(company_analysis, ensure_ascii=False, indent=2))
    print()

    # 分析用户建议
    print("4. 用户建议分析...")
    suggestions_analysis = analyzer.analyze_suggestions()
    print(json.dumps(suggestions_analysis, ensure_ascii=False, indent=2))
    print()

    # 生成优化报告
    print("5. 生成优化报告...")
    output_path, report = analyzer.save_optimization_report()
    print(f"优化报告已保存到: {output_path}")
    print(f"总共收集了 {report['summary']['total_feedback']} 条反馈")
    print(f"生成了 {len(report['recommendations'])} 条优化建议")


if __name__ == "__main__":
    main()
