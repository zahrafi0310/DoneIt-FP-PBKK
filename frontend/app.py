import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="DoneIt",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded",
)

defaults = {
    "page": "login",
    "token": None,
    "user": None,
    "login_error": "",
    "reg_error": "",
    "reg_success": False,
    "submit_quest_id": None,
    "submit_quest_title": None,
    "submit_error": "",
    "show_new_quest_form": False,
    "edit_quest_id": None,
    "nq_error": "",
    "eq_error": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

page = st.session_state.page

if page == "login":
    from pages.login import show
    show()

elif page == "register":
    from pages.register import show
    show()

elif page == "dashboard":
    from pages.dashboard import show
    show()

elif page == "my_quest":
    from pages.my_quest import show
    show()

elif page == "profile":
    from pages.profile import show
    show()

elif page == "admin_dashboard":
    from pages.admin.dashboard import show
    show()

elif page == "admin_review":
    from pages.admin.review import show
    show()

elif page == "admin_stats":
    from pages.admin.stats import show
    show()

else:
    st.session_state.page = "login"
    st.rerun()