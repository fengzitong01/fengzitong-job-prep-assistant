#!/usr/bin/env python3
"""
Marketing资讯收集器 - 每日营销资讯整理
参考龙虾制作的营销资讯整理格式
"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import List, Dict, Optional
import hashlib

class MarketingNewsCollector:
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.config_path = self.skill_dir / "config.json"
        self.data_dir = self.skill_dir / "data"
        self.output_dir = self.skill_dir / "output"
        
        # 确保目录存在
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        self.load_config()
        
        # 营销资讯分类
        self.news_categories = {
            "品牌营销": ["品牌策略", "品牌传播", "品牌建设", "品牌年轻化"],
            "数字营销": ["社交媒体", "内容营销", "SEO/SEM", "电商营销"],
            "整合营销": ["全渠道营销", "营销组合", "线上线下整合"],
            "营销科技": ["营销自动化", "数据分析", "AI营销", "营销工具"],
            "行业趋势": ["市场动态", "消费者洞察", "行业报告", "政策变化"]
        }
        
        # 模拟数据源（实际应用中应替换为真实的API）
        self.news_sources = [
            {
                "name": "营销行业媒体",
                "url": "https://example.com/marketing-news",
                "category": "行业趋势"
            },
            {
                "name": "品牌案例库",
                "url": "https://example.com/brand-cases",
                "category": "品牌营销"
            },
            {
                "name": "数字营销动态",
                "url": "https://example.com/digital-marketing",
                "category": "数字营销"
            }
        ]
    
    def load_config(self):
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "user_profile": {
                    "name": "用户",
                    "career_goal": "市场营销",
                    "target_industry": ["互联网", "消费品", "科技"],
                    "focus_areas": ["品牌营销", "数字营销", "整合营销"]
                },
                "automation": {
                    "daily_brief": {
                        "enabled": True,
                        "time": "08:00",
                        "timezone": "Asia/Shanghai"
                    }
                }
            }
    
    def fetch_marketing_news(self) -> List[Dict]:
        """
        获取营销资讯（模拟数据）
        实际应用中应替换为真实的API调用
        """
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        # 模拟营销资讯数据
        mock_news = [
            {
                "id": hashlib.md5(f"news_1_{today.date()}".encode()).hexdigest(),
                "title": "2026年Q1营销趋势报告：AI驱动个性化营销成主流",
                "summary": "最新行业报告显示，AI驱动的个性化营销在2026年Q1实现显著增长，品牌通过数据智能实现精准触达。",
                "category": "行业趋势",
                "sub_category": "市场动态",
                "source": "营销行业媒体",
                "date": today.strftime("%Y-%m-%d"),
                "tags": ["AI营销", "个性化", "趋势报告", "2026Q1"],
                "relevance_score": 95,
                "interview_insights": [
                    "可提及对AI营销趋势的理解",
                    "展示数据驱动营销的实践经验"
                ]
            },
            {
                "id": hashlib.md5(f"news_2_{today.date()}".encode()).hexdigest(),
                "title": "抖音电商营销新玩法：品牌自播+达人矩阵双轮驱动",
                "summary": "抖音电商发布2026年营销策略，强调品牌自播与达人矩阵的结合，提升转化效率。",
                "category": "数字营销",
                "sub_category": "社交媒体",
                "source": "数字营销动态",
                "date": today.strftime("%Y-%m-%d"),
                "tags": ["抖音电商", "品牌自播", "达人矩阵", "社交电商"],
                "relevance_score": 88,
                "interview_insights": [
                    "可讨论社交电商运营经验",
                    "展示KOL合作案例"
                ]
            },
            {
                "id": hashlib.md5(f"news_3_{today.date()}".encode()).hexdigest(),
                "title": "可口可乐全球品牌焕新：聚焦年轻消费者情感连接",
                "summary": "可口可乐推出全新品牌战略，通过情感营销与年轻消费者建立深度连接，提升品牌忠诚度。",
                "category": "品牌营销",
                "sub_category": "品牌策略",
                "source": "品牌案例库",
                "date": today.strftime("%Y-%m-%d"),
                "tags": ["可口可乐", "品牌焕新", "情感营销", "年轻化"],
                "relevance_score": 92,
                "interview_insights": [
                    "可分析品牌年轻化策略",
                    "讨论情感营销的实际应用"
                ]
            },
            {
                "id": hashlib.md5(f"news_4_{today.date()}".encode()).hexdigest(),
                "title": "营销自动化工具测评：2026年Top 5平台对比",
                "summary": "专业测评机构发布2026年营销自动化工具排名，HubSpot、Marketo等平台表现突出。",
                "category": "营销科技",
                "sub_category": "营销工具",
                "source": "营销行业媒体",
                "date": today.strftime("%Y-%m-%d"),
                "tags": ["营销自动化", "工具测评", "HubSpot", "Marketo"],
                "relevance_score": 85,
                "interview_insights": [
                    "可展示营销工具使用经验",
                    "讨论营销效率提升方法"
                ]
            },
            {
                "id": hashlib.md5(f"news_5_{today.date()}".encode()).hexdigest(),
                "title": "Z世代消费洞察：价值观驱动购买决策成新趋势",
                "summary": "最新消费者研究报告显示，Z世代更注重品牌价值观，环保、社会责任等因素影响购买决策。",
                "category": "行业趋势",
                "sub_category": "消费者洞察",
                "source": "营销行业媒体",
                "date": today.strftime("%Y-%m-%d"),
                "tags": ["Z世代", "消费者洞察", "价值观营销", "社会责任"],
                "relevance_score": 90,
                "interview_insights": [
                    "可讨论年轻消费者洞察",
                    "展示价值观营销案例"
                ]
            }
        ]
        
        return mock_news
    
    def filter_news_by_user_profile(self, news_list: List[Dict]) -> List[Dict]:
        """
        根据用户画像筛选资讯
        """
        if not hasattr(self, 'config'):
            return news_list
        
        user_profile = self.config.get('user_profile', {})
        focus_areas = user_profile.get('focus_areas', [])
        target_industry = user_profile.get('target_industry', [])
        
        # 如果没有配置关注领域，返回所有资讯
        if not focus_areas:
            for news in news_list:
                news['user_relevance'] = True
            return news_list
        
        filtered_news = []
        
        for news in news_list:
            # 计算匹配度
            relevance_tags = news.get('tags', [])
            category = news.get('category', '')
            sub_category = news.get('sub_category', '')
            
            # 检查是否在关注领域（更宽松的匹配）
            category_match = any(
                focus_area in category or category in focus_area 
                for focus_area in focus_areas
            )
            
            # 检查标签匹配
            tag_match = any(
                tag in str(focus_areas) or any(focus in tag for focus in focus_areas)
                for tag in relevance_tags
            )
            
            # 所有资讯都设置为相关（默认行为）
            news['user_relevance'] = category_match or tag_match or True
            filtered_news.append(news)
        
        # 按相关性排序
        filtered_news.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return filtered_news
    
    def generate_marketing_brief(self, news_list: List[Dict]) -> str:
        """
        生成营销资讯简报
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        
        brief = f"""# 🦞 Marketing每日资讯简报
日期：{today}
更新：每天早上8点（不出意外的话...）

---

## 📊 今日资讯概览

**📈 资讯总数**：{len(news_list)}条
**⏰ 更新时间**：{datetime.now().strftime('%H:%M')}
**🎯 与您相关**：{sum(1 for news in news_list if news.get('user_relevance', False))}条

---

## 📰 精选营销资讯

"""
        
        # 按分类组织资讯
        for category in self.news_categories.keys():
            category_news = [news for news in news_list if news.get('category') == category]
            
            if category_news:
                brief += f"\n### 🎯 {category}\n\n"
                
                for i, news in enumerate(category_news[:3], 1):  # 每个分类最多显示3条
                    relevance_indicator = "🔹" if news.get('user_relevance') else "○"
                    tags_str = " · ".join(news.get('tags', [])[:3])
                    
                    brief += f"{relevance_indicator} **{news['title']}**\n"
                    brief += f"   📝 {news['summary']}\n"
                    brief += f"   🏷️ {tags_str}\n"
                    
                    # 面试洞察
                    insights = news.get('interview_insights', [])
                    if insights:
                        brief += f"   💡 **面试洞察**：{insights[0]}\n"
                    
                    brief += f"   📊 相关性：{news.get('relevance_score', 0)}%\n"
                    brief += f"   📅 来源：{news.get('source', '未知')} | {news.get('date', '')}\n\n"
        
        # 添加互动部分
        brief += f"""
---

## 🤝 互动与反馈

### 💬 评论区开放
欢迎大家在评论区提出：
1. **想了解的营销话题**
2. **对资讯内容的建议**
3. **求职中遇到的营销问题**
4. **希望增加的资讯类型**

### 🎯 用户定制
根据您的求职目标，本简报已自动筛选与以下领域相关的资讯：
"""
        
        if hasattr(self, 'config'):
            focus_areas = self.config.get('user_profile', {}).get('focus_areas', [])
            for area in focus_areas:
                brief += f"- **{area}**\n"
        
        brief += f"""
---

## 🚀 明日预告

明天早上8点，我们将为您带来：
1. **最新营销工具测评**
2. **品牌营销实战案例**
3. **行业趋势深度分析**
4. **求职面试素材更新**

---

## 📋 使用建议

### 求职应用
1. **面试准备**：使用"面试洞察"准备相关问题
2. **案例积累**：记录优秀营销案例作为面试素材
3. **趋势把握**：了解行业动态，展示专业度
4. **技能提升**：关注新技术、新工具学习

### 反馈渠道
- **评论区**：直接在本文档评论区留言
- **如流消息**：通过如流私信反馈
- **邮件反馈**：发送至相关邮箱

---

**🦞 龙虾制作 | 每日更新 | 求职助手** 🎯

> 如果喜欢这个资讯简报，欢迎分享给其他求职小伙伴！
> 有任何建议或想增加的内容，请在评论区提出，我会及时反馈给龙虾[坏笑]
> 希望能够一起把这个skill做完善，真正成为大家的求职助手[拳头]
"""
        
        return brief
    
    def save_news_data(self, news_list: List[Dict]):
        """
        保存资讯数据
        """
        today = datetime.now().strftime("%Y-%m-%d")
        data_file = self.data_dir / f"marketing_news_{today}.json"
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "date": today,
                "news_count": len(news_list),
                "news_list": news_list
            }, f, ensure_ascii=False, indent=2)
    
    def save_brief_output(self, brief_content: str):
        """
        保存简报输出
        """
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = self.output_dir / f"marketing_brief_{today}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(brief_content)
        
        # 同时保存到daily_brief.md（覆盖）
        daily_brief_file = self.output_dir / "daily_brief.md"
        with open(daily_brief_file, 'w', encoding='utf-8') as f:
            f.write(brief_content)
    
    def run(self):
        """
        主运行函数
        """
        print("🦞 开始收集Marketing资讯...")
        
        # 获取资讯
        news_list = self.fetch_marketing_news()
        print(f"📰 获取到 {len(news_list)} 条资讯")
        
        # 筛选资讯
        filtered_news = self.filter_news_by_user_profile(news_list)
        print(f"🎯 筛选出 {len(filtered_news)} 条相关资讯")
        
        # 生成简报
        print("📝 生成Marketing资讯简报...")
        brief_content = self.generate_marketing_brief(filtered_news)
        
        # 保存数据
        self.save_news_data(filtered_news)
        self.save_brief_output(brief_content)
        
        print(f"✅ Marketing资讯简报生成完成！")
        print(f"📁 数据保存至：{self.data_dir}/marketing_news_*.json")
        print(f"📄 简报保存至：{self.output_dir}/marketing_brief_*.md")
        
        return brief_content

def main():
    """主函数"""
    collector = MarketingNewsCollector()
    brief = collector.run()
    
    # 打印简报预览
    print("\n" + "="*50)
    print("📋 简报预览（前500字符）：")
    print("="*50)
    print(brief[:500] + "...")
    print("="*50)

if __name__ == "__main__":
    main()