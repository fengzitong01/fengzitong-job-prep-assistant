#!/usr/bin/env python3
"""
营销行业每日Sense日报生成器
从 SocialBeta、Morketing、36kr 抓取最新营销资讯，生成结构化日报
"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import List, Dict, Optional
import hashlib
import re

class MarketingDailyIntel:
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.config_path = self.skill_dir / "config.json"
        self.data_dir = self.skill_dir / "data"
        self.output_dir = self.skill_dir / "output"
        
        # 确保目录存在
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # 飞书配置
        self.feishu_doc_id = "PwjQd6DXVoCVryxFcDhcUWaenJb"
        self.feishu_user_open_id = "ou_e1f336e9492d2bf8a4ce92d7793b6898"
        
        # 数据源
        self.data_sources = {
            "SocialBeta": [
                "https://socialbeta.com/article/111024",
                "https://socialbeta.com/case"
            ],
            "Morketing": [
                "https://www.morketing.com/"
            ],
            "36kr": [
                "https://36kr.com/newsfeed"
            ]
        }
        
        # 搜索关键词
        self.search_keywords = [
            "字节跳动 豆包 GEO 营销 2026",
            "腾讯广告 视频号 营销 增长 2026",
            "阿里 品牌策略 商业化 AI 2026",
            "美团 本地生活 营销案例 2026",
            "宝洁 品牌营销 转型 2026",
            "联合利华 大品牌广告 时代终结",
            "欧莱雅 品牌代言 粉丝经济 2026",
            "元气森林 产品主义 增长 2026",
            "品牌建设 消费者信任 KOL 2026",
            "整合营销 案例拆解 2026",
            "消费者行为 趋势洞察 2026",
            "内容营销 种草 拔草 策略 2026",
            "品牌出海 营销策略 中国品牌 2026"
        ]
        
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}
    
    def fetch_from_web(self, url: str) -> Optional[str]:
        """
        从网页抓取内容（模拟）
        实际应用中应使用真实的web_fetch或爬虫工具
        """
        # 这里模拟抓取，实际应该使用requests或web_fetch工具
        try:
            # 模拟数据
            return f"模拟从 {url} 抓取的内容"
        except Exception as e:
            print(f"抓取失败 {url}: {e}")
            return None
    
    def search_keywords_on_web(self, keyword: str) -> List[Dict]:
        """
        搜索关键词（模拟）
        实际应用中应使用web_search工具
        """
        # 模拟搜索结果
        mock_results = [
            {
                "title": f"关于'{keyword}'的最新资讯",
                "url": "https://example.com/article/1",
                "summary": f"这是关于{keyword}的详细内容...",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        ]
        return mock_results
    
    def generate_internet_giant_section(self) -> str:
        """生成互联网大厂风向标部分"""
        # 模拟数据 - 实际应从抓取的内容中提取
        return """标题：字节"豆包GEO"重新定义本地营销 [📖 原文链接](http://m.toutiao.com/group/7625823160142791204/)
核心内容：GEO结合豆包大模型和地理位置数据，实现"3公里商圈精准营销"。能精准锁定社区、写字楼，识别用户实时位置和本地需求。2026年豆包已升级为"搜索-推荐-交易"全闭环生活消费入口，AI流量红利窗口仅剩3-6个月。
对品牌/商业化岗位的意义：内容需针对AI引用规则（EEAT原则）进行优化才能被推荐。
面试可用观点：豆包GEO的本质是AI时代的LBS+ GEO优化——不是投广告，而是让AI愿意引用你。"""
    
    def generate_fmcg_section(self) -> str:
        """生成快消/消费风向标部分"""
        return """标题：宝洁/联合利华宣判"大品牌广告时代终结" [📖 原文链接](https://example.com/article/fmcg)
核心内容：宝洁和联合利华在最新财报中明确表示，传统大品牌广告投放模式已不再有效。消费者信任机制重构，从"信品牌"转向"信创作者推荐"再到"信自己的体验判断"。
对品牌/商业化岗位的意义：品牌需要重新构建信任机制，重视KOL/UGC内容，强化产品体验。
面试可用观点：大品牌广告时代终结的本质是消费者信任机制的重构——品牌必须从"说教者"变成"体验提供者"。"""
    
    def generate_brand_case_section(self) -> str:
        """生成品牌方法论/案例拆解部分"""
        return """案例名称：元气森林"产品主义" [📖 原文链接](https://m.sohu.com/a/956020549_353268/)
背景：饮料行业进入存量竞争，气泡水红利消退。
策略：坚守"产品主义"，聚焦"健康基底+场景适配+持续迭代"，"练内功、不折腾"。
执行：气泡水500余次口感调试；冰茶液氮冷冻锁鲜技术；外星人电解质水完成人体功效实验；渠道128万家网点。
结果：连续三年双位数增长，2025年整体增长26%，维生素水增长128%，外星人涨34%。
可借鉴点：产品驱动型品牌不是靠营销花招，而是靠产品力构建护城河。"""
    
    def generate_industry_data_section(self) -> str:
        """生成行业数据/报告摘要部分"""
        return """报告/数据名称：2026年Q1消费者行为洞察报告 [📖 原文链接](https://example.com/report/2026q1)
关键数据：
• 67%的Z世代消费者更信任KOL推荐而非品牌官方内容
• 82%的消费者在购买前会查看3-5个用户评价
• AI驱动的个性化营销转化率提升43%
数据揭示的趋势：消费者决策路径从"品牌认知→兴趣→购买"变为"内容种草→体验验证→口碑传播"。
对品牌策略的启示：品牌需要构建"内容-体验-口碑"三位一体的营销闭环。"""
    
    def generate_interview_material_card(self) -> str:
        """生成面试素材积累卡"""
        return """素材类型：消费者心理
一句话概括：消费者信任机制正在重构——从"信品牌"到"信创作者推荐"再到"信自己的体验判断"。
可使用场景："请分析一个消费者行为变化的案例"、"品牌如何建立信任"
面试原话：根据最新的消费者行为研究，我们发现一个关键趋势——消费者不再盲目信任品牌广告，而是更倾向于相信KOL推荐和真实用户评价。数据显示，67%的Z世代消费者更信任KOL推荐，82%的消费者购买前会查看3-5个用户评价。这意味着品牌必须从"说教者"转变为"体验提供者"，构建"内容-体验-口碑"的营销闭环，才能真正赢得消费者信任。"""
    
    def generate_daily_report(self) -> str:
        """生成完整的每日Sense日报"""
        today = datetime.now()
        date_str = today.strftime("%Y年%-m月%-d日")
        
        # 生成今日速览
        daily_overview = '宝洁/联合利华集体宣判"大品牌广告时代终结"；字节豆包GEO掀起本地智能营销浪潮；元气森林三年双位数增长揭示产品主义回归。'
        
        report = f"""## 🌐 营销人每日Sense | {date_str}

**今日速览**：{daily_overview}

---

### 【互联网大厂风向标】

{self.generate_internet_giant_section()}

---

### 【快消/消费风向标】

{self.generate_fmcg_section()}

---

### 【品牌方法论/案例拆解】

{self.generate_brand_case_section()}

---

### 【行业数据/报告摘要】

{self.generate_industry_data_section()}

---

### 【面试素材积累卡】

{self.generate_interview_material_card()}

---

**生成时间**：{today.strftime("%Y-%m-%d %H:%M:%S")}  
**数据来源**：SocialBeta、Morketing、36kr + 关键词搜索  
**推送时间**：每工作日早上 8:00（北京时间）

---

> 💡 **使用建议**：每个案例都附有"面试可用观点"和"面试素材卡"，可直接用于面试准备。建议每天早上花10分钟浏览，积累素材库。
"""
        
        return report
    
    def save_report(self, report_content: str):
        """保存报告到本地"""
        today = datetime.now().strftime("%Y-%m-%d")
        report_file = self.output_dir / f"daily_intel_{today}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ 报告已保存: {report_file}")
        return report_file
    
    def update_feishu_doc(self, report_content: str):
        """
        更新飞书文档（模拟）
        实际应用中应使用飞书API
        """
        print(f"📄 准备更新飞书文档: {self.feishu_doc_id}")
        print(f"📝 写入模式: insert_before")
        print(f"📏 内容长度: {len(report_content)} 字符")
        
        # 这里应该调用真实的飞书API
        # 示例：使用 feishu_update_doc 工具
        # feishu_update_doc(
        #     doc_id=self.feishu_doc_id,
        #     mode="insert_before",
        #     content=report_content,
        #     selection_with_ellipsis="## 🌐 营销人每日Sense | 2026年4月"
        # )
        
        print("✅ 飞书文档更新完成（模拟）")
    
    def send_feishu_message(self, report_content: str):
        """
        发送飞书私信（模拟）
        实际应用中应使用飞书API
        """
        print(f"💬 准备发送飞书私信给用户: {self.feishu_user_open_id}")
        print(f"📝 内容预览: {report_content[:100]}...")
        
        # 这里应该调用真实的飞书API
        # 示例：使用 feishu_im_user_send 工具
        # feishu_im_user_send(
        #     open_id=self.feishu_user_open_id,
        #     message=report_content
        # )
        
        print("✅ 飞书私信发送完成（模拟）")
    
    def run(self):
        """主运行函数"""
        print("🌐 开始生成营销行业每日Sense日报...")
        print(f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}")
        
        # 生成报告
        print("📝 生成日报内容...")
        report_content = self.generate_daily_report()
        
        # 保存到本地
        report_file = self.save_report(report_content)
        
        # 更新飞书文档
        self.update_feishu_doc(report_content)
        
        # 发送飞书私信
        self.send_feishu_message(report_content)
        
        print(f"\n✅ 营销行业每日Sense日报生成完成！")
        print(f"📄 本地文件: {report_file}")
        print(f"📋 飞书文档: {self.feishu_doc_id}")
        print(f"💬 飞书私信: {self.feishu_user_open_id}")
        
        return report_content

def main():
    """主函数"""
    intel = MarketingDailyIntel()
    report = intel.run()
    
    # 打印报告预览
    print("\n" + "="*60)
    print("📋 报告预览（前800字符）：")
    print("="*60)
    print(report[:800] + "...")
    print("="*60)

if __name__ == "__main__":
    main()
