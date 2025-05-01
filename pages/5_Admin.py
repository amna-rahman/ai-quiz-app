import streamlit as st
from utils.db_utils import get_admin, get_all_users, get_all_quizzes
import json

st.set_page_config(page_title="🛠️ Admin Panel")

st.title("🛠️ Admin Dashboard")

# Session-based simple admin check
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    st.subheader("🔐 Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if get_admin(username, password):
            st.session_state["admin_logged_in"] = True
            st.success("✅ Admin logged in successfully.")
        else:
            st.error("❌ Invalid admin credentials.")

# Once logged in
if st.session_state["admin_logged_in"]:
    st.subheader("👥 Registered Users")
    users = get_all_users()
    st.table(users)

    st.subheader("📊 All Quiz Attempts")
    quizzes = get_all_quizzes()

    for i, record in enumerate(reversed(quizzes), start=1):
        st.markdown(f"### 🧾 Quiz #{i}")
        try:
            questions = json.loads(record["quiz_data"])
            st.write(f"User ID: {record['user_id']} | Score: {record['score']} / {len(questions)}")
            with st.expander("View Quiz Questions"):
                for j, q in enumerate(questions):
                    st.markdown(f"**Q{j+1}:** {q['question']}")
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.markdown(f"**Explanation:** {q.get('explanation', 'N/A')}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"⚠️ Failed to parse quiz: {e}")
