import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import json
from datetime import datetime

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from streamlit secrets (make sure you set these in your Streamlit secrets)
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# Open your Google Sheet by key
sheet = client.open_by_key(st.secrets["GOOGLE_SHEET_ID"])

# Access worksheets
users_sheet = sheet.worksheet("Users")
quizzes_sheet = sheet.worksheet("Quizzes")

# Try to get or create LearningContent worksheet
try:
    content_sheet = sheet.worksheet("LearningContent")
except gspread.exceptions.WorksheetNotFound:
    content_sheet = sheet.add_worksheet(title="LearningContent", rows="100", cols="2")
    content_sheet.append_row(["content_id", "content_text"])  # Add header

# -------------------------------
# USER MANAGEMENT
# -------------------------------

def insert_user(username, password, email):
    existing = users_sheet.get_all_records()
    for row in existing:
        if row["username"] == username:
            raise Exception("Username already exists.")
    users_sheet.append_row([username, password, email])

def get_user(username, password):
    records = users_sheet.get_all_records()
    for i, row in enumerate(records):
        if row["username"] == username and row["password"] == password:
            # Return row number and username (row index + header + 1)
            return [i + 2, row["username"]]
    return None

def get_all_users():
    return users_sheet.get_all_records()

# -------------------------------
# QUIZ MANAGEMENT
# -------------------------------

def insert_quiz(user_id, quiz_type, quiz_data, score):
    """
    Insert a quiz attempt for a user.

    Args:
        user_id (int or str): User identifier (row number or username)
        quiz_type (str): "traditional" or "ai_generated"
        quiz_data (dict or str): Quiz data (questions/answers), saved as JSON string
        score (int): User's quiz score
    """
    if isinstance(quiz_data, dict):
        quiz_data_str = json.dumps(quiz_data)
    else:
        quiz_data_str = str(quiz_data)

    timestamp = datetime.utcnow().isoformat()
    quizzes_sheet.append_row([user_id, quiz_type, quiz_data_str, score, timestamp])

def get_all_quizzes():
    """
    Returns all quiz attempts as list of dicts with keys:
    user_id, quiz_type, quiz_data (json string), score, timestamp
    """
    return quizzes_sheet.get_all_records()

def get_all_quiz_results_with_users():
    """
    Combines quiz attempts with user info for admin reports.
    Returns list of dicts with keys:
    username, email, quiz_type, quiz_data, score, timestamp
    """
    users = users_sheet.get_all_records()
    quizzes = quizzes_sheet.get_all_records()

    # Build a map user_id -> user info (assuming user_id is row number - 2)
    user_map = {}
    for idx, user in enumerate(users):
        user_map[str(idx + 2)] = user  # key is string of row number

    results = []
    for q in quizzes:
        user_id = str(q.get("user_id"))
        user_info = user_map.get(user_id, {})
        result = {
            "username": user_info.get("username", "Unknown"),
            "email": user_info.get("email", ""),
            "quiz_type": q.get("quiz_type", ""),
            "quiz_data": q.get("quiz_data", ""),
            "score": q.get("score", ""),
            "timestamp": q.get("timestamp", "")
        }
        results.append(result)
    return results

# -------------------------------
# ADMIN AUTHENTICATION
# -------------------------------

def get_admin(username, password):
    return username == "admin" and password == "admin123"

# -------------------------------
# LEARNING CONTENT MANAGEMENT
# -------------------------------

def save_learning_content(content):
    """
    Overwrite existing content with new content in LearningContent sheet.
    """
    existing = content_sheet.get_all_values()
    # Delete all rows except header if content exists
    if len(existing) > 1:
        content_sheet.delete_rows(2, len(existing))
    content_sheet.append_row(["1", content])

def get_latest_content():
    records = content_sheet.get_all_records()
    return records[0]["content_text"] if records else ""
