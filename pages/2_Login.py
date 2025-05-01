import streamlit as st
from utils.db_utils import get_user

st.title("🔐 User Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username and password:
        user = get_user(username, password)
        if user:
            st.session_state["user_id"] = user[0]
            st.session_state["username"] = user[1]
            st.success("✅ Login successful! Return to Home page.")
        else:
            st.error("❌ Invalid username or password.")
    else:
        st.warning("⚠️ Please enter both username and password.")
