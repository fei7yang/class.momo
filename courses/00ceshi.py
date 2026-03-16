# -*- coding: utf-8 -*-
"""
courses/00ceshi.py — 测试课程
命名规范：两位数字 + 拼音，如 01shuxue、02yingyu
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from send_base import send_calendar_event

# ── 课程信息（每次修改只改这里）──────────────────────────────
UID      = "claw-course-00ceshi"   # 永远不变，是这门课的唯一ID
SEQUENCE = 3                        # 每次有更新 +1

SUMMARY  = "测试"
DATE_STR = "2026年3月17日（周二）"
TIME_STR = "09:00 - 10:00"
START    = "20260317T090000"
END      = "20260317T100000"
DESC     = "这是第一个测试课程，用于验证系统流程。"
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[00ceshi] 发送课程更新：{SUMMARY} / {DATE_STR} {TIME_STR}")
    send_calendar_event(
        uid=UID,
        sequence=SEQUENCE,
        summary=SUMMARY,
        start=START,
        end=END,
        date_str=DATE_STR,
        time_str=TIME_STR,
        desc=DESC,
    )
    print("[00ceshi] 完成。")
