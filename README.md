# ElevateLab-Project

# 🔐 Password Strength Analyzer with Custom Wordlist Generator

## 📌 Objective
This tool is designed to:
- Analyze the strength of user-provided passwords using real-world metrics.
- Generate custom wordlists based on user inputs for use in ethical hacking or penetration testing.

---

## 🛠️ Tools & Libraries Used
- **Python** – Core programming language.
- **argparse** – For building the command-line interface.
- **zxcvbn** – For password strength evaluation.
- **datetime** – To handle date input and formatting.
- **itertools** – For generating password combinations.
- *(Optional)* **tkinter** – For adding a GUI version.

---

## ⚙️ Features

### 1. Password Strength Analyzer
- Uses the **zxcvbn** library to:
  - Score passwords from **0 (weak)** to **4 (strong)**.
  - Estimate the time required to crack the password.
  - Provide useful **feedback and suggestions** to improve weak passwords.

### 2. Custom Wordlist Generator
- Accepts user inputs such as:
  - Name
  - Date of Birth
  - Pet Name
- Generates password guesses by:
  - Applying **leetspeak** substitutions (e.g., `a -> @, 4`).
  - Creating **uppercase/lowercase** variations.
  - Appending **years, dates**, and **special characters**.
  - Combining and permutating inputs.

---

## 🚀 How to Use

### 🔧 Analyze a Password:
```bash
python password_tool.py -p YourPassword123!
