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
                Buat akunmu sekarang.<br>
                Bergabung dan mulai selesaikan<br>
                quest pertamamu hari ini.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div style='padding: 2.5rem 1rem 1rem 1rem;'>", unsafe_allow_html=True)
        st.markdown("<div class='modal-box'>", unsafe_allow_html=True)

        st.markdown(f"""
        <p style='font-family:Fredoka,sans-serif; font-size:1.6rem; font-weight:700;
                  color:{TOMATO}; margin-bottom:0.2rem;'>Buat Akun</p>
        <p style='color:#888; font-size:0.88rem; margin-bottom:1.2rem;'>Daftar dan mulai petualanganmu</p>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Pilih username unik kamu", key="reg_username")
        email    = st.text_input("Email",    placeholder="email@contoh.com",          key="reg_email")
        password = st.text_input("Password", placeholder="Min. 6 karakter",
                                 type="password", key="reg_password")

        if "reg_error" in st.session_state and st.session_state.reg_error:
            st.markdown(f"""
            <div style='background:#ffd5d5; color:#8b0000; border-radius:10px;
                        padding:0.6rem 1rem; font-size:0.88rem; margin-bottom:0.5rem;'>
                {st.session_state.reg_error}
            </div>
            """, unsafe_allow_html=True)

        if "reg_success" in st.session_state and st.session_state.reg_success:
            st.markdown("""
            <div style='background:#d4f7d4; color:#276b27; border-radius:10px;
                        padding:0.6rem 1rem; font-size:0.88rem; margin-bottom:0.5rem;'>
                Registrasi berhasil! Mengarahkan ke dashboard...
            </div>
            """, unsafe_allow_html=True)

        if st.button("Daftar", use_container_width=True, type="primary", key="btn_register"):
            if not username or not email or not password:
                st.session_state.reg_error = "Semua field wajib diisi."
                st.session_state.reg_success = False
                st.rerun()
            elif len(password) < 6:
                st.session_state.reg_error = "Password minimal 6 karakter."
                st.session_state.reg_success = False
                st.rerun()
            else:
                try:
                    resp = requests.post(
                        f"{API_BASE}/auth/register",
                        json={"username": username, "email": email, "password": password},
                        timeout=8
                    )
                    if resp.status_code == 201:
                        login_resp = requests.post(
                            f"{API_BASE}/auth/login",
                            json={"username": username, "password": password},
                            timeout=8
                        )
                        if login_resp.status_code == 200:
                            data = login_resp.json()
                            st.session_state.token = data["access_token"]
                            me = requests.get(
                                f"{API_BASE}/auth/me",
                                headers={"Authorization": f"Bearer {data['access_token']}"},
                                timeout=8
                            ).json()
                            st.session_state.user = me
                            st.session_state.reg_error = ""
                            st.session_state.reg_success = True
                            st.session_state.page = "dashboard"
                            st.rerun()
                    else:
                        err = resp.json().get("detail", "Registrasi gagal.")
                        st.session_state.reg_error = err
                        st.session_state.reg_success = False
                        st.rerun()
                except Exception as e:
                    st.session_state.reg_error = f"Tidak bisa terhubung ke server: {e}"
                    st.session_state.reg_success = False
                    st.rerun()

        st.markdown(f"""
        <div style='text-align:center; margin-top:1.2rem; font-size:0.88rem; color:#888;'>
            Sudah punya akun?
        </div>
        """, unsafe_allow_html=True)

        if st.button("Masuk di sini", use_container_width=True, key="btn_go_login"):
            st.session_state.page = "login"
            st.session_state.reg_error = ""
            st.session_state.reg_success = False
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)