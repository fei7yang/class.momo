# -*- coding: utf-8 -*-
# ============================================================
#  config.example.py — 配置模板
#  复制此文件为 config.py，填入真实值，config.py 不会被上传
# ============================================================

# AgentMail API Key（在 console.agentmail.to 获取）
AGENTMAIL_API_KEY = "am_us_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# AgentMail 发件箱 ID（你创建的 inbox，不含 @agentmail.to）
INBOX_ID = "class.momo"

# 发件人显示名
SENDER_NAME = "Eric的虾虾🦐"

# 默认收件人列表（可在各课程文件中覆盖）
DEFAULT_RECIPIENTS = [
    "your_email@163.com",
    "another@example.com",
]

# 提前提醒分钟数
DEFAULT_ALARM_MINUTES = 15
