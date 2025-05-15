import streamlit as st
from PyPDF2 import PdfReader
import json
from utils.db_utils import insert_quiz
from utils.llm_utils import get_gemini_response

st.set_page_config(page_title="🧠 AI Quiz Generator")

st.title("🧠 Generate Quiz from Text or PDF")

if "user_id" not in st.session_state:
    st.warning("Please log in to use this feature.")
    st.stop()

# Sidebar parameters
st.sidebar.header("📋 Quiz Settings")
num_questions = st.sidebar.slider("Number of Questions", 1, 10, 3)
quiz_type = st.sidebar.selectbox("Type", ["Select...", "Multiple-Choice", "True-False"])
difficulty = st.sidebar.selectbox("Difficulty", ["Select...", "Easy", "Medium", "Hard"])
language = st.sidebar.selectbox("Language", ["Select...", "English", "Urdu", "French"])

# Input method choice
input_method = st.radio("How would you like to provide content?", ["Paste Text", "Upload PDF"])

pdf_text = ""

if input_method == "Paste Text":
    user_text = st.text_area("Paste your paragraph or article here:")
    if user_text:
        pdf_text = user_text

elif input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        try:
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            st.success("✅ PDF uploaded and text extracted.")
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")

# Generate Quiz
if st.button("Generate Quiz"):
    if not pdf_text:
        st.warning("⚠️ Please provide some text input or upload a valid PDF.")
    elif "Select..." in [quiz_type, difficulty, language]:
        st.warning("⚠️ Please complete all quiz settings in the sidebar.")
    else:
        st.info("⏳ Generating quiz... please wait.")

        prompt = f"""
You are a quiz-generating AI. Based on the following content, create exactly {num_questions} {quiz_type.lower()} questions in {language} 
with {difficulty.lower()} difficulty.

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
\"\"\"
{pdf_text}
\"\"\"
"""

        try:
            response = get_gemini_response(prompt)

            # Clean up code block formatting if Gemini wraps it in ```json
            if response.strip().startswith("```json"):
                response = response.strip().replace("```json", "").replace("```", "").strip()

            quiz = json.loads(response)
            st.session_state["quiz"] = quiz
            st.success("✅ Quiz generated successfully!")

        except Exception as e:
            st.error(f"❌ Could not generate or parse quiz: {e}")
            st.info("🔎 Raw response below for debugging:")
            st.code(response)
            st.stop()

# Show quiz if available
if "quiz" in st.session_state:
    st.subheader("📋 Take the Quiz")
    score = 0
    answers = []

    for i, q in enumerate(st.session_state["quiz"]):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        choice = st.radio("Choose one:", q["options"], key=f"q{i}")
        answers.append((choice, q["answer"], q.get("explanation", "")))

    if st.button("Submit Quiz"):
        st.subheader("📊 Results")
        for i, (user_ans, correct_ans, explanation) in enumerate(answers):
            st.write(f"**Q{i+1}**: Your answer: `{user_ans}` | Correct: `{correct_ans}`")
            if user_ans == correct_ans:
                st.success("Correct ✅")
                score += 1
            else:
                st.error("Incorrect ❌")
            st.info(f"🧠 Explanation: {explanation}")
            st.markdown("---")

        st.success(f"🎯 Final Score: **{score}/{len(answers)}**")
        insert_quiz(st.session_state["user_id"], json.dumps(st.session_state["quiz"]), score)
