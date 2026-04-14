# 飞书机器人通知配置指南

## 配置步骤

### 1. 获取飞书App ID和Secret（已有）

你的config.json中已有：
```json
"feishu": {
  "app_id": "cli_a92053d4ffb85bb5",
  "app_secret": "SBG5j8eRxG68NM4wvjyuQc8h6eD3CS8U"
}
```

### 2. 获取你的飞书用户ID

有以下几种方式获取你的用户ID：

#### 方式1：通过飞书开放平台
1. 访问 https://open.feishu.cn/
2. 登录你的账号
3. 在"开发者后台"查看你的用户信息

#### 方式2：通过飞书客户端
1. 打开飞书，进入"我的"页面
2. 点击头像查看个人信息
3. 在"用户信息"中查看用户ID

#### 方式3：通过机器人@消息
机器人可以先发送消息，然后获取发送者的用户ID。

### 3. 修改配置

在config.json中配置：

#### 配置1：发送给个人
```json
"notification": {
  "enabled": true,
  "method": "feishu",
  "feishu": {
    "user_id": "你的飞书用户ID"
  }
}
```

#### 配置2：发送到群聊
```json
"notification": {
  "enabled": true,
  "method": "feishu",
  "feishu": {
    "chat_id": "你的飞书群聊ID"
  }
}
```

### 4. 安装依赖

确保安装了必要的Python库：
```bash
pip install requests
```

### 5. 测试飞书通知

运行测试脚本：
```bash
python3 scripts/feishu_notification_test.py
```

## 快速配置方法

如果你不想手动查找用户ID，可以使用以下方法：

### 方法1：告诉我你的飞书邮箱
如果你告诉我你的飞书邮箱（通常是xxx@example.com），我可以帮你在代码中添加通过邮箱查找用户ID的功能。

### 方法2：临时使用Webhook
我可以先配置一个Webhook方式，你可以通过飞书创建Webhook机器人和我分享URL。

## 当前配置状态

你的config.json中已经包含了飞书App ID和Secret，只需要：

1. **找到你的飞书用户ID** 或 **群聊ID**
2. **更新config.json中的notification配置**

**你的飞书App ID：** cli_a92053d4ffb85bb5

## 注意事项

1. **权限检查**：确保飞书机器人有发送消息的权限
2. **网络要求**：需要能访问飞书API域名（open.feishu.cn）
3. **配置安全**：不要泄露App Secret

## 备用方案

如果飞书通知配置太复杂，也可以考虑：

1. **继续使用如流通知**（当前默认）
2. **使用邮件通知**
3. **使用Webhook通知**（支持飞书Webhook）