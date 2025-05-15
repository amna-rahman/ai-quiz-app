import streamlit as st
import json
from utils.db_utils import get_admin, get_all_users, get_all_quizzes, save_learning_content
from utils.quiz_utils import generate_ai_quiz, generate_traditional_quiz  # You’ll add these
import pandas as pd

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

# -------------------------------
# Once logged in as Admin
# -------------------------------
if st.session_state["admin_logged_in"]:

    st.subheader("📘 Enter Learning Content")
    content = st.text_area("Paste learning material here (text only):", height=300)

    if st.button("💾 Save Content"):
        if content.strip():
            save_learning_content(content)  # You define this function to store in Google Sheet or JSON
            st.session_state["learning_content"] = content
            st.success("✅ Content saved successfully.")
        else:
            st.warning("⚠️ Please enter some content first.")

    if "learning_content" in st.session_state:
        with st.expander("👁 Preview Current Learning Content"):
            st.markdown(st.session_state["learning_content"])

        st.markdown("---")
        st.subheader("🧠 Generate Quizzes from Content")

        if st.button("📜 Generate Traditional Quiz"):
            traditional_quiz = generate_traditional_quiz(st.session_state["learning_content"])
            st.session_state["traditional_quiz"] = traditional_quiz
            st.success("✅ Traditional Quiz generated.")

        if st.button("🤖 Generate AI Quiz"):
            ai_quiz = generate_ai_quiz(st.session_state["learning_content"])
            st.session_state["ai_quiz"] = ai_quiz
            st.success("✅ AI Quiz generated.")

        # Optional: Preview
        if "traditional_quiz" in st.session_state:
            with st.expander("📋 Traditional Quiz"):
                for q in st.session_state["traditional_quiz"]:
                    st.write(f"Q: {q['question']}")
                    st.write(f"A: {q['answer']}")

        if "ai_quiz" in st.session_state:
            with st.expander("🤖 AI Quiz"):
                for q in st.session_state["ai_quiz"]:
                    st.write(f"Q: {q['question']}")
                    st.write(f"A: {q['answer']}")
                    st.write(f"Explanation: {q.get('explanation', 'N/A')}")
    
    # --------------------
    # Admin views all data
    # --------------------
    with st.expander("📊 All Users"):
        users = get_all_users()
        st.table(users)

    with st.expander("📝 All Quiz Attempts"):
        quizzes = get_all_quizzes()

        records = []
        for record in quizzes:
            try:
                questions = json.loads(record["quiz_data"])
                records.append({
                    "User ID": record['user_id'],
                    "Score": f"{record['score']} / {len(questions)}",
                    "Total Questions": len(questions)
                })
            except:
                pass

        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
            st.download_button("⬇️ Download as Excel", data=df.to_excel(index=False), file_name="quiz_results.xlsx")
