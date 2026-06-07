import streamlit as st

API_BASE = "http://localhost:8000"

HONEYDEW   = "#F6FFEA"
SOFT_PEACH = "#FFDE96"
CORAL      = "#FA855A"
TOMATO     = "#C93638"
SKY_BLUE   = "#62C4DA"

DIFF_COLOR = {
    "easy":   "#62C4DA",
    "medium": "#FA855A",
    "hard":   "#C93638",
}

LEVEL_NAMES = {1: "Petualang", 2: "Pejuang", 3: "Legenda"}

def inject_global_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {HONEYDEW};
        font-family: 'Inter', sans-serif;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}

    [data-testid="collapsedControl"] {{ display: none !important; }}
    [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
    button[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
    [data-testid="stSidebar"] button[kind="header"] {{ display: none !important; }}
    [data-testid="stSidebarNavItems"] {{ display: none !important; }}

    [data-testid="stSidebar"] {{
        display: flex !important;
        visibility: visible !important;
        transform: translateX(0) !important;
        min-width: 200px !important;
        max-width: 200px !important;
        background-color: {TOMATO} !important;
    }}
    [data-testid="stSidebarContent"] {{
        background-color: {TOMATO} !important;
        padding-top: 1rem !important;
    }}
    [data-testid="stSidebar"] section[data-testid="stSidebarContent"] {{
        background-color: {TOMATO} !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {{
        color: {HONEYDEW} !important;
    }}
    [data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: {HONEYDEW} !important;
        border: none !important;
        text-align: left !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.65rem 1rem !important;
        border-radius: 10px !important;
        width: 100% !important;
        transition: background 0.15s !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255,255,255,0.18) !important;
    }}

    .sidebar-logo {{
        font-family: 'Fredoka', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: {HONEYDEW} !important;
        padding: 1rem 0 0.1rem 0;
        letter-spacing: 1px;
    }}
    .sidebar-tagline {{
        font-size: 0.72rem;
        color: {SOFT_PEACH} !important;
        margin-bottom: 1.5rem;
        display: block;
    }}

    .quest-card {{
        background: white;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
        border: 1.5px solid #f0e8e8;
        cursor: pointer;
        transition: box-shadow 0.15s;
    }}
    .quest-card:hover {{ box-shadow: 0 4px 18px rgba(201,54,56,0.10); }}
    .quest-card.disabled {{
        background: #e8e8e8;
        color: #aaa;
        cursor: not-allowed;
        border: 1.5px solid #ddd;
    }}

    .diff-badge {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }}

    .modal-box {{
        background: white;
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 6px 32px rgba(201,54,56,0.10);
    }}

    div[data-testid="stTextInput"] input {{
        border-radius: 10px !important;
        border: 1.5px solid #e8d8d8 !important;
    }}
    div[data-testid="stTextInput"] input:focus {{
        border-color: {CORAL} !important;
        box-shadow: 0 0 0 2px rgba(250,133,90,0.18) !important;
    }}

    .stButton > button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.15s !important;
    }}
    .stButton > button[kind="primary"] {{
        background: {TOMATO} !important;
        color: white !important;
        border: none !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: {CORAL} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: transparent;
        display: flex !important;
        width: 100% !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600;
        color: {TOMATO};
        background: #f9f0f0;
        flex: 1 1 0 !important;
        justify-content: center !important;
        text-align: center !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: {TOMATO} !important;
        color: white !important;
    }}

    .stat-card {{
        background: white;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        text-align: center;
        border: 1.5px solid #f0e8e8;
    }}
    .stat-number {{
        font-family: 'Fredoka', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: {TOMATO};
    }}
    .stat-label {{
        font-size: 0.82rem;
        color: #888;
        font-weight: 500;
        margin-top: 0.1rem;
    }}

    .admin-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }}
    .admin-table th {{
        background: {TOMATO};
        color: white;
        padding: 0.65rem 0.9rem;
        text-align: left;
        font-weight: 600;
    }}
    .admin-table td {{
        padding: 0.65rem 0.9rem;
        border-bottom: 1px solid #f0e8e8;
        vertical-align: middle;
    }}
    .admin-table tr:hover td {{ background: #fff8f8; }}

    .xp-bar-outer {{
        background: #f0e8e8;
        border-radius: 20px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin-top: 0.4rem;
    }}
    .xp-bar-inner {{
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, {CORAL}, {TOMATO});
        transition: width 0.5s;
    }}

    .submission-card {{
        background: white;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.8rem;
        border: 1.5px solid #f0e8e8;
    }}
    .submission-card.approved {{ border-color: #62C4DA; }}
    .submission-card.rejected {{ border-color: #FA855A; }}

    div[data-testid="stExpander"] {{
        border-radius: 12px !important;
        border: 1.5px solid #f0e8e8 !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def sidebar_user(current_page: str):
    with st.sidebar:
        st.markdown("<div class='sidebar-logo'>DoneIt</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-tagline'>Complete quests. Earn XP. Level up.</div>", unsafe_allow_html=True)

        pages = [("Dashboard", "dashboard"), ("Quest Saya", "my_quest"), ("Profil", "profile")]
        for label, key in pages:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin:1rem 0'>", unsafe_allow_html=True)
        if st.button("Logout", key="nav_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


def sidebar_admin(current_page: str):
    with st.sidebar:
        st.markdown("<div class='sidebar-logo'>DoneIt</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-tagline'>Admin Panel</div>", unsafe_allow_html=True)

        pages = [("Dashboard", "admin_dashboard"), ("Review Submission", "admin_review"), ("Statistik", "admin_stats")]
        for label, key in pages:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin:1rem 0'>", unsafe_allow_html=True)
        if st.button("Logout", key="nav_logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()