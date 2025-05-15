import streamlit as st
from utils.db_utils import insert_user

st.set_page_config(page_title="🏠 Home - Quiz App", layout="centered")

st.title("🏠 Welcome to AI Quiz App")

if "user_id" not in st.session_state:
    st.subheader("📝 Survey Access / Login")
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
            st.info("Use the sidebar to access **Learning Content**, **Take Quizzes**, and **Review History**.")
            st.experimental_rerun()  # Refresh to update UI after login
        else:
            st.warning("⚠️ Please enter both your name and ID.")
else:
    # User is logged in
    st.success(f"Hello, **{st.session_state['user_name']}**! 🎉")
    
    is_admin = st.session_state.get("is_admin", False)

    if is_admin:
        st.markdown("""
        ### 👩‍🏫 Admin Dashboard
        
        - ✍️ **Enter learning content** for users to read
        - 🧠 **Generate two quizzes** from the text:
            - Traditional quiz (based on direct content)
            - AI-generated quiz (from Google Gemini)
        - 📥 **View and export user quiz results**

        Use the sidebar to go to the **Admin** page.
        """)
    else:
        st.markdown("""
        ### 🎓 User Dashboard

        - 📖 **Read the learning content** provided by the admin
        - 📝 **Take two quizzes** based on the content:
            - Traditional Quiz
            - AI-Generated Quiz
        - 📊 **View your quiz history and performance**

        Use the sidebar to go to **Learning Content** and then **Take Quizzes**.
        """)

    st.info("Use the sidebar to access all features.")
