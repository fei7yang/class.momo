# class.momo

> 一个由 **Eric's Claw** 驱动的课程日历管理工具。
> 通过 [AgentMail](https://agentmail.to) 发送标准 iCalendar 邀请，支持 Outlook、iPhone、华为等所有主流日历客户端。

---

## 设计思路

传统的课程提醒依赖人工转发或手动添加，更新麻烦且容易遗漏。本项目的目标是：

- 每门课程对应一个独立的 `.py` 文件
- 需要更新某节课时，只修改那个文件里的几个字段，然后运行它
- 收件人会收到一封 HTML 格式的邮件，附带标准 `.ics` 日历文件
- 支持日历事件**原地更新**（不新建事件），依赖 iCalendar 的 `UID + SEQUENCE` 机制
- 收件人无需安装任何 App，用 Outlook / 163 / 系统邮件接受邀请即可

---

## 项目结构

```
class.momo/
├── config.py              ← 本地配置（含 API Key，不上传）
├── config.example.py      ← 配置模板（复制并重命名为 config.py）
├── send_base.py            ← 公共发送逻辑（所有课程共用）
├── courses/
│   ├── 00ceshi.py         ← 测试课程
│   ├── 01xxxxx.py         ← 第二门课（待添加）
│   └── ...
└── README.md
```

命名规范：`两位数字 + 拼音`，例如 `01shuxue`、`02yingyu`，便于排序和识别。

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/fei7yang/class.momo.git
cd class.momo
```

### 2. 安装依赖

```bash
pip install agentmail
```

### 3. 配置

```bash
cp config.example.py config.py
# 编辑 config.py，填入你的 AgentMail API Key 和收件人
```

在 [console.agentmail.to](https://console.agentmail.to) 注册并创建一个 inbox，获取 API Key。

### 4. 发送课程提醒

```bash
# 发送某门课的更新
python courses/00ceshi.py
```

---

## 更新已有课程

打开对应的课程文件，修改时间或描述，然后把 `SEQUENCE` 加 1，重新运行：

```python
SEQUENCE = 1          # 原来是 0，改成 1
DATE_STR = "2026年3月18日（周三）"
TIME_STR = "10:00 - 11:00"
START    = "20260318T100000"
END      = "20260318T110000"
```

收件人日历里的事件会**自动更新**，不会新增重复条目。

---

## 依赖

- Python 3.8+
- [agentmail](https://pypi.org/project/agentmail/)

---

## License

MIT
