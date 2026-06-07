import streamlit as st
import requests
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from style import API_BASE, inject_global_css, TOMATO, CORAL, SOFT_PEACH, HONEYDEW

def show():
    inject_global_css()

    left, right = st.columns([1, 1])

    with left:
        st.markdown(f"""
        <div style='display:flex; flex-direction:column; justify-content:center;
                    height:100%; padding: 4rem 2rem 2rem 2rem; text-align:left;'>
            <div style='font-family:Fredoka,sans-serif; font-size:4rem; font-weight:700;
                        color:{TOMATO}; line-height:1;'>DoneIt</div>
            <div style='color:{CORAL}; font-size:1.05rem; font-weight:600; margin-top:0.6rem;'>
                Complete quests. Earn XP. Level up.
            </div>
            <div style='margin-top:1.5rem; color:#666; font-size:0.92rem; line-height:1.7;'>
                Platform gamifikasi kampus.<br>
                Selesaikan tantangan, kumpulkan XP,<br>
                dan buktikan kemampuanmu.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='padding: 3rem 1rem 1rem 1rem;'>", unsafe_allow_html=True)
        st.markdown("<div class='modal-box'>", unsafe_allow_html=True)

        st.markdown(f"""
        <p style='font-family:Fredoka,sans-serif; font-size:1.6rem; font-weight:700;
                  color:{TOMATO}; margin-bottom:0.2rem;'>Masuk</p>
        <p style='color:#888; font-size:0.88rem; margin-bottom:1.2rem;'>Selamat datang kembali</p>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Masukkan username", key="login_username")
        password = st.text_input("Password", placeholder="Masukkan password", type="password", key="login_password")

        if "login_error" in st.session_state and st.session_state.login_error:
            st.markdown(f"""
            <div style='background:#ffd5d5; color:#8b0000; border-radius:10px;
                        padding:0.6rem 1rem; font-size:0.88rem; margin-bottom:0.5rem;'>
                {st.session_state.login_error}
            </div>
            """, unsafe_allow_html=True)

        if st.button("Masuk", use_container_width=True, type="primary", key="btn_login"):
            if not username or not password:
                st.session_state.login_error = "Username dan password wajib diisi."
                st.rerun()
            else:
                try:
                    resp = requests.post(
                        f"{API_BASE}/auth/login",
                        json={"username": username, "password": password},
                        timeout=8
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.token = data["access_token"]
                        me = requests.get(
                            f"{API_BASE}/auth/me",
                            headers={"Authorization": f"Bearer {data['access_token']}"},
                            timeout=8
                        ).json()
                        st.session_state.user = me
                        st.session_state.login_error = ""
                        if me.get("is_admin"):
                            st.session_state.page = "admin_dashboard"
                        else:
                            st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        err = resp.json().get("detail", "Login gagal.")
                        st.session_state.login_error = err
                        st.rerun()
                except Exception as e:
                    st.session_state.login_error = f"Tidak bisa terhubung ke server: {e}"
                    st.rerun()

        st.markdown(f"""
        <div style='text-align:center; margin-top:1.2rem; font-size:0.88rem; color:#888;'>
            Belum punya akun?
        </div>
        """, unsafe_allow_html=True)

        if st.button("Daftar di sini", use_container_width=True, key="btn_go_register"):
            st.session_state.page = "register"
            st.session_state.login_error = ""
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)