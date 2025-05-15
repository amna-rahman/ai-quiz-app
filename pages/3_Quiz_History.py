import streamlit as st
import json
from utils.db_utils import get_all_quizzes

st.set_page_config(page_title="📊 Quiz History")

st.title("📊 Your Quiz History")

# Check if user is logged in
if "user_id" not in st.session_state:
    st.warning("Please log in to view your quiz history.")
    st.stop()

user_id = st.session_state["user_id"]

# Fetch all quizzes
all_quizzes = get_all_quizzes()

# Filter quizzes by current user
user_quizzes = [q for q in all_quizzes if str(q["user_id"]) == str(user_id)]

if not user_quizzes:
    st.info("You haven't taken any quizzes yet.")
else:
    st.success(f"You have taken {len(user_quizzes)} quiz attempt(s).")

    for idx, quiz_record in enumerate(reversed(user_quizzes), start=1):
        st.markdown(f"### 🧾 Quiz #{idx}")
        try:
            questions = json.loads(quiz_record["quiz_data"])
            score = quiz_record["score"]
            total = len(questions)
        except Exception as e:
            st.error(f"⚠️ Error loading quiz: {e}")
            continue

        st.write(f"**Score:** {score} / {total}")
        with st.expander("📋 View Questions"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                st.markdown(f"**Correct Answer:** {q['answer']}")
                st.markdown(f"**Explanation:** {q.get('explanation', 'N/A')}")
                st.markdown("---")
