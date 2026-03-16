# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from send_base import build_html

html = build_html(
    summary="测试",
    date_str="2026年3月17日（周二）",
    time_str="09:00 - 10:00",
    alarm_minutes=15,
    desc="这是第一个测试课程，用于验证系统流程。"
)

out = r"C:\Eric_Workspace\class.momo\preview.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"OK: {out}")
