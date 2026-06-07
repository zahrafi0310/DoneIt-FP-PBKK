import streamlit as st
import requests
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from style import API_BASE, inject_global_css, sidebar_user, TOMATO, CORAL, LEVEL_NAMES

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

XP_THRESHOLDS = [0, 0, 500, 1500]
XP_MAX        = [0, 500, 1500, 9999]

def calculate_level(xp: int) -> int:
    if xp < 500:
        return 1
    elif xp < 1500:
        return 2
    else:
        return 3

def xp_progress(xp: int, level: int) -> int:
    level = max(1, min(level, 3))
    lo = XP_THRESHOLDS[level]
    hi = XP_MAX[level]
    if hi == 9999:
        return 100
    if xp <= lo:
        return 0
    return min(100, max(0, int((xp - lo) / (hi - lo) * 100)))

def show():
    inject_global_css()
    sidebar_user("profile")

    user = st.session_state.get("user", {})
    try:
        me = requests.get(f"{API_BASE}/auth/me", headers=auth_headers(), timeout=8).json()
        user = me
        st.session_state.user = me
    except:
        pass

    xp         = user.get("xp") or 0
    level      = calculate_level(xp)
    level_name = LEVEL_NAMES.get(level, "Petualang")
    progress   = xp_progress(xp, level)
    next_level = min(level + 1, 3)

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem;
                     font-weight:700; color:{TOMATO};'>Profil</span>
    </div>
    """, unsafe_allow_html=True)

    initial = (user.get("username") or "?")[0].upper()
    st.markdown(f"""
    <div class='modal-box' style='margin-bottom:1.5rem;'>
        <div style='display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap;'>
            <div style='width:70px; height:70px; border-radius:50%;
                        background:linear-gradient(135deg,{CORAL},{TOMATO});
                        display:flex; align-items:center; justify-content:center;
                        font-family:Fredoka,sans-serif; font-size:2rem;
                        font-weight:700; color:white;'>
                {initial}
            </div>
            <div style='flex:1;'>
                <div style='font-family:Fredoka,sans-serif; font-size:1.4rem;
                            font-weight:700; color:#222;'>{user.get("username","")}</div>
                <div style='font-size:0.85rem; color:#888;'>{user.get("email","")}</div>
                <div style='margin-top:0.3rem;'>
                    <span style='background:{TOMATO}; color:white; border-radius:20px;
                                 padding:2px 12px; font-size:0.8rem; font-weight:600;'>
                        Level {level} - {level_name}
                    </span>
                </div>
            </div>
            <div style='text-align:right;'>
                <div style='font-family:Fredoka,sans-serif; font-size:2.2rem;
                            font-weight:700; color:{TOMATO};'>{xp}</div>
                <div style='font-size:0.78rem; color:#aaa;'>Total XP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    coral_color = CORAL
    tomato_color = TOMATO
    progress_label = f"Progress ke Level {next_level}" if level < 3 else "Level Maksimum Tercapai"
    st.markdown(f"""
    <div style='background:white; border-radius:18px; padding:1.2rem 2rem;
                box-shadow:0 6px 32px rgba(201,54,56,0.10); margin-bottom:1.5rem;'>
        <div style='display:flex; justify-content:space-between;
                    font-size:0.8rem; color:#888; margin-bottom:6px;'>
            <span>{progress_label}</span>
            <span>{progress}%</span>
        </div>
        <div style='background:#f0e8e8; border-radius:20px; height:12px;
                    width:100%; overflow:hidden;'>
            <div style='width:{progress}%; height:100%; border-radius:20px;
                        background:linear-gradient(90deg,{coral_color},{tomato_color});'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family:Fredoka,sans-serif; font-size:1.2rem; font-weight:700;
                color:{TOMATO}; margin-bottom:0.8rem;'>Riwayat Submission</div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{API_BASE}/submissions/my", headers=auth_headers(), timeout=8)
        submissions = resp.json() if resp.status_code == 200 else []
    except:
        submissions = []

    try:
        qresp  = requests.get(f"{API_BASE}/quests/", headers=auth_headers(), timeout=8)
        quests = {q["id"]: q for q in (qresp.json() if qresp.status_code == 200 else [])}
    except:
        quests = {}

    if not submissions:
        st.markdown("""
        <div style='background:white; border-radius:14px; padding:1.5rem;
                    text-align:center; color:#aaa; border:1.5px solid #f0e8e8;'>
            Belum ada submission.
        </div>
        """, unsafe_allow_html=True)
        return

    status_cfg = {
        "approved": ("#d4f7d4", "#276b27", "Disetujui"),
        "pending":  ("#fff8e1", "#b8860b", "Menunggu Review"),
        "rejected": ("#ffd5d5", "#8b0000", "Ditolak"),
    }
    border_cfg = {
        "approved": "#62C4DA",
        "pending":  "#f0e8e8",
        "rejected": "#FA855A",
    }

    for sub in submissions:
        status  = sub.get("status", "pending")
        bg, fg, label = status_cfg.get(status, ("#eee", "#666", status.capitalize()))
        border  = border_cfg.get(status, "#f0e8e8")

        q_info  = quests.get(sub["quest_id"], {})
        q_title = q_info.get("title") or f"Quest #{sub['quest_id']}"
        q_xp    = q_info.get("xp_reward", "?")

        try:
            sub_time = datetime.fromisoformat(sub["submitted_at"]).strftime("%d %b %Y, %H:%M")
        except:
            sub_time = sub["submitted_at"]

        xp_display = f"+{q_xp} XP" if status == "approved" else ("? XP" if status == "pending" else "0 XP")

        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:1.1rem 1.3rem;
                    margin-bottom:0.8rem; border:1.5px solid {border};'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                <div style='flex:1;'>
                    <div style='font-weight:700; font-size:0.98rem; color:#222;'>{q_title}</div>
                    <div style='font-size:0.78rem; color:#aaa; margin-top:0.2rem;'>{sub_time}</div>
        """, unsafe_allow_html=True)

        if status == "rejected" and sub.get("rejection_reason"):
            reason = sub["rejection_reason"]
            st.markdown(f"""
            <div style='margin-top:0.4rem; font-size:0.8rem; color:#8b0000;
                        background:#fff0f0; border-radius:6px; padding:0.4rem 0.7rem;'>
                Alasan: {reason}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
                </div>
                <div style='text-align:right; margin-left:1rem;'>
                    <span style='background:{bg}; color:{fg}; border-radius:20px;
                                 padding:3px 12px; font-size:0.78rem; font-weight:600;'>
                        {label}
                    </span>
                    <div style='font-family:Fredoka,sans-serif; font-size:1.1rem;
                                font-weight:700; color:{TOMATO}; margin-top:0.3rem;'>
                        {xp_display}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)