import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

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

def insert_quiz(user_id, quiz_data, score):
    quizzes_sheet.append_row([user_id, quiz_data, score])

def get_all_quizzes():
    return quizzes_sheet.get_all_records()

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
