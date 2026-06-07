import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from style import API_BASE, inject_global_css, sidebar_admin, TOMATO, CORAL, SKY_BLUE, SOFT_PEACH, HONEYDEW

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

CATEGORIES = {
    "akademik":  "Akademik",
    "fun_things": "Fun Things",
    "soft_skill": "Soft Skill",
    "lifestyle":  "Lifestyle",
}

CAT_COLORS = {
    "akademik":   SKY_BLUE,
    "fun_things": CORAL,
    "soft_skill": SOFT_PEACH,
    "lifestyle":  "#b5d99c",
}

def show():
    inject_global_css()
    sidebar_admin("admin_stats")

    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-family:Fredoka,sans-serif; font-size:1.8rem; font-weight:700; color:{TOMATO};'>
            Statistik Platform
        </span>
        <div style='color:#666; font-size:0.92rem; margin-top:0.2rem;'>Ringkasan aktivitas DoneIt</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.get(f"{API_BASE}/admin/stats", headers=auth_headers(), timeout=8)
        stats = resp.json() if resp.status_code == 200 else {}
    except:
        stats = {}
        st.error("Gagal memuat statistik.")

    active_users  = stats.get("active_users", 0)
    active_quests = stats.get("active_quests", 0)
    approved      = stats.get("approved", 0)
    pending       = stats.get("pending", 0)
    rejected      = stats.get("rejected", 0)
    total_subs    = stats.get("total_submissions", 0)
    by_cat        = stats.get("quests_by_category", {})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{active_users}</div>
            <div class='stat-label'>User Aktif</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{active_quests}</div>
            <div class='stat-label'>Quest Aktif</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family:Fredoka,sans-serif; font-size:1.1rem; font-weight:700;
                color:{TOMATO}; margin-bottom:0.7rem;'>
        Ringkasan Submission
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{total_subs}</div>
            <div class='stat-label'>Total Submission</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number' style='color:#276b27;'>{approved}</div>
            <div class='stat-label'>Disetujui</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number' style='color:#b8860b;'>{pending}</div>
            <div class='stat-label'>Menunggu</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number' style='color:{CORAL};'>{rejected}</div>
            <div class='stat-label'>Ditolak</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family:Fredoka,sans-serif; font-size:1.1rem; font-weight:700;
                color:{TOMATO}; margin-bottom:0.7rem;'>
        Quest Aktif per Kategori
    </div>
    """, unsafe_allow_html=True)

    cat_cols = st.columns(4)
    for col, (cat_key, cat_label) in zip(cat_cols, CATEGORIES.items()):
        count = by_cat.get(cat_key, 0)
        color = CAT_COLORS.get(cat_key, CORAL)
        with col:
            st.markdown(f"""
            <div class='stat-card' style='border-top:4px solid {color};'>
                <div class='stat-number' style='color:{color};'>{count}</div>
                <div class='stat-label'>{cat_label}</div>
            </div>
            """, unsafe_allow_html=True)