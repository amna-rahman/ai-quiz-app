import streamlit as st

st.set_page_config(page_title="🏠 Home - Quiz App", layout="centered")

st.title("🏠 Welcome to AI Quiz App")

# Check if user is logged in
if "user_id" in st.session_state:
    st.success(f"Hello, **{st.session_state['username']}**! 🎉")
    
    st.markdown("""
    ### What would you like to do today?

    - 📄 **Generate a Quiz from PDF** → Go to the sidebar and select "Quiz From PDF"
    - 🧠 **Test your knowledge** with AI-generated questions
    - 📊 **See your quiz history** 

    ---
    If you're an admin, switch to the **Admin page** from the sidebar.
    """)

    st.info("Use the sidebar to access registration, login, quiz generation, and more.")
else:
    st.warning("Please log in from the **Login** page in the sidebar to continue.")
