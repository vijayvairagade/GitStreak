# GitStreak

## 🕒 GitHub README Timestamp Updater

> ⚙️ Automatically updates your GitHub repository's `README.md` file with a current timestamp at random intervals using the GitHub API.

---

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![GitHub API](https://img.shields.io/badge/API-GitHub%20v3-orange)
![Automation](https://img.shields.io/badge/Automation-Cron%20style-green)

---
## ⛔ Make sure to create a new and PRIVATE repository for this.

## 📌 Features

* 🤖 **Automatic README updates** with a "Last Seen" timestamp
* ⏱️ **Random interval updates** between 1 and 6 hours
* 🔒 **Secure GitHub token authentication**
* 📁 Supports **custom README path**
* 🌐 Can be hosted on remote servers (e.g., EC2, DigitalOcean, etc.)
* 🔧 Optional **`.env` support** via `python-dotenv`

---

## 🛠️ Requirements

* Python 3.7+
* GitHub Personal Access Token (with `repo` or `contents:write` scope)


> Make sure to install `python-dotenv` if you want to use `.env` file support:

```bash
pip install python-dotenv
```

---

## 📁 .env File Example

You can configure your environment securely using a `.env` file:

```env
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_username
GITHUB_REPO=your_repository_name
README_PATH=README.md  # optional if your file is named differently
```

---

## 🚀 Usage

### 🔁 Run the script

```bash
python main.py
```

### 🧪 You will be prompted for:

* GitHub token (if not found in environment)
* GitHub username
* Repository name
* (Optional) Custom README path

Once started, it will:

* Connect to your GitHub repo
* Retrieve your `README.md`
* Inject or update a line like:

```markdown
Last Seen - 03:24PM 14/07/2025 Monday
```

* Push the update as a commit
* Sleep for 1 to 6 hours and repeat

---

## 📸 Example Output

```
🚀 GitHub README Timestamp Updater started!
✅ Connected to repository: vijayvairagade/github-auto-timestamp
✅ Successfully updated README.md on GitHub
⏳ Next update in: 2h 47m
```

---

## ⛔ Stop the Script

Use `Ctrl + C` to manually stop the continuous update loop.

---

## ❓ FAQ

**Q:** What permissions should my GitHub token have?
**A:** It needs `repo` or `contents:write` permission to update files in a private or public repo.

**Q:** Will this overwrite the whole README?
**A:** No. It only replaces or appends the timestamp line that matches this pattern:

```regex
Example
Last Seen - 10:12AM 14/07/2025 Monday
```

**Q:** Can I run this on a server or as a background service?
**A:** Absolutely! It's designed for continuous, unattended operation.

---

## 👨‍💻 Author

**Vijay Vairagade**
© 2025 - All rights reserved.

---
