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

# Add a new user
def insert_user(username, password, email):
    existing = users_sheet.get_all_records()
    for row in existing:
        if row["username"] == username:
            raise Exception("Username already exists.")
    users_sheet.append_row([username, password, email])

# Authenticate user
def get_user(username, password):
    records = users_sheet.get_all_records()
    for i, row in enumerate(records):
        if row["username"] == username and row["password"] == password:
            return [i+2, row["username"]]  # +2 accounts for header row and 1-based indexing
    return None

# Save quiz results
def insert_quiz(user_id, quiz_data, score):
    quizzes_sheet.append_row([user_id, quiz_data, score])

# Admin login (simple)
def get_admin(username, password):
    return username == "admin" and password == "admin123"

# List all users
def get_all_users():
    return users_sheet.get_all_records()

# List all quizzes
def get_all_quizzes():
    return quizzes_sheet.get_all_records()
