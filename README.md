
# 🛡️ ColdBOT — Discord Moderation Bot (Test Version)

ColdBOT is a simple yet functional Discord moderation bot developed for testing and learning purposes. It features essential moderation tools such as user kicking, banning, unbanning, and viewing the ban list. All moderation actions are logged to a file directly on your Desktop.

**Author:** Jibreal Id-deen  
**Date:** May 23, 2025

---

## 📌 Description

ColdBOT is a test-focused **Discord moderation bot** built with Python and `discord.py`. It includes essential moderation features like kicking, banning, unbanning, and viewing banned users, with confirmation prompts and local logging.

> ✅ This project is designed for **testing and learning** purposes.

---

## 🚀 Features

- 🤖 Basic message responses to `$hello` and `$who`
- 👢 `!kick` command with reaction-based confirmation
- 🔨 `!ban` command with confirmation and reason support
- 🛑 `!unban` command by **username only** (no discriminator required)
- 📜 `!banlist` command to list all banned users and reasons
- 🗂️ Logs all bans/unbans to `ban_unban_log.txt` on your **Desktop**
- 🔐 Only usable by moderators with the proper permissions

---

## 📁 Log File

All ban and unban actions are logged to a file on your desktop:

**Location:**
```
C:\Users\YourUsername\Desktop\ban_unban_log.txt
```

**Example log entry:**
```
[2025-05-23 16:40:01] BAN: troublemaker#0001 (ID: 1234567890) by Cold#1234 | Reason: Spamming  
[2025-05-23 16:44:21] UNBAN: troublemaker#0001 (ID: 1234567890) by Cold#1234 | Reason: No reason provided
```

---

## 🔧 Requirements

- Python 3.8 or newer
- `discord.py` (or compatible fork like `py-cord`)

Install the library:
```bash
pip install -U discord.py
```

---

## 📦 How to Run the Bot

1. Clone or download this repository.
2. Open the `bot.py` file in your text editor.
3. Replace the token placeholder:
```python
bot.run('YOUR_BOT_TOKEN_HERE')
```
4. Save the file and run the bot:
```bash
python bot.py
```

---

## 🔑 How to Create a Discord Bot & Get Your Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**, name it (e.g., `ColdBOT`)
3. Go to the **Bot** tab → Click **"Add Bot"**
4. Under the bot settings, click **"Copy" Token**
   - Paste it into your `bot.run()` line in `bot.py`
5. Scroll down and enable:
   - **Message Content Intent**
   - **Server Members Intent**
6. Click **Save Changes**

---

## 🤝 How to Invite the Bot to Your Server

1. In the Developer Portal, go to **OAuth2 > URL Generator**
2. Select the scope:
   - `bot`
3. Under "Bot Permissions", select:
   - `Read Messages`
   - `Send Messages`
   - `Kick Members`
   - `Ban Members`
4. Copy the generated URL, paste it into your browser
5. Choose a server where you have permissions and click **Authorize**

---

## ✅ Available Commands

| Command        | Description                                               |
|----------------|-----------------------------------------------------------|
| `$hello`       | Replies with "Hello World!"                               |
| `$who`         | Introduces the bot and tags the user                      |
| `!kick @user`  | Kicks a user after confirmation                           |
| `!ban @user`   | Bans a user after confirmation, logs to Desktop           |
| `!unban name`  | Unbans a user by username (no tag required), logs too     |
| `!banlist`     | Shows a list of all banned users with reason and ID       |

---

## ⚠️ Notes

- ❗ **Never share your bot token publicly**
- 🔁 If your token is exposed, regenerate it immediately
- ⚙️ This bot is for **testing**, not hardened for public deployment
- 🔒 Consider adding command cooldowns, error handling, and logging to a database for production use

---

## 📚 License

This project is open for learning and modification.  
Use it freely, break it, improve it.

> Created with ❤️ for Discord bot development practice by **Jibreal Id-deen**
