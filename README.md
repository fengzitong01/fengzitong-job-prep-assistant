# 求职准备助手 - OpenClaw Skill

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw-skills/job-preparation-assistant)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/openclaw/openclaw)

> 🎯 **全面的求职准备助手** - 集成Marketing资讯整理、岗位分析、面试准备、简历优化等功能，助力求职成功！

---

## ✨ 功能特性

### 📋 求职目标管理
- 目标岗位设定与跟踪
- 目标公司列表管理（18家详细配置）
- 求职时间规划
- 薪资期望设定

### 🔍 岗位要求分析
- JD智能解析
- 技能关键词提取
- 能力匹配度分析
- 简历优化建议

### 📰 Marketing资讯智能筛选
- 按求职目标筛选资讯
- 按公司、岗位、技能分类
- 面试素材自动提取
- 行业趋势跟踪

### 🎤 面试准备支持
- 常见面试问题库
- 行为面试STAR法则模板
- 案例分析准备材料
- 模拟面试功能

### 📊 求职进度跟踪
- 投递进度记录
- 面试反馈分析
- Offer比较分析
- 时间节点提醒

### 📄 简历优化
- 简历关键词检查
- 格式美化建议
- 内容优化建议
- 版本管理

---

## 🚀 快速开始

### 方式1: 一键安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/openclaw-skills/job-preparation-assistant.git

# 进入目录
cd job-preparation-assistant

# 运行安装脚本
bash install.sh
```

### 方式2: 手动安装

```bash
# 1. 创建Skill目录
mkdir -p ~/.openclaw/skills/job-preparation-assistant

# 2. 复制文件
cp -r ./* ~/.openclaw/skills/job-preparation-assistant/

# 3. 安装依赖
pip install requests python-dateutil

# 4. 配置
cp examples/config.example.json config.json
# 编辑config.json，设置你的求职目标
```

### 方式3: OpenClaw CLI（即将支持）

```bash
openclaw skill install job-preparation-assistant
```

---

## 📖 使用说明

### 1. 配置求职目标

编辑 `config.json` 文件：

```json
{
  "user_profile": {
    "name": "你的名字",
    "career_goal": "品牌策划/市场营销经理/数字营销专员",
    "target_industry": ["互联网大厂", "科技公司", "消费品"],
    "target_role": ["品牌策划", "市场营销经理", "数字营销专员"],
    "focus_areas": ["品牌营销", "数字营销", "整合营销"]
  },
  "job_search_config": {
    "start_date": "2026-04-14",
    "target_salary": {
      "min": 15000,
      "max": 25000,
      "negotiable": true
    },
    "preferred_locations": ["北京", "上海", "深圳"]
  }
}
```

### 2. 生成每日简报

```bash
# 手动运行
python3 ~/.openclaw/skills/job-preparation-assistant/scripts/daily_brief.py

# 输出文件位置
# ~/.openclaw/skills/job-preparation-assistant/output/YYYY-MM-DD_daily_brief.md
```

### 3. 面试准备

```bash
# 查看STAR法则模板
cat ~/.openclaw/skills/job-preparation-assistant/templates/star_template.md

# 查看面试问题库
cat ~/.openclaw/skills/job-preparation-assistant/templates/interview_questions.md
```

### 4. 求职进度跟踪

```bash
# 记录投递
python3 ~/.openclaw/skills/job-preparation-assistant/scripts/progress_tracker.py --log-application

# 查看进度
python3 ~/.openclaw/skills/job-preparation-assistant/scripts/progress_tracker.py --show-progress
```

---

## 🎯 目标公司列表

### 互联网大厂
- 字节跳动、腾讯、阿里巴巴、美团、京东、拼多多

### 科技公司
- 华为、小米、OPPO、vivo、苹果、联想

### 消费品
- 宝洁、联合利华、欧莱雅、耐克、安踏、元气森林、完美日记、花西子

**详细配置**: 每家公司包含产品信息、企业文化、面试要点

---

## ⏰ 自动化功能

### 每日任务（早上8:00）
- ✅ Marketing资讯整理
- ✅ 面试素材提取
- ✅ 行业趋势分析
- ✅ 求职进度提醒

### 每周任务（周日晚上21:00）
- ✅ 求职进度总结
- ✅ 面试复盘分析
- ✅ 下周计划制定
- ✅ 简历优化建议

---

## 📁 文件结构

```
job-preparation-assistant/
├── package.json              # Skill包信息
├── README.md                 # 本文档
├── install.sh                # 安装脚本
├── uninstall.sh              # 卸载脚本
├── SKILL.md                  # 技能详细说明
├── config.json               # 用户配置
├── scripts/                  # 可执行脚本
│   ├── daily_brief.py            # 每日简报
│   ├── job_analysis.py           # 岗位分析
│   ├── interview_prep.py         # 面试准备
│   └── progress_tracker.py       # 进度跟踪
├── templates/                # 模板文件
│   ├── star_template.md          # STAR法则模板
│   ├── interview_questions.md    # 面试问题库
│   └── resume_template.md        # 简历模板
├── data/                     # 数据文件
│   ├── target_companies.json     # 目标公司列表
│   ├── job_applications.json     # 投递记录
│   └── interview_feedback.json   # 面试反馈
├── output/                   # 输出文件
│   ├── daily_brief.md            # 每日简报
│   └── weekly_summary.md         # 每周总结
└── examples/                 # 示例文件
    └── config.example.json       # 配置示例
```

---

## 🔧 配置说明

### 必需配置字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `user_profile.name` | 用户姓名 | "你的名字" |
| `user_profile.career_goal` | 职业目标 | "品牌策划" |
| `user_profile.target_industry` | 目标行业 | ["互联网大厂"] |
| `job_search_config.start_date` | 求职开始日期 | "2026-04-14" |
| `target_companies` | 目标公司列表 | 见config.json |

### 可选配置字段

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `job_search_config.target_salary` | 目标薪资 | negotiable: true |
| `job_search_config.preferred_locations` | 目标城市 | ["北京", "上海", "深圳"] |
| `automation.daily.time` | 每日任务时间 | "08:00" |
| `automation.weekly.time` | 每周任务时间 | "21:00" |

---

## 🌟 特色功能

### 1. 智能资讯筛选
- 根据你的求职目标自动筛选相关资讯
- 按行业、公司、技能智能分类
- 提取面试素材和案例

### 2. STAR法则模板
- 行为面试标准回答模板
- 包含多个场景示例
- 可直接用于面试准备

### 3. 目标公司深度信息
- 18家目标公司的详细信息
- 包含产品、文化、面试要点
- 实时更新招聘动态

### 4. 自动化进度跟踪
- 自动记录投递进度
- 面试反馈分析
- 数据可视化

---

## 📊 数据统计

### 投递统计
- 总投递数
- 回复率
- 面试转化率
- Offer数量

### 能力分析
- 技能匹配度
- 简历关键词覆盖
- 面试表现评分

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献方式
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

### v1.0.0 (2026-04-14)
- ✅ 初始版本发布
- ✅ 求职目标管理
- ✅ 面试准备模板
- ✅ 目标公司列表
- ✅ 每日简报功能

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 💬 联系方式

- **项目**: OpenClaw Skills Community
- **GitHub**: [openclaw-skills](https://github.com/openclaw-skills)

---

## 🙏 致谢

感谢 OpenClaw 团队提供优秀的Skill框架！

---

**🎯 助力你的求职之旅，祝你求职顺利！** 🚀
