# -*- coding: utf-8 -*-
"""
send_base.py — 公共发送模块
所有课程文件都 import 这里的 send_calendar_event()
"""

import base64
from agentmail import AgentMail
import config


def build_ics(uid, sequence, summary, start, end, timezone, desc, alarm_minutes, recipients):
    """生成 iCalendar 字符串"""
    attendees = "\n".join(
        f"ATTENDEE;CN={addr};RSVP=TRUE:mailto:{addr}"
        for addr in recipients
    )
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        f"PRODID:-//Eric's Claw//Calendar//EN\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:REQUEST\n"
        "BEGIN:VEVENT\n"
        f"UID:{uid}@ericsclaw.to\n"
        f"SEQUENCE:{sequence}\n"
        "DTSTAMP:20260316T000000Z\n"
        f"DTSTART;TZID={timezone}:{start}\n"
        f"DTEND;TZID={timezone}:{end}\n"
        f"SUMMARY:{summary}\n"
        f"DESCRIPTION:{desc}\n"
        f"ORGANIZER;CN={config.SENDER_NAME}:mailto:{config.INBOX_ID}\n"
        f"{attendees}\n"
        "BEGIN:VALARM\n"
        f"TRIGGER:-PT{alarm_minutes}M\n"
        "ACTION:DISPLAY\n"
        f"DESCRIPTION:提醒：{summary} 即将开始\n"
        "END:VALARM\n"
        "END:VEVENT\n"
        "END:VCALENDAR"
    )


def build_html(summary, date_str, time_str, alarm_minutes, desc):
    """生成 HTML 邮件正文"""
    return f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f5f6fa;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:12px;
                      box-shadow:0 2px 12px rgba(0,0,0,0.08);overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%);
                       padding:32px 40px 28px;">
              <p style="margin:0;font-size:13px;color:#7ecfff;
                        letter-spacing:2px;text-transform:uppercase;">CALENDAR UPDATE</p>
              <h1 style="margin:8px 0 0;font-size:24px;font-weight:700;
                         color:#ffffff;letter-spacing:0.5px;">📅 课程时间更新</h1>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:36px 40px 28px;">
              <p style="margin:0 0 6px;font-size:16px;font-weight:600;color:#333;">
                亲爱的 momo，您好
              </p>
              <p style="margin:0 0 24px;font-size:15px;color:#444;line-height:1.7;">
                以下课程安排已更新，请查收并接受日历邀请。
              </p>
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f0f7ff;border-left:4px solid #0f3460;
                            border-radius:6px;margin-bottom:28px;">
                <tr>
                  <td style="padding:20px 24px;">
                    <p style="margin:0 0 6px;font-size:18px;font-weight:700;
                               color:#0f3460;">{summary}</p>
                    <p style="margin:0 0 4px;font-size:13px;color:#666;">
                      &#128197;&nbsp;{date_str}
                    </p>
                    <p style="margin:0 0 4px;font-size:13px;color:#666;">
                      &#128336;&nbsp;{time_str}
                    </p>
                    <p style="margin:0 0 4px;font-size:13px;color:#888;">
                      &#128276;&nbsp;提前 {alarm_minutes} 分钟提醒
                    </p>
                    <p style="margin:8px 0 0;font-size:13px;color:#999;">{desc}</p>
                  </td>
                </tr>
              </table>
              <p style="margin:0;font-size:14px;color:#555;line-height:1.6;">
                附件中包含日历邀请文件
                （<code style="background:#f0f0f0;padding:1px 5px;
                               border-radius:3px;font-size:13px;">invite.ics</code>），
                点击接受后将自动添加到您的日历。
              </p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="border-top:1px solid #eee;padding:20px 40px;background:#fafafa;">
              <p style="margin:0;font-size:13px;color:#aaa;letter-spacing:0.5px;">
                From <strong style="color:#555;">{config.SENDER_NAME}</strong>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_calendar_event(
    uid,
    sequence,
    summary,
    start,          # 格式: "20260317T090000"
    end,            # 格式: "20260317T100000"
    date_str,       # 显示用: "2026年3月17日（周二）"
    time_str,       # 显示用: "09:00 - 10:00"
    desc="",
    timezone="Asia/Shanghai",
    alarm_minutes=None,
    recipients=None,
):
    """发送日历事件邮件给所有收件人"""
    if alarm_minutes is None:
        alarm_minutes = config.DEFAULT_ALARM_MINUTES
    if recipients is None:
        recipients = config.DEFAULT_RECIPIENTS

    ics = build_ics(uid, sequence, summary, start, end,
                    timezone, desc, alarm_minutes, recipients)
    ics_b64 = base64.b64encode(ics.encode("utf-8")).decode("utf-8")
    html    = build_html(summary, date_str, time_str, alarm_minutes, desc)
    text    = (
        f"课程时间更新：{summary}\n\n"
        f"时间：{date_str} {time_str}\n"
        f"提醒：活动开始前 {alarm_minutes} 分钟\n\n"
        f"{desc}\n\n"
        f"请接受附件中的日历邀请。\n\n"
        f"--\nFrom {config.SENDER_NAME}"
    )

    client = AgentMail(api_key=config.AGENTMAIL_API_KEY)

    to_addr = recipients[0]
    cc_list = recipients[1:] if len(recipients) > 1 else []

    print(f"  TO:  {to_addr}")
    for cc in cc_list:
        print(f"  CC:  {cc}")
    print("  发送中...", end=" ")
    try:
        result = client.inboxes.messages.send(
            inbox_id=config.INBOX_ID,
            to=to_addr,
            cc=cc_list if cc_list else None,
            subject=f"📅 课程时间更新：{summary}",
            text=text,
            html=html,
            attachments=[{
                "filename": "invite.ics",
                "content": ics_b64,
                "content_type": "text/calendar; method=REQUEST",
            }],
        )
        print(f"OK ({result.message_id[:30]}...)")
    except Exception as e:
        print(f"FAIL: {e}")
