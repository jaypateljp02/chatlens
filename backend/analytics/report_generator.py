"""
Executive Report Generator for ChatLens AI.
Compiles communication metrics, AI summaries, sentiment breakdowns, and pending action items into a printable HTML report.
"""
from typing import List, Dict, Any
from datetime import datetime
from models.schemas import ParsedMessage
from analytics.communication import calculate_communication_stats
from analytics.sentiment import calculate_sentiment_stats
from analytics.people import calculate_people_profiles
from analytics.actions import detect_action_items
from ai.gemma_client import generate_gemma_summary


def generate_executive_report(messages: List[ParsedMessage], title: str = "Executive Communication Report") -> str:
    """Generate a clean printable HTML executive report string."""
    comm = calculate_communication_stats(messages)
    sent = calculate_sentiment_stats(messages)
    people = calculate_people_profiles(messages)
    actions = detect_action_items(messages)
    
    chat_text = "\n".join([f"[{m.timestamp}] {m.sender}: {m.content}" for m in messages if not m.is_system])
    summary_data = generate_gemma_summary(chat_text, "bullet")
    
    people_list = people.get("profiles", []) if isinstance(people, dict) else getattr(people, "profiles", [])
    action_list = actions.get("action_items", []) if isinstance(actions, dict) else getattr(actions, "action_items", [])
    
    if isinstance(sent, dict):
        overall_sent = sent.get("overall_sentiment", {})
    else:
        overall_sent = getattr(sent, "overall_sentiment", {})
        
    pos_count = overall_sent.get("positive", 0) if isinstance(overall_sent, dict) else 0

    top_people_html = ""
    for p in people_list[:5]:
        p_name = p.get("name") if isinstance(p, dict) else getattr(p, "name", "Unknown")
        p_style = p.get("communication_style") if isinstance(p, dict) else getattr(p, "communication_style", "Communicator")
        p_msgs = p.get("messages_count") if isinstance(p, dict) else getattr(p, "messages_count", 0)
        p_score = p.get("engagement_score") if isinstance(p, dict) else getattr(p, "engagement_score", 0)
        
        top_people_html += f"""
        <div style="background: #F8F9FA; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between;">
            <div>
                <strong>{p_name}</strong> <span style="color: #6c757d; font-size: 12px;">({p_style})</span>
            </div>
            <div>
                <strong>{p_msgs}</strong> msgs | Score: <strong style="color: #128C7E;">{p_score} pts</strong>
            </div>
        </div>
        """

    actions_html = ""
    for act in action_list[:5]:
        act_promise = act.get("promise") if isinstance(act, dict) else getattr(act, "promise", "")
        act_assignee = act.get("assignee") if isinstance(act, dict) else getattr(act, "assignee", "Unassigned")
        act_status = act.get("status") if isinstance(act, dict) else getattr(act, "status", "pending")
        
        status_color = "#25D366" if act_status == "completed" else "#FFA726"
        actions_html += f"""
        <div style="padding: 10px; border-left: 4px solid {status_color}; background: #F8F9FA; margin-bottom: 8px; border-radius: 4px;">
            <div style="font-weight: 600; font-size: 14px;">"{act_promise}"</div>
            <div style="font-size: 12px; color: #6c757d; margin-top: 4px;">Assigned: <strong>{act_assignee}</strong> | Status: <span style="color: {status_color}; font-weight: 700;">{str(act_status).upper()}</span></div>
        </div>
        """

    most_active = comm.most_active_participant if hasattr(comm, 'most_active_participant') else (comm.get('most_active_participant') if isinstance(comm, dict) else 'N/A')

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>ChatLens AI - {title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f6f8; color: #111b21; padding: 30px; margin: 0; }}
        .container {{ max-width: 800px; background: white; margin: 0 auto; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .header {{ border-bottom: 2px solid #25D366; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ margin: 0; color: #075E54; font-size: 24px; }}
        .header .meta {{ font-size: 12px; color: #667781; text-align: right; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat-card {{ background: #EFEAE2; padding: 16px; border-radius: 10px; text-align: center; }}
        .stat-card .val {{ font-size: 22px; font-weight: 700; color: #128C7E; }}
        .stat-card .lbl {{ font-size: 12px; color: #667781; margin-top: 4px; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #075E54; margin: 24px 0 12px 0; border-bottom: 1px solid #E9EDEF; padding-bottom: 6px; }}
        .summary-box {{ background: #F0F2F5; padding: 16px; border-radius: 10px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; }}
        @media print {{ body {{ padding: 0; background: white; }} .container {{ box-shadow: none; padding: 0; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>ChatLens AI Executive Report</h1>
                <div style="font-size: 13px; color: #667781; margin-top: 4px;">{title}</div>
            </div>
            <div class="meta">
                <div>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div>Status: Verified Official Report</div>
            </div>
        </div>

        <div class="grid">
            <div class="stat-card">
                <div class="val">{len(messages)}</div>
                <div class="lbl">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="val">{len(people_list)}</div>
                <div class="lbl">Participants</div>
            </div>
            <div class="stat-card">
                <div class="val">{most_active}</div>
                <div class="lbl">Top Contributor</div>
            </div>
            <div class="stat-card">
                <div class="val">{pos_count}</div>
                <div class="lbl">Positive Msgs</div>
            </div>
        </div>

        <div class="section-title">🤖 AI Executive Summary</div>
        <div class="summary-box">{summary_data.get('summary_text', '')}</div>

        <div class="section-title">👥 Top Participant Performance</div>
        {top_people_html}

        <div class="section-title">⚠️ Action Items & Commitments</div>
        {actions_html}

        <div style="margin-top: 40px; border-top: 1px solid #E9EDEF; padding-top: 16px; font-size: 11px; color: #667781; text-align: center;">
            Generated by ChatLens AI Intelligence Platform • All Processing Completed On-Device
        </div>
    </div>
</body>
</html>"""
    return html
