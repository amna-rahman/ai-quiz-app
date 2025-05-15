import streamlit as st

st.set_page_config(page_title="🏠 Home - Quiz App", layout="centered")

st.title("🏠 Welcome to AI Quiz App")

# Check if user is logged in
if "user_id" in st.session_state:
    st.success(f"Hello, **{st.session_state['username']}**! 🎉")

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
else:
    st.warning("Please log in from the **Login** page in the sidebar to continue.")
