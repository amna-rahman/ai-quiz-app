import streamlit as st
from utils.quiz_utils import generate_traditional_quiz, generate_ai_quiz
from utils.db_utils import save_learning_content, save_quiz_to_db, get_all_quiz_results_with_users, get_admin

st.set_page_config(page_title="👩‍🏫 Admin Panel", layout="centered")
st.title("👩‍🏫 Admin Panel")

# --- Admin Login ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.subheader("🔐 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if get_admin(username, password):
            st.session_state.admin_logged_in = True
            st.success("Logged in successfully as admin!")
            st.experimental_rerun()
        else:
            st.error("Invalid admin credentials.")
    st.stop()

# --- Content Entry ---
st.subheader("📚 Enter Learning Content")
learning_text = st.text_area("Paste learning content below (text only):", height=300)
quiz_type = st.radio("Select type of quiz to generate:", ["Traditional Quiz", "AI-Generated Quiz"])

if st.button("Generate Quiz"):
    if learning_text.strip():
        # Save learning content
        save_learning_content(learning_text)

        # Generate quiz (always 5 questions)
        if quiz_type == "Traditional Quiz":
            quiz = generate_traditional_quiz(learning_text)
        else:
            quiz = generate_ai_quiz(learning_text)

        if len(quiz) != 5:
            st.warning("Quiz must contain exactly 5 questions. Current count: {}".format(len(quiz)))
        else:
            save_quiz_to_db(quiz, quiz_type, learning_text)
            st.success(f"{quiz_type} generated and saved successfully! ✅")

            st.subheader("📝 Generated Questions:")
            for i, q in enumerate(quiz, 1):
                st.markdown(f"**{i}. {q['question']}**")
                st.markdown(f"**Correct Answer:** {q['answer']}")
                st.markdown("---")
    else:
        st.warning("Please enter some learning content before generating a quiz.")

st.divider()
st.subheader("📊 Quiz History (All Users)")
history = get_all_quiz_results_with_users()

if history:
    for entry in history:
        st.markdown(f"**User:** {entry['username']} | **Email:** {entry['email']} | **Type:** {entry['quiz_type']} | **Score:** {entry['score']} | **Time:** {entry['timestamp']}")
        st.markdown("---")
    
    if st.download_button("🗃️ Download All Results as Excel", data=None, file_name="quiz_results.xlsx", disabled=True):
        st.info("Download functionality not implemented in this snippet.")
else:
    st.info("No quizzes taken yet.")
