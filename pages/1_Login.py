import streamlit as st
from utils.db_utils import insert_user

st.title("📝 Survey Access")

name = st.text_input("Your Name")
user_id = st.text_input("Your ID (or any unique identifier)")

if st.button("Start Quiz"):
    if name.strip() and user_id.strip():
        # Save to session state for quiz usage
        st.session_state["user_name"] = name.strip()
        st.session_state["user_id"] = user_id.strip()

        # Optional: save user info without password, ignore if exists
        try:
            insert_user(name.strip(), "N/A", f"{user_id.strip()}@survey.local")
        except Exception:
            pass

        st.success(f"Welcome {name}! You can now take the quiz.")
        # You can add code here to redirect to quiz page, for example:
        # st.experimental_rerun()
    else:
        st.warning("⚠️ Please enter both your name and ID.")
