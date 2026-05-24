# 🚀 Automated Job Hunter

This is an automated Python background system designed to scrape various remote and local job boards for Software Engineering roles (specifically Python, PERN stack, Backend, Fullstack) and send real-time alerts via Telegram.

## 📁 Project Structure

* `engine.py`: The core brain. Aggregates jobs, checks the database, and triggers Telegram alerts.
* `db_manager.py`: Manages the local `jobs.db` SQLite database to ensure you never get duplicate alerts.
* `telegram_bot.py`: The module that talks to the Telegram API to send messages.
* `extractors/`: Individual scripts for scraping different websites (RemoteOK, WeWorkRemotely, etc.)
* `.env`: Hidden file containing the `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

## ⚙️ Setup & Installation

If moving this project to another computer:

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 python-dotenv feedparser
   ```
3. Run the engine manually:
   ```bash
   python engine.py
   ```

## 🕒 Automation

This project is set up to run 100% automatically in the background using **Windows Task Scheduler**.

### How it was set up (PowerShell):
If you ever move this to a new Windows PC, you can automatically register the background task by opening an Administrator PowerShell in this folder and running:

```powershell
$Action = New-ScheduledTaskAction -Execute "$PWD\.venv\Scripts\python.exe" -Argument "$PWD\engine.py" -WorkingDirectory "$PWD"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "JobHunterBot" -Action $Action -Trigger $Trigger -Description "Runs the automated job scraper every hour" -Force
```

### Managing the Task:
Because this runs natively on Windows:
* You do **not** need to keep your terminal or IDE open.
* It will silently wake up in the background every hour, execute `engine.py`, check all 5 job boards, and send any new matches to your Telegram.
* To stop or delete the automation, open **Task Scheduler** in Windows, look for `JobHunterBot` in the Task Scheduler Library, and right-click -> Disable/Delete.
