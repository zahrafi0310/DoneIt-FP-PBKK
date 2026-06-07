import streamlit as st
import requests
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from style import API_BASE, inject_global_css, sidebar_admin, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, HONEYDEW, DIFF_COLOR

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

CATEGORIES = {"akademik": "Akademik", "fun_things": "Fun Things",
               "soft_skill": "Soft Skill", "lifestyle": "Lifestyle"}
DIFFICULTIES = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}

def show():
    inject_global_css()
    sidebar_admin("admin_dashboard")

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Dashboard Admin
        </span>
        <div style='color:#666; font-size:0.92rem; margin-top:0.2rem;'>Manajemen Quest</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp   = requests.get(f"{API_BASE}/quests/", headers=auth_headers(), timeout=8)
        quests = resp.json() if resp.status_code == 200 else []
    except:
        quests = []
        st.error("Gagal memuat quest.")

    col_title, col_btn = st.columns([3, 1])
    with col_btn:
        if st.button("+ Quest Baru", type="primary", use_container_width=True, key="open_new_quest"):
            st.session_state.show_new_quest_form = True

    if st.session_state.get("show_new_quest_form"):
        _new_quest_form()

    if st.session_state.get("edit_quest_id"):
        _edit_quest_form(quests)
        return

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    if not quests:
        st.markdown(f"""
        <div style='background:white; border-radius:14px; padding:2rem; text-align:center;
                    color:#aaa; border:1.5px solid #f0e8e8;'>
            Belum ada quest aktif.
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <table class='admin-table'>
        <thead>
            <tr>
                <th>Judul</th>
                <th>Kategori</th>
                <th>Kesulitan</th>
                <th>XP</th>
                <th>Tenggat</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)

    for q in quests:
        diff   = q.get("difficulty", "easy")
        color  = DIFF_COLOR.get(diff, "#aaa")
        cat_lbl = CATEGORIES.get(q["category"], q["category"])

        if q.get("is_limited") and q.get("end_date"):
            try:
                dt = datetime.fromisoformat(q["end_date"])
                deadline = dt.strftime("%d %b %Y")
            except:
                deadline = q["end_date"]
        else:
            deadline = "Permanent"

        st.markdown(f"""
            <tr>
                <td style='font-weight:600;'>{q["title"]}</td>
                <td>{cat_lbl}</td>
                <td>
                    <span class='diff-badge' style='background:{color};'>{diff.capitalize()}</span>
                </td>
                <td style='font-family:Fredoka,sans-serif; font-weight:700; color:{TOMATO};'>
                    {q["xp_reward"]}
                </td>
                <td style='font-size:0.82rem; color:#888;'>{deadline}</td>
                <td></td>
            </tr>
        """, unsafe_allow_html=True)

        st.markdown("</tbody></table>", unsafe_allow_html=True)

        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            if st.button("Edit", key=f"edit_{q['id']}", use_container_width=True):
                st.session_state.edit_quest_id = q["id"]
                st.rerun()
        with col2:
            if st.button("Nonaktifkan", key=f"del_{q['id']}", use_container_width=True):
                try:
                    r = requests.delete(
                        f"{API_BASE}/quests/{q['id']}",
                        headers=auth_headers(), timeout=8
                    )
                    if r.status_code == 204:
                        st.success("Quest dinonaktifkan.")
                        st.rerun()
                    else:
                        st.error("Gagal menonaktifkan quest.")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown(f"""
        <table class='admin-table'><tbody>
        """, unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)


def _new_quest_form():
    st.markdown(f"""
    <div style='background:#fff8f8; border-radius:14px; padding:1.4rem 1.5rem;
                border:1.5px solid #f0e8e8; margin-bottom:1.2rem;'>
        <div style='font-family:Fredoka,sans-serif; font-size:1.2rem; font-weight:700;
                    color:{TOMATO}; margin-bottom:1rem;'>Quest Baru</div>
    """, unsafe_allow_html=True)

    title       = st.text_input("Judul Quest", key="nq_title")
    description = st.text_area("Deskripsi", key="nq_desc", height=100)

    col1, col2 = st.columns(2)
    with col1:
        category   = st.selectbox("Kategori", list(CATEGORIES.keys()),
                                  format_func=lambda x: CATEGORIES[x], key="nq_cat")
        difficulty = st.selectbox("Tingkat Kesulitan", list(DIFFICULTIES.keys()),
                                  format_func=lambda x: DIFFICULTIES[x], key="nq_diff")
    with col2:
        xp_reward  = st.number_input("XP Reward", min_value=10, max_value=9999,
                                     value=100, step=10, key="nq_xp")
        is_limited = st.checkbox("Quest Limited (ada tenggat waktu)", key="nq_limited")

    end_date = None
    if is_limited:
        duration_opts = {1: "1 Hari", 3: "3 Hari", 5: "5 Hari", 7: "7 Hari"}
        dur = st.selectbox("Durasi Quest", list(duration_opts.keys()),
                           format_func=lambda x: duration_opts[x], key="nq_dur")
        end_date = (datetime.now() + timedelta(days=dur)).isoformat()

    if "nq_error" in st.session_state and st.session_state.nq_error:
        st.markdown(f"""
        <div style='background:#ffd5d5; color:#8b0000; border-radius:8px;
                    padding:0.5rem 0.9rem; font-size:0.85rem; margin:0.4rem 0;'>
            {st.session_state.nq_error}
        </div>
        """, unsafe_allow_html=True)

    col_save, col_cancel = st.columns([1, 1])
    with col_save:
        if st.button("Simpan Quest", type="primary", use_container_width=True, key="save_new_quest"):
            if not title.strip() or not description.strip():
                st.session_state.nq_error = "Judul dan deskripsi wajib diisi."
                st.rerun()
            else:
                payload = {
                    "title": title, "description": description,
                    "category": category, "difficulty": difficulty,
                    "xp_reward": xp_reward, "is_limited": is_limited,
                    "end_date": end_date,
                    "start_date": datetime.now().isoformat() if is_limited else None,
                }
                try:
                    r = requests.post(
                        f"{API_BASE}/quests/",
                        headers=auth_headers(), json=payload, timeout=8
                    )
                    if r.status_code == 201:
                        st.success("Quest berhasil dibuat!")
                        st.session_state.show_new_quest_form = False
                        st.session_state.nq_error = ""
                        st.rerun()
                    else:
                        st.session_state.nq_error = r.json().get("detail", "Gagal membuat quest.")
                        st.rerun()
                except Exception as e:
                    st.session_state.nq_error = f"Error: {e}"
                    st.rerun()
    with col_cancel:
        if st.button("Batal", use_container_width=True, key="cancel_new_quest"):
            st.session_state.show_new_quest_form = False
            st.session_state.nq_error = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _edit_quest_form(quests):
    quest_id = st.session_state.get("edit_quest_id")
    q = next((x for x in quests if x["id"] == quest_id), None)
    if not q:
        st.error("Quest tidak ditemukan.")
        return

    st.markdown(f"""
    <div style='font-family:Fredoka,sans-serif; font-size:1.2rem; font-weight:700;
                color:{TOMATO}; margin-bottom:1rem;'>Edit Quest: {q["title"]}</div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='modal-box'>", unsafe_allow_html=True)

        title       = st.text_input("Judul", value=q["title"],       key="eq_title")
        description = st.text_area("Deskripsi", value=q["description"], key="eq_desc", height=100)

        col1, col2 = st.columns(2)
        with col1:
            cat_keys  = list(CATEGORIES.keys())
            cat_idx   = cat_keys.index(q["category"]) if q["category"] in cat_keys else 0
            category  = st.selectbox("Kategori", cat_keys,
                                     format_func=lambda x: CATEGORIES[x],
                                     index=cat_idx, key="eq_cat")
            diff_keys = list(DIFFICULTIES.keys())
            diff_idx  = diff_keys.index(q["difficulty"]) if q["difficulty"] in diff_keys else 0
            difficulty = st.selectbox("Kesulitan", diff_keys,
                                      format_func=lambda x: DIFFICULTIES[x],
                                      index=diff_idx, key="eq_diff")
        with col2:
            xp_reward  = st.number_input("XP Reward", min_value=10, max_value=9999,
                                         value=q["xp_reward"], step=10, key="eq_xp")
            is_limited = st.checkbox("Quest Limited", value=q.get("is_limited", False), key="eq_limited")

        end_date = q.get("end_date")
        if is_limited:
            duration_opts = {1: "1 Hari", 3: "3 Hari", 5: "5 Hari", 7: "7 Hari"}
            dur = st.selectbox("Perpanjang Durasi", list(duration_opts.keys()),
                               format_func=lambda x: duration_opts[x], key="eq_dur")
            extend = st.checkbox("Perbarui tenggat waktu dari sekarang", key="eq_extend")
            if extend:
                end_date = (datetime.now() + timedelta(days=dur)).isoformat()

        if "eq_error" in st.session_state and st.session_state.eq_error:
            st.markdown(f"""
            <div style='background:#ffd5d5; color:#8b0000; border-radius:8px;
                        padding:0.5rem 0.9rem; font-size:0.85rem; margin:0.4rem 0;'>
                {st.session_state.eq_error}
            </div>
            """, unsafe_allow_html=True)

        col_save, col_cancel = st.columns([1, 1])
        with col_save:
            if st.button("Simpan Perubahan", type="primary", use_container_width=True, key="save_edit"):
                payload = {
                    "title": title, "description": description,
                    "category": category, "difficulty": difficulty,
                    "xp_reward": xp_reward, "is_limited": is_limited,
                    "end_date": end_date,
                }
                try:
                    r = requests.put(
                        f"{API_BASE}/quests/{quest_id}",
                        headers=auth_headers(), json=payload, timeout=8
                    )
                    if r.status_code == 200:
                        st.success("Quest berhasil diperbarui!")
                        st.session_state.edit_quest_id = None
                        st.session_state.eq_error = ""
                        st.rerun()
                    else:
                        st.session_state.eq_error = r.json().get("detail", "Gagal update.")
                        st.rerun()
                except Exception as e:
                    st.session_state.eq_error = f"Error: {e}"
                    st.rerun()
        with col_cancel:
            if st.button("Kembali", use_container_width=True, key="cancel_edit"):
                st.session_state.edit_quest_id = None
                st.session_state.eq_error = ""
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)