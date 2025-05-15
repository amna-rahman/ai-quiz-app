import streamlit as st
from utils.quiz_utils import generate_traditional_quiz, generate_ai_quiz, save_quiz_to_db, get_quiz_history

st.set_page_config(page_title="👩‍🏫 Admin Panel", layout="centered")
st.title("👩‍🏫 Admin Panel")

st.subheader("📚 Enter Learning Content")
learning_text = st.text_area("Paste learning content below (text only):", height=300)

quiz_type = st.radio("Select type of quiz to generate:", ["Traditional Quiz", "AI-Generated Quiz"])

if st.button("Generate Quiz"):
    if learning_text.strip():
        if quiz_type == "Traditional Quiz":
            quiz = generate_traditional_quiz(learning_text)
        else:
            quiz = generate_ai_quiz(learning_text)

        # Save the quiz to DB or in-memory store
        save_quiz_to_db(quiz, quiz_type)
        st.success(f"{quiz_type} generated and saved successfully! ✅")

        st.subheader("📝 Generated Questions:")
        for i, q in enumerate(quiz, 1):
            st.markdown(f"**{i}. {q['question']}**")
    else:
        st.warning("Please enter some learning content before generating a quiz.")

st.divider()
st.subheader("📊 Quiz History (All Users)")
history = get_quiz_history()

if history:
    for entry in history:
        st.markdown(f"**User:** {entry['user']} | **Type:** {entry['type']} | **Score:** {entry['score']}")
else:
    st.info("No quizzes taken yet.")
