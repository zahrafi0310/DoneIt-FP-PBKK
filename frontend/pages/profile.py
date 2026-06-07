import streamlit as st
import requests
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from style import API_BASE, inject_global_css, sidebar_user, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, HONEYDEW, LEVEL_NAMES

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

XP_THRESHOLDS = [0, 300, 900, 1800]
XP_MAX        = [300, 900, 1800, 9999]

def xp_progress(xp, level):
    lo = XP_THRESHOLDS[min(level, 3)]
    hi = XP_MAX[min(level, 3)]
    if hi == 9999:
        return 100
    return min(100, int((xp - lo) / (hi - lo) * 100))

def show():
    inject_global_css()
    sidebar_user("profile")

    user = st.session_state.get("user", {})
    token = st.session_state.get("token", "")

    try:
        me = requests.get(f"{API_BASE}/auth/me", headers=auth_headers(), timeout=8).json()
        user = me
        st.session_state.user = me
    except:
        pass

    xp    = user.get("xp", 0)
    level = user.get("level", 0)
    level_name = LEVEL_NAMES.get(level, "Pemula")
    progress   = xp_progress(xp, level)

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Profil
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='modal-box' style='margin-bottom:1.5rem;'>
        <div style='display:flex; align-items:center; gap:1.5rem; flex-wrap:wrap;'>
            <div style='width:70px; height:70px; border-radius:50%;
                        background:linear-gradient(135deg,{CORAL},{TOMATO});
                        display:flex; align-items:center; justify-content:center;
                        font-family:Fredoka,sans-serif; font-size:2rem; font-weight:700; color:white;'>
                {user.get("username","?")[0].upper()}
            </div>
            <div style='flex:1;'>
                <div style='font-family:Fredoka,sans-serif; font-size:1.4rem; font-weight:700; color:#222;'>
                    {user.get("username","")}
                </div>
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

        <div style='margin-top:1.2rem;'>
            <div style='display:flex; justify-content:space-between; font-size:0.8rem; color:#888; margin-bottom:4px;'>
                <span>Progress ke Level {min(level+1, 3)}</span>
                <span>{progress}%</span>
            </div>
            <div class='xp-bar-outer'>
                <div class='xp-bar-inner' style='width:{progress}%;'></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family:Fredoka,sans-serif; font-size:1.2rem; font-weight:700;
                color:{TOMATO}; margin-bottom:0.8rem;'>
        Riwayat Submission
    </div>
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
        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:1.5rem; text-align:center;
                    color:#aaa; border:1.5px solid #f0e8e8;'>
            Belum ada submission.
        </div>
        """, unsafe_allow_html=True)
        return

    status_cfg = {
        "approved": ("#d4f7d4", "#276b27", "Disetujui"),
        "pending":  ("#fff8e1", "#b8860b", "Menunggu"),
        "rejected": ("#ffd5d5", "#8b0000", "Ditolak"),
    }

    for sub in submissions:
        status = sub.get("status", "pending")
        bg, fg, label = status_cfg.get(status, ("#eee", "#666", status.capitalize()))

        q_info = quests.get(sub["quest_id"], {})
        q_title = q_info.get("title", f"Quest #{sub['quest_id']}")
        q_xp    = q_info.get("xp_reward", "?")

        try:
            sub_time = datetime.fromisoformat(sub["submitted_at"]).strftime("%d %b %Y, %H:%M")
        except:
            sub_time = sub["submitted_at"]

        rejection = ""
        if status == "rejected" and sub.get("rejection_reason"):
            rejection = f"""
            <div style='margin-top:0.4rem; font-size:0.8rem; color:#8b0000;
                        background:#fff0f0; border-radius:6px; padding:0.4rem 0.7rem;'>
                Alasan: {sub["rejection_reason"]}
            </div>
            """

        st.markdown(f"""
        <div class='submission-card {status}' style='margin-bottom:0.8rem;'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                <div style='flex:1;'>
                    <div style='font-weight:700; font-size:0.98rem; color:#222;'>{q_title}</div>
                    <div style='font-size:0.78rem; color:#aaa; margin-top:0.2rem;'>{sub_time}</div>
                    {rejection}
                </div>
                <div style='text-align:right; margin-left:1rem;'>
                    <span style='background:{bg}; color:{fg}; border-radius:20px;
                                 padding:3px 12px; font-size:0.78rem; font-weight:600;'>
                        {label}
                    </span>
                    <div style='font-family:Fredoka,sans-serif; font-size:1.1rem;
                                font-weight:700; color:{TOMATO}; margin-top:0.3rem;'>
                        {"+" if status == "approved" else ""}{q_xp if status == "approved" else "?"} XP
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)