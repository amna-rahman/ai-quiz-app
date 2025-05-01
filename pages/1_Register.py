import streamlit as st
from utils.db_utils import insert_user

st.title("📝 User Registration")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and email and password:
        try:
            insert_user(username, password, email)
            st.success("✅ Registration successful! Go to the Login page.")
        except Exception as e:
            st.error(f"❌ {e}")
    else:
        st.warning("⚠️ Please fill all the fields.")
