# backup_google_sheets


# 🗄️ Backup Google Sheets

Automated Python solution to **backup Google Sheets** from your **Google Drive** and save them directly to a **mapped network drive** on Windows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✅ Features

- 🔐 **Secure authentication** with Google Drive API (OAuth2)
- 🔍 **Filter** and list all Google Sheets files
- ⬇️ **Download** as Excel (`.xlsx`) or CSV formats
- 💾 **Save backups** to mapped network drives (e.g., `Z:\Backups\GoogleSheets`)
- 🕒 **Automate** using Windows Task Scheduler



---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/PBreno/backup_google_sheets.git
cd backup_google_sheets
```

### 2. Create and activate virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Google Drive API Setup

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Drive API**.
3. Create **OAuth 2.0 credentials** (`Desktop app`).
4. Download the `credentials.json` file.
On the first run, `token.json` will be generated after you authenticate.
`

### 5. Running the Backup

```
python src\public\main.py
```

---
## 🤝 Contributing 
Feel free to fork the repo, submit issues, or create pull requests!   
**All contributions are welcome!**


## 📧 Contact
Maintained by **[@PBreno](https://github.com/PBreno)**  
For any questions, please open an issue.