#!/usr/bin/env python3
"""
求职准备助手 - 每日简报生成
"""

import json
import os
from datetime import datetime
from pathlib import Path

class JobPrepDailyBrief:
    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.config_path = self.skill_dir / "config.json"
        self.output_dir = self.skill_dir / "output"
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def generate_daily_brief(self):
        """生成每日求职简报"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 尝试读取Marketing资讯简报
        marketing_brief_path = self.output_dir / f"marketing_brief_{today}.md"
        marketing_section = ""
        
        if marketing_brief_path.exists():
            with open(marketing_brief_path, 'r', encoding='utf-8') as f:
                marketing_content = f.read()
                # 提取Marketing资讯部分
                if "## 📰 精选营销资讯" in marketing_content:
                    start_idx = marketing_content.find("## 📰 精选营销资讯")
                    end_idx = marketing_content.find("## 🤝 互动与反馈")
                    if start_idx != -1 and end_idx != -1:
                        marketing_section = marketing_content[start_idx:end_idx].strip()
        
        if not marketing_section:
            marketing_section = """### 行业趋势
- 待收集：每天早上8:00自动更新

### 案例分析
- 待收集：聚焦品牌营销、数字营销、整合营销

### 面试素材
- 待提取：从资讯中提取可用于面试的观点和案例"""
        
        brief = f"""# 求职准备每日简报
日期：{today}

---

## 📊 今日求职进度

### 📝 投递统计
- 今日投递：0份
- 本周投递：0份
- 总投递数：0份
- 回复率：0%

### 🎯 目标岗位
"""
        
        # 添加目标岗位信息
        for role in self.config['user_profile']['target_role']:
            brief += f"- {role}\n"
        
        brief += f"""
---

## 📰 Marketing资讯速览

{marketing_section}

---

## 🎯 今日任务

### 优先级任务
1. [ ] 查看目标公司招聘动态
2. [ ] 更新简历关键词
3. [ ] 准备行为面试案例
4. [ ] 研究目标公司品牌策略

### 学习任务
1. [ ] 阅读1篇营销行业文章
2. [ ] 分析1个营销案例
3. [ ] 整理面试素材

---

## 💡 今日建议

### 简历优化
- 检查简历是否包含目标岗位关键词
- 确保量化成果清晰可见
- 突出与目标公司匹配的经验

### 面试准备
- 准备3个STAR案例
- 研究目标公司最近的营销动态
- 练习自我介绍

### 求职策略
- 关注目标公司的招聘公众号
- 在领英上关注目标公司的HR
- 参与行业社群讨论

---

## 📅 本周规划

### 本周目标
- 投递数量：25份
- 面试准备：完成5个STAR案例
- 学习任务：分析3个营销案例

### 时间分配
- 周一：简历优化 + 投递
- 周二：面试准备 + 学习
- 周三：投递 + 跟进
- 周四：面试准备 + 投递
- 周五：总结 + 规划下周

---

## 🎯 目标公司动态

"""
        
        # 添加目标公司信息
        for category, companies in self.config['target_companies'].items():
            brief += f"\n### {category}\n"
            for company in companies[:3]:  # 只显示前3家
                brief += f"- {company['name']}\n"
        
        brief += """
---

## 📝 备忘录

### 待办事项
- [ ] 更新求职进度
- [ ] 整理面试反馈
- [ ] 调整求职策略

### 重要提醒
- 保持每日学习和投递
- 及时记录面试反馈
- 定期复盘和调整

---

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return brief
    
    def save_brief(self, brief):
        """保存简报到本地"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}_daily_brief.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(brief)
        
        print(f"✅ 每日简报已保存: {filepath}")
        return filepath
    
    def run(self):
        """运行主程序"""
        print("🚀 开始生成求职准备每日简报...")
        brief = self.generate_daily_brief()
        filepath = self.save_brief(brief)
        print(f"\n📄 简报已生成: {filepath}")
        return brief

if __name__ == "__main__":
    assistant = JobPrepDailyBrief()
    assistant.run()
