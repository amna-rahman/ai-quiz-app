

### ✅ `README.md` (copy-paste friendly)

```markdown
# 🤖 AI Quiz App

The **AI Quiz App** is a web-based interactive tool that lets users generate quizzes from PDFs or custom text using **Google Gemini AI**. It supports user authentication, quiz history tracking, and an admin dashboard — all built with **Streamlit** and backed by **Google Sheets**.

---

## 🚀 Features

- 🔐 User registration & login (Google Sheets backend)
- 📄 Upload a PDF or paste a paragraph to generate quizzes
- ⚙️ Choose quiz type, difficulty, and language
- 🤖 AI-generated questions with answers and explanations (Gemini API)
- 📊 Instant results and detailed quiz history
- 🛠️ Admin dashboard to view all users and quiz attempts

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini (`google-generativeai`)
- **Backend Storage**: Google Sheets (`gspread`)
- **Authentication**: Session-based (`st.session_state`)
- **Environment**: Conda or virtualenv

---

## 📁 Project Structure

```
Final app/
├── app.py
├── requirements.txt
├── .env               # (Contains API keys - not pushed)
├── gcreds.json        # (Google service account - not pushed)
├── utils/
│   ├── db_utils.py
│   └── llm_utils.py
├── pages/
│   ├── 1_Register.py
│   ├── 2_Login.py
│   ├── 3_Generate_Quiz.py
│   ├── 4_Quiz_History.py
│   └── 5_Admin.py
```

---

## 💻 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-quiz-app.git
cd ai-quiz-app
```

### 2. Set up the environment

```bash
conda create -n quiz_env python=3.10
conda activate quiz_env
pip install -r requirements.txt
```

### 3. Create a `.env` file

```env
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_API_KEY=your_gemini_api_key
```

### 4. Place `gcreds.json` in the root

> This contains your service account credentials (don't commit it to GitHub)

### 5. Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deploying on Streamlit Cloud

1. Push your project to GitHub (make sure `.env` and `gcreds.json` are in `.gitignore`)
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Select your repo and set main file as `app.py`
4. Add your **Secrets** under **Settings > Secrets** like this:

```toml
GOOGLE_SHEET_ID = "your_google_sheet_id"
GOOGLE_API_KEY = "your_gemini_api_key"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
# Paste the full contents of gcreds.json here
```

---

## 🔐 Admin Access

Use the following to log in to the admin dashboard:

- **Username:** `admin`
- **Password:** `admin123`

(You can change this in `db_utils.py`)

---

## 📌 Future Enhancements

- Timestamp and metadata for quiz history
- Export quiz history to CSV/PDF
- OpenAI fallback integration
- Responsive UI and theming

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://ai.google.dev/)
- [GSpread](https://gspread.readthedocs.io/)

