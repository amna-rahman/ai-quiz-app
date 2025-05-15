def generate_traditional_quiz(content):
    # This is a placeholder. You can improve it later using NLP or LLM.
    sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
    quiz = [{"question": f"What does this sentence mean? '{s}'", "answer": s} for s in sentences[:5]]
    return quiz

def generate_ai_quiz(content):
    # You can later call Gemini or OpenAI here.
    # For now, just mock with a different format.
    return [
        {"question": f"What is a key concept from this content?", "answer": "AI-generated answer 1"},
        {"question": f"What can we infer from this content?", "answer": "AI-generated answer 2"}
    ]

# Temporary in-memory quiz history
quiz_db = []
quiz_history = []

def save_quiz_to_db(quiz, quiz_type):
    quiz_db.append({
        "type": quiz_type,
        "questions": quiz
    })

def get_quiz_history():
    # Example: Return mock data or load from your DB
    return quiz_history
