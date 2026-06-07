import streamlit as st
import requests
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from style import API_BASE, inject_global_css, sidebar_user, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, DIFF_COLOR

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def is_expired(quest):
    if not quest.get("is_limited"):
        return False
    end_date = quest.get("end_date")
    if not end_date:
        return False
    try:
        dt = datetime.fromisoformat(end_date)
        return datetime.now() > dt
    except:
        return False

def show():
    inject_global_css()
    sidebar_user("my_quest")

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Quest Saya
        </span>
        <div style='color:#666; font-size:0.92rem; margin-top:0.2rem;'>
            Daftar quest yang kamu terima
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("submit_quest_id"):
        _show_submit_form()
        return

    try:
        resp = requests.get(f"{API_BASE}/quests/my", headers=auth_headers(), timeout=8)
        my_quests = resp.json() if resp.status_code == 200 else []
    except:
        my_quests = []
        st.error("Gagal memuat quest.")

    if not my_quests:
        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:2rem; text-align:center;
                    color:#aaa; border:1.5px solid #f0e8e8;'>
            Kamu belum menerima quest apapun.<br>
            <span style='font-size:0.85rem;'>Pergi ke Dashboard untuk browse quest.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    for aq in my_quests:
        q = aq["quest"]
        expired = is_expired(q)
        diff    = q.get("difficulty", "easy")
        color   = DIFF_COLOR.get(diff, "#aaa")

        if q.get("is_limited") and q.get("end_date"):
            try:
                dt = datetime.fromisoformat(q["end_date"])
                deadline_text = dt.strftime("%d %b %Y, %H:%M")
            except:
                deadline_text = q["end_date"]
        else:
            deadline_text = "Permanent"

        card_style = "opacity:0.45; pointer-events:none;" if expired else ""
        border_col = "#ddd" if expired else "#f0e8e8"

        st.markdown(f"""
        <div style='background:{"#f0f0f0" if expired else "white"}; border-radius:14px;
                    padding:1rem 1.2rem; margin-bottom:0.5rem;
                    border:1.5px solid {border_col};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='font-weight:700; font-size:1rem; color:{"#aaa" if expired else "#222"};'>
                        {q["title"]}
                    </span>
                    &nbsp;
                    <span class='diff-badge' style='background:{"#bbb" if expired else color};'>
                        {diff.capitalize()}
                    </span>
                </div>
                <div style='font-family:Fredoka,sans-serif; font-size:1.2rem;
                            font-weight:700; color:{"#aaa" if expired else TOMATO};'>
                    {q["xp_reward"]} XP
                </div>
            </div>
            <div style='font-size:0.8rem; color:#aaa; margin-top:0.3rem;'>
                {"[EXPIRED] " if expired else ""}Tenggat: {deadline_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not expired:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Submit Quest", key=f"submit_btn_{aq['id']}", type="primary", use_container_width=True):
                    st.session_state.submit_quest_id  = q["id"]
                    st.session_state.submit_quest_title = q["title"]
                    st.rerun()
            with col2:
                if st.button("Batalkan Quest", key=f"cancel_btn_{aq['id']}", use_container_width=True):
                    try:
                        r = requests.post(
                            f"{API_BASE}/quests/{q['id']}/cancel",
                            headers=auth_headers(), timeout=8
                        )
                        if r.status_code == 200:
                            st.success("Quest dibatalkan.")
                            st.rerun()
                        else:
                            st.error(r.json().get("detail", "Gagal membatalkan."))
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown("<div style='margin-bottom:0.6rem;'></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)


def _show_submit_form():
    quest_id    = st.session_state.get("submit_quest_id")
    quest_title = st.session_state.get("submit_quest_title", "Quest")

    st.markdown(f"""
    <div style='margin-bottom:1.2rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.4rem; font-weight:700; color:{TOMATO};'>
            Submit: {quest_title}
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='modal-box'>", unsafe_allow_html=True)

        photo = st.file_uploader("Foto Bukti", type=["jpg", "jpeg", "png"], key="submit_photo")
        description = st.text_area("Deskripsi Singkat", placeholder="Ceritakan apa yang kamu lakukan...",
                                   key="submit_desc", height=120)

        if "submit_error" in st.session_state and st.session_state.submit_error:
            st.markdown(f"""
            <div style='background:#ffd5d5; color:#8b0000; border-radius:10px;
                        padding:0.6rem 1rem; font-size:0.88rem; margin-bottom:0.5rem;'>
                {st.session_state.submit_error}
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Kirim Submission", type="primary", use_container_width=True, key="do_submit"):
                if not photo:
                    st.session_state.submit_error = "Foto bukti wajib diunggah."
                    st.rerun()
                elif not description.strip():
                    st.session_state.submit_error = "Deskripsi wajib diisi."
                    st.rerun()
                else:
                    try:
                        files = {"photo": (photo.name, photo.getvalue(), photo.type)}
                        data  = {"quest_id": quest_id, "description": description}
                        r = requests.post(
                            f"{API_BASE}/submissions/",
                            headers=auth_headers(),
                            files=files,
                            data=data,
                            timeout=15
                        )
                        if r.status_code == 200:
                            st.success("Submission berhasil dikirim!")
                            st.session_state.submit_quest_id    = None
                            st.session_state.submit_quest_title = None
                            st.session_state.submit_error       = ""
                            st.rerun()
                        else:
                            st.session_state.submit_error = r.json().get("detail", "Gagal submit.")
                            st.rerun()
                    except Exception as e:
                        st.session_state.submit_error = f"Error: {e}"
                        st.rerun()
        with col2:
            if st.button("Kembali", use_container_width=True, key="back_from_submit"):
                st.session_state.submit_quest_id    = None
                st.session_state.submit_quest_title = None
                st.session_state.submit_error       = ""
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)