import db_utils
import json
import random

def generate_question_answer_pairs_from_text(text, num_questions=5):
    """
    Placeholder implementation:
    Generates dummy Q&A pairs from text.
    Replace this logic with a proper QA model or prompt-based LLM approach.
    """
    sentences = text.split(".")
    questions = []
    for i in range(min(num_questions, len(sentences))):
        q = f"What is the meaning of: {sentences[i].strip()}?"
        a = f"Explanation of: {sentences[i].strip()}"
        questions.append({"question": q, "answer": a})
    return questions

def score_quiz(questions, user_answers):
    """
    Compare expected answers with user's answers.
    Very basic string match for now.
    """
    score = 0
    for i in range(len(questions)):
        correct = questions[i]["answer"].strip().lower()
        user = user_answers[i].strip().lower()
        if correct == user:
            score += 1
    return score

def save_quiz_to_db(user_id, quiz_type, questions, score, learning_text=""):
    """
    Save the quiz attempt to Google Sheets via db_utils.
    """
    quiz_data = {"questions": questions}
    db_utils.insert_quiz(user_id, quiz_type, quiz_data, score, learning_text)
