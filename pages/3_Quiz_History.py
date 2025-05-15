import streamlit as st
import json
from utils.db_utils import get_all_quizzes

st.set_page_config(page_title="📊 Quiz History")

st.title("📊 Your Quiz History")

# ------------------------------
# Authentication check
# ------------------------------
if "user_id" not in st.session_state or "username" not in st.session_state:
    st.warning("Please log in to view your quiz history.")
    st.stop()

user_id = str(st.session_state["user_id"])

# ------------------------------
# Fetch and filter quizzes
# ------------------------------
all_quizzes = get_all_quizzes()
user_quizzes = [q for q in all_quizzes if str(q.get("user_id")) == user_id]

if not user_quizzes:
    st.info("You haven't taken any quizzes yet.")
    st.stop()

st.success(f"You have taken {len(user_quizzes)} quiz attempt(s).")

# ------------------------------
# Display quiz history
# ------------------------------
for idx, quiz_record in enumerate(reversed(user_quizzes), start=1):
    st.markdown(f"---\n### 🧾 Quiz #{idx} - *{quiz_record.get('quiz_type', 'N/A')}*")
    st.write(f"**Score:** {quiz_record.get('score', 'N/A')}")

    # Try to parse quiz_data JSON
    try:
        questions = json.loads(quiz_record.get("quiz_data", "[]"))
    except json.JSONDecodeError:
        st.error("❌ Failed to load quiz questions.")
        continue

    with st.expander("📋 View Questions"):
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q.get('question', 'N/A')}**")
            st.markdown(f"- **Correct Answer:** {q.get('answer', 'N/A')}")
            st.markdown(f"- **Explanation:** {q.get('explanation', 'N/A')}")
            st.markdown("")

    st.caption(f"🕒 Attempted on: {quiz_record.get('timestamp', 'Unknown')}")
