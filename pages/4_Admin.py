import streamlit as st
import json
import pandas as pd
from utils.db_utils import get_admin, get_all_users, get_all_quizzes, save_learning_content, get_latest_content
from utils.quiz_utils import generate_traditional_quiz
from utils.llm_utils import get_gemini_response

st.set_page_config(page_title="🛠️ Admin Panel")

st.title("🛠️ Admin Dashboard")

# Simple admin login check
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

def load_content():
    st.session_state["learning_content"] = get_latest_content()

if not st.session_state["admin_logged_in"]:
    st.subheader("🔐 Admin Login")
    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if get_admin(username, password):
            st.session_state["admin_logged_in"] = True
            load_content()
            st.success("✅ Admin logged in successfully.")
        else:
            st.error("❌ Invalid admin credentials.")
    st.stop()

# Admin is logged in below

st.subheader("📘 Enter Learning Content (Text Only, max 5000 chars)")
content = st.text_area("Paste learning material here:", value=st.session_state.get("learning_content", ""), height=300, max_chars=5000)

if st.button("💾 Save Content"):
    if content.strip():
        save_learning_content(content)
        st.session_state["learning_content"] = content
        st.success("✅ Content saved successfully.")
    else:
        st.warning("⚠️ Please enter some content first.")

if "learning_content" in st.session_state and st.session_state["learning_content"]:
    with st.expander("👁 Preview Current Learning Content"):
        st.markdown(st.session_state["learning_content"])

    st.markdown("---")
    st.subheader("🧠 Generate Quizzes from Content (max 5 questions each)")

    if st.button("📜 Generate Traditional Quiz"):
        traditional_quiz = generate_traditional_quiz(st.session_state["learning_content"], max_questions=5)
        st.session_state["traditional_quiz"] = traditional_quiz
        st.success("✅ Traditional Quiz generated.")

    if st.button("🤖 Generate AI Quiz"):
        prompt = f"""
You are a quiz-generating AI. Based on the following content, create exactly 5 multiple-choice questions in English with medium difficulty.

Return ONLY a JSON array in this exact format:

[
  {{
    "question": "What is ...?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option B",
    "explanation": "Explanation here."
  }},
  ...
]

Content:
\"\"\"{st.session_state["learning_content"]}\"\"\"
"""
        try:
            response = get_gemini_response(prompt)
            if response.strip().startswith("```json"):
                response = response.strip().replace("```json", "").replace("```", "").strip()
            ai_quiz = json.loads(response)
            st.session_state["ai_quiz"] = ai_quiz
            st.success("✅ AI Quiz generated.")
        except Exception as e:
            st.error(f"❌ Could not generate or parse AI quiz: {e}")
            st.info("🔎 Raw response for debugging:")
            st.code(response)

    # Preview quizzes
    if "traditional_quiz" in st.session_state:
        with st.expander("📋 Traditional Quiz Preview"):
            for i, q in enumerate(st.session_state["traditional_quiz"], 1):
                st.write(f"Q{i}: {q['question']}")
                if "options" in q:
                    for opt in q["options"]:
                        st.write(f"- {opt}")
                st.write(f"Answer: {q['answer']}")

    if "ai_quiz" in st.session_state:
        with st.expander("🤖 AI Quiz Preview"):
            for i, q in enumerate(st.session_state["ai_quiz"], 1):
                st.write(f"Q{i}: {q['question']}")
                for opt in q["options"]:
                    st.write(f"- {opt}")
                st.write(f"Answer: {q['answer']}")
                st.write(f"Explanation: {q.get('explanation', 'N/A')}")

    st.markdown("---")
    st.subheader("📊 All Users and Quiz Results")

    users = get_all_users()
    quizzes = get_all_quizzes()

    if users:
        st.write(f"Total users: {len(users)}")
        st.dataframe(users)

    records = []
    for record in quizzes:
        try:
            quiz_data = json.loads(record["quiz_data"])
            total_questions = len(quiz_data)
            records.append({
                "User ID": record["user_id"],
                "Score": f"{record['score']} / {total_questions}",
                "Total Questions": total_questions,
                "Quiz Type": record.get("quiz_type", "N/A"),
                "Date": record.get("created_at", "N/A")
            })
        except:
            continue

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df)
        excel_data = df.to_excel(index=False)
        st.download_button(
            label="⬇️ Download Quiz Results as Excel",
            data=excel_data,
            file_name="quiz_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
