import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from style import API_BASE, inject_global_css, sidebar_user, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, HONEYDEW, DIFF_COLOR

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def show():
    inject_global_css()
    sidebar_user("dashboard")

    user = st.session_state.get("user", {})
    token = st.session_state.get("token", "")

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Halo, {user.get("username", "Adventurer")}
        </span>
        <div style='color:#666; font-size:0.92rem; margin-top:0.2rem;'>
            Level {user.get("level", 0)} &nbsp;|&nbsp; {user.get("xp", 0)} XP
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{API_BASE}/quests/", headers=auth_headers(), timeout=8)
        quests = resp.json() if resp.status_code == 200 else []
    except:
        quests = []
        st.error("Gagal memuat quest. Pastikan server berjalan.")

    try:
        my_resp = requests.get(f"{API_BASE}/quests/my", headers=auth_headers(), timeout=8)
        my_quests = my_resp.json() if my_resp.status_code == 200 else []
        accepted_ids = {aq["quest_id"] for aq in my_quests}
    except:
        accepted_ids = set()

    categories = {
        "akademik":  "Akademik",
        "fun_things": "Fun Things",
        "soft_skill": "Soft Skill",
        "lifestyle":  "Lifestyle",
    }

    tabs = st.tabs(list(categories.values()))

    for tab, (cat_key, cat_label) in zip(tabs, categories.items()):
        with tab:
            cat_quests = [q for q in quests if q["category"] == cat_key]
            if not cat_quests:
                st.markdown(f"<div style='color:#aaa; padding:1rem 0; font-size:0.9rem;'>Belum ada quest di kategori ini.</div>", unsafe_allow_html=True)
                continue

            for q in cat_quests:
                diff  = q.get("difficulty", "easy")
                color = DIFF_COLOR.get(diff, "#aaa")
                is_limited = q.get("is_limited", False)
                end_date   = q.get("end_date", None)

                deadline_text = ""
                if is_limited and end_date:
                    from datetime import datetime
                    try:
                        dt = datetime.fromisoformat(end_date)
                        deadline_text = f"Berakhir: {dt.strftime('%d %b %Y, %H:%M')}"
                    except:
                        deadline_text = f"Berakhir: {end_date}"
                else:
                    deadline_text = "Permanent"

                already = q["id"] in accepted_ids

                with st.expander(f"{q['title']}  —  {q['xp_reward']} XP", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"""
                        <div style='font-size:0.88rem; color:#555; margin-bottom:0.7rem;'>
                            {q.get("description", "")}
                        </div>
                        <div>
                            <span class='diff-badge' style='background:{color};'>{diff.capitalize()}</span>
                            &nbsp;
                            <span style='font-size:0.8rem; color:#888;'>{deadline_text}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div style='text-align:right;'>
                            <div style='font-family:Fredoka,sans-serif; font-size:1.6rem;
                                        font-weight:700; color:{TOMATO};'>{q['xp_reward']}</div>
                            <div style='font-size:0.75rem; color:#aaa;'>XP Reward</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if already:
                        st.markdown(f"""
                        <div style='margin-top:0.8rem; padding:0.5rem 1rem; background:#e8f8f0;
                                    border-radius:8px; color:#276b27; font-size:0.85rem; font-weight:600;'>
                            Quest ini sudah ada di daftar questmu.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        if st.button("Terima Quest", key=f"accept_{q['id']}", type="primary"):
                            try:
                                r = requests.post(
                                    f"{API_BASE}/quests/{q['id']}/accept",
                                    headers=auth_headers(), timeout=8
                                )
                                if r.status_code in (200, 201):
                                    st.success("Quest berhasil diterima!")
                                    st.rerun()
                                else:
                                    st.error(r.json().get("detail", "Gagal menerima quest."))
                            except Exception as e:
                                st.error(f"Error: {e}")