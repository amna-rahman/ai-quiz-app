import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import json
import streamlit as st

load_dotenv()

# Authorize with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open_by_key(st.secrets["GOOGLE_SHEET_ID"])

# Access the individual sheets
users_sheet = sheet.worksheet("Users")
quizzes_sheet = sheet.worksheet("Quizzes")

# Try to access LearningContent sheet or create it
try:
    content_sheet = sheet.worksheet("LearningContent")
except:
    content_sheet = sheet.add_worksheet(title="LearningContent", rows="100", cols="2")
    content_sheet.append_row(["content_id", "content_text"])  # Header row

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
            return [i + 2, row["username"]]  # +2 accounts for header row and 1-based indexing
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
    Save the learning content in the LearningContent sheet.
    Overwrites any existing content.
    """
    existing = content_sheet.get_all_values()
    if len(existing) > 1:
        content_sheet.delete_rows(2)  # Remove old content, keep header
    content_sheet.append_row(["1", content])

def get_latest_content():
    """
    Get the latest learning content from the LearningContent sheet.
    """
    records = content_sheet.get_all_records()
    return records[0]["content_text"] if records else ""
