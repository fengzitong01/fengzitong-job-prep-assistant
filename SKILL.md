# 求职准备助手 Skill

## 描述
全面的求职准备助手，集成Marketing资讯整理、岗位分析、面试准备、简历优化等功能，助力求职成功。

## 适用场景
- Marketing领域求职准备（品牌策划、市场营销经理、数字营销专员）
- 目标公司：互联网大厂、科技公司、消费品行业（消费电子、快消）
- 面试准备、简历优化、进度跟踪

## 核心功能

### 1. 求职目标管理
- 目标岗位设定与跟踪
- 目标公司列表管理
- 求职时间规划
- 薪资期望设定

### 2. 岗位要求分析
- JD智能解析
- 技能关键词提取
- 能力匹配度分析
- 简历优化建议

### 3. Marketing资讯智能筛选
- 按求职目标筛选资讯
- 按公司、岗位、技能分类
- 面试素材自动提取
- 行业趋势跟踪

### 4. 面试准备支持
- 常见面试问题库
- 行为面试STAR法则模板
- 案例分析准备材料
- 模拟面试功能

### 5. 求职进度跟踪
- 投递进度记录
- 面试反馈分析
- Offer比较分析
- 时间节点提醒

### 6. 简历优化
- 简历关键词检查
- 格式美化建议
- 内容优化建议
- 版本管理

## 文件结构
```
skills/job-preparation-assistant/
├── SKILL.md
├── config.json
├── scripts/
│   ├── job_analysis.py
│   ├── interview_prep.py
│   ├── progress_tracker.py
│   └── resume_optimizer.py
├── templates/
│   ├── star_template.md
│   ├── interview_questions.md
│   └── resume_template.md
├── data/
│   ├── target_companies.json
│   ├── job_applications.json
│   └── interview_feedback.json
└── output/
    ├── daily_brief.md
    └── weekly_summary.md
```

## 使用方法

### 1. 求职目标管理
```bash
# 设置求职目标
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/job_analysis.py --set-goal

# 查看目标匹配度
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/job_analysis.py --analyze-jd --jd "岗位描述文本"
```

### 2. 面试准备
```bash
# 生成面试问题
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/interview_prep.py --generate-questions

# STAR法则模板
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/interview_prep.py --star-template
```

### 3. 进度跟踪
```bash
# 记录投递
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/progress_tracker.py --log-application

# 查看进度
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/progress_tracker.py --show-progress
```

### 4. 每日简报
```bash
# 生成每日求职简报
python3 ~/.openclaw/workspace/skills/job-preparation-assistant/scripts/daily_brief.py

# 自动运行：每天早上8:00
```

## 飞书文档集成
- **主文档**: 待创建
- **资讯日报**: 每日Marketing资讯
- **面试记录**: 面试准备和反馈
- **进度看板**: 求职进度可视化

## 配置说明

### 用户档案 (config.json)
```json
{
  "user_profile": {
    "name": "冯梓桐",
    "career_goal": "品牌策划/市场营销经理/数字营销专员",
    "target_industry": ["互联网大厂", "科技公司", "消费品"],
    "target_role": ["品牌策划", "市场营销经理", "数字营销专员"],
    "focus_areas": ["品牌营销", "数字营销", "整合营销"]
  }
}
```

### 求职配置
```json
{
  "job_search_config": {
    "start_date": "2026-04-14",
    "target_salary": "面议",
    "preferred_locations": ["北京", "上海", "深圳"],
    "application_limit_per_day": 5
  }
}
```

## 自动化功能

### 每日任务（早上8:00）
1. Marketing资讯整理
2. 面试素材提取
3. 行业趋势分析
4. 求职进度提醒

### 每周任务（周日晚上）
1. 求职进度总结
2. 面试复盘分析
3. 下周计划制定
4. 简历优化建议

## 数据统计

### 投递统计
- 总投递数
- 回复率
- 面试转化率
- Offer数量

### 能力分析
- 技能匹配度
- 简历关键词覆盖
- 面试表现评分

## 维护更新
- 定期更新目标公司列表
- 新增面试题库
- 优化简历模板
- 调整求职策略

## 注意事项
1. 保护个人隐私信息
2. 定期备份数据
3. 及时更新进度
4. 保持简历最新版本

## 未来扩展
- AI模拟面试
- 薪资谈判指导
- 职业规划建议
- 社交媒体个人品牌建设
