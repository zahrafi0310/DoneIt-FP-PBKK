import streamlit as st
import requests
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from style import API_BASE, inject_global_css, sidebar_admin, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, HONEYDEW

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def show():
    inject_global_css()
    sidebar_admin("admin_review")

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Review Submission
        </span>
        <div style='color:#666; font-size:0.92rem; margin-top:0.2rem;'>
            Submission yang menunggu persetujuan
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{API_BASE}/submissions/pending", headers=auth_headers(), timeout=8)
        submissions = resp.json() if resp.status_code == 200 else []
    except:
        submissions = []
        st.error("Gagal memuat submission.")

    try:
        qresp  = requests.get(f"{API_BASE}/quests/", headers=auth_headers(), timeout=8)
        quests = {q["id"]: q for q in (qresp.json() if qresp.status_code == 200 else [])}
    except:
        quests = {}

    user_ids = list({sub["user_id"] for sub in submissions})
    users = {}
    for uid in user_ids:
        try:
            uresp = requests.get(f"{API_BASE}/auth/users/{uid}", headers=auth_headers(), timeout=8)
            if uresp.status_code == 200:
                u = uresp.json()
                users[uid] = u.get("username", f"User #{uid}")
            else:
                users[uid] = f"User #{uid}"
        except:
            users[uid] = f"User #{uid}"

    if not submissions:
        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:2rem; text-align:center;
                    color:#aaa; border:1.5px solid #f0e8e8;'>
            Tidak ada submission yang perlu direview saat ini.
        </div>
        """, unsafe_allow_html=True)
        return

    for sub in submissions:
        q_info   = quests.get(sub["quest_id"], {})
        q_title  = q_info.get("title", f"Quest #{sub['quest_id']}")
        q_xp     = q_info.get("xp_reward", "?")
        username = users.get(sub["user_id"], f"User #{sub['user_id']}")

        try:
            sub_time = datetime.fromisoformat(sub["submitted_at"]).strftime("%d %b %Y, %H:%M")
        except:
            sub_time = sub["submitted_at"]

        with st.expander(f"Submission #{sub['id']} — Quest: {q_title} — {username}", expanded=False):
            col_info, col_photo = st.columns([1.4, 1])

            with col_info:
                st.markdown(f"""
                <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.8rem; color:#aaa; margin-bottom:0.2rem;'>Quest</div>
                    <div style='font-weight:700; color:#222;'>{q_title}</div>
                </div>
                <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.8rem; color:#aaa; margin-bottom:0.2rem;'>Submitted by</div>
                    <div style='font-weight:600; color:#444;'>{username}</div>
                </div>
                <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.8rem; color:#aaa; margin-bottom:0.2rem;'>XP Reward</div>
                    <div style='font-family:Fredoka,sans-serif; font-size:1.3rem;
                                font-weight:700; color:{TOMATO};'>{q_xp} XP</div>
                </div>
                <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.8rem; color:#aaa; margin-bottom:0.2rem;'>Dikirim pada</div>
                    <div style='font-size:0.88rem; color:#555;'>{sub_time}</div>
                </div>
                <div style='margin-bottom:0.8rem;'>
                    <div style='font-size:0.8rem; color:#aaa; margin-bottom:0.2rem;'>Deskripsi User</div>
                    <div style='font-size:0.88rem; color:#333; background:#f9f9f9;
                                border-radius:8px; padding:0.6rem 0.8rem;'>
                        {sub.get("description", "-")}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_photo:
                photo_path = sub.get("photo_path", "")
                if photo_path and os.path.exists(photo_path):
                    st.image(photo_path, caption="Foto Bukti", use_container_width=True)
                else:
                    st.markdown(f"""
                    <div style='background:#f0f0f0; border-radius:10px; padding:2rem;
                                text-align:center; color:#aaa; font-size:0.85rem;'>
                        Foto tidak tersedia
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:0.8rem;'>", unsafe_allow_html=True)
            col_approve, col_reject = st.columns([1, 1])

            with col_approve:
                if st.button("Approve", key=f"approve_{sub['id']}", type="primary",
                             use_container_width=True):
                    try:
                        r = requests.put(
                            f"{API_BASE}/submissions/{sub['id']}/review",
                            headers=auth_headers(),
                            json={"status": "approved"},
                            timeout=8
                        )
                        if r.status_code == 200:
                            st.success("Submission disetujui!")
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Gagal approve."))
                    except Exception as e:
                        st.error(f"Error: {e}")

            with col_reject:
                if st.button("Reject", key=f"reject_open_{sub['id']}", use_container_width=True):
                    st.session_state[f"show_reject_{sub['id']}"] = True

            if st.session_state.get(f"show_reject_{sub['id']}"):
                reason = st.text_area(
                    "Alasan Penolakan",
                    key=f"reason_{sub['id']}",
                    placeholder="Jelaskan alasan penolakan submission ini...",
                    height=90
                )
                col_send, col_back = st.columns([1, 1])
                with col_send:
                    if st.button("Kirim Penolakan", key=f"do_reject_{sub['id']}",
                                 type="primary", use_container_width=True):
                        if not reason.strip():
                            st.error("Alasan penolakan wajib diisi.")
                        else:
                            try:
                                r = requests.put(
                                    f"{API_BASE}/submissions/{sub['id']}/review",
                                    headers=auth_headers(),
                                    json={"status": "rejected", "rejection_reason": reason},
                                    timeout=8
                                )
                                if r.status_code == 200:
                                    st.success("Submission ditolak.")
                                    st.session_state[f"show_reject_{sub['id']}"] = False
                                    st.rerun()
                                else:
                                    st.error(r.json().get("detail", "Gagal reject."))
                            except Exception as e:
                                st.error(f"Error: {e}")
                with col_back:
                    if st.button("Batal", key=f"cancel_reject_{sub['id']}", use_container_width=True):
                        st.session_state[f"show_reject_{sub['id']}"] = False
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)