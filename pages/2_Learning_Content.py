import streamlit as st
from utils.db_utils import get_latest_content

st.set_page_config(page_title="📚 Learning Content")

# --------------------------
# Authentication check
# --------------------------
if "username" not in st.session_state:
    st.warning("Please log in to access learning content.")
    st.stop()

st.title("📚 Learning Content")

# --------------------------
# Fetch and display content
# --------------------------
content = get_latest_content()

if content:
    st.markdown(content, unsafe_allow_html=True)
else:
    st.info("No learning content is available at the moment. Please check back later.")

