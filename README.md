# 🤖 Personal AI Employee - Bronze Tier

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

This repository contains the **Bronze Tier** implementation of a Personal AI Employee - an autonomous AI agent that manages personal and business affairs 24/7 using Claude Code and Obsidian.

---

## 📋 Bronze Tier Deliverables

✅ **Completed:**

- [x] Obsidian vault with `Dashboard.md`, `Company_Handbook.md`, and `Business_Goals.md`
- [x] File System Watcher script (monitors drop folder for new files)
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`, `/Pending_Approval`, `/Approved`
- [x] Claude Code ready to read/write to vault
- [x] Documentation and setup instructions

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT                           │
│  Dashboard.md | Company_Handbook.md | Business_Goals.md     │
│  /Inbox | /Needs_Action | /Done | /Pending_Approval        │
└─────────────────────────────────────────────────────────────┘
                            ↑ ↓ reads/writes
┌─────────────────────────────────────────────────────────────┐
│              CLAUDE CODE (Reasoning Engine)                 │
└─────────────────────────────────────────────────────────────┘
                            ↑ triggers
┌─────────────────────────────────────────────────────────────┐
│           FILE SYSTEM WATCHER (Python)                      │
│           Monitors drop folder for new files                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Obsidian](https://obsidian.md/download) | Latest | Knowledge base |
| [Claude Code](https://claude.com/product/claude-code) | Latest | AI reasoning engine |
| [Git](https://git-scm.com/downloads) | Latest | Version control |

### Step 1: Install Python Dependencies

```bash
cd watchers
pip install -r requirements.txt
```

### Step 2: Open Obsidian Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select the `AI_Employee_Vault` folder in this repository

### Step 3: Create a Drop Folder

Create a folder anywhere on your system where you'll drop files for processing:

```bash
# Example on Windows
mkdir "C:\Users\YourName\AI_Drop"

# Example on Mac/Linux
mkdir ~/AI_Drop
```

### Step 4: Start the File System Watcher

```bash
cd watchers
python filesystem_watcher.py "../AI_Employee_Vault" "C:/Users/YourName/AI_Drop"
```

Replace the paths with your actual vault path and drop folder path.

### Step 5: Test the System

1. Drop any file into your drop folder
2. Watch the terminal for detection messages
3. Check `AI_Employee_Vault/Needs_Action/` for a new `.md` action file
4. Open Obsidian to see the action item

### Step 6: Use Claude Code to Process Actions

```bash
cd AI_Employee_Vault
claude
```

Then prompt Claude Code:

```
Check the /Needs_Action folder and process any pending items.
Create a plan in /Plans folder and move completed items to /Done.
Update the Dashboard.md with current status.
```

---

## 📁 Vault Structure

```
AI_Employee_Vault/
├── Dashboard.md              # Main dashboard with status overview
├── Company_Handbook.md       # Rules of engagement for AI
├── Business_Goals.md         # Business objectives and metrics
├── Inbox/                    # General incoming items
├── Needs_Action/             # Items requiring action (Watcher output)
├── Pending_Approval/         # Items awaiting human approval
├── Approved/                 # Approved items ready for action
├── Rejected/                 # Rejected items
├── Plans/                    # Action plans created by Claude
├── Done/                     # Completed items archive
├── Accounting/               # Financial records
├── Briefings/                # CEO briefing reports
├── Logs/                     # System logs
├── Invoices/                 # Generated invoices
├── Updates/                  # Status updates
└── Dropped_Files/            # Copies of files from drop folder
```

---

## 🔧 Configuration

### Watcher Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `check_interval` | 5 seconds | How often to check for new files |
| `vault_path` | Required | Path to Obsidian vault root |
| `drop_folder_path` | Required | Path to folder to monitor |

### Customizing the Watcher

Edit `filesystem_watcher.py` to:

- Change the check interval
- Add file type filters
- Modify action file templates
- Add custom metadata fields

---

## 📖 Usage Patterns

### Pattern 1: File Drop Processing

1. Drop a file (document, image, etc.) into your drop folder
2. Watcher creates action file in `/Needs_Action`
3. Claude Code reads and categorizes the file
4. Claude creates a plan in `/Plans`
5. You review and approve if needed
6. Claude processes and moves to `/Done`

### Pattern 2: Daily Review

```bash
cd AI_Employee_Vault
claude
```

Prompt:
```
Review the Dashboard.md and update it with:
1. Count of items in each folder
2. Summary of completed tasks
3. Any pending approvals
4. System status
```

### Pattern 3: Weekly Business Review

Prompt:
```
Read Business_Goals.md and generate a weekly briefing in /Briefings.
Include:
- Revenue tracking
- Task completion rate
- Bottlenecks identified
- Recommendations for next week
```

---

## 🔒 Security Notes

### ⚠️ Important Security Practices

1. **Never commit credentials** - Add `.env` files to `.gitignore`
2. **Use environment variables** for API keys when adding Gmail/WhatsApp watchers
3. **Review before approving** - Always check `/Pending_Approval` items
4. **Audit logs regularly** - Check `/Logs` for unusual activity

### Recommended `.gitignore`

```gitignore
# Secrets and credentials
.env
*.key
*.pem
credentials.json

# Logs (optional - may contain sensitive data)
Logs/*.log

# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
```

---

## 🧪 Testing

### Test the File System Watcher

```bash
# Start the watcher
python filesystem_watcher.py "../AI_Employee_Vault" "./test_drop"

# In another terminal, create a test file
echo "Test content" > ./test_drop/test_file.txt

# Check for action file creation
ls ../AI_Employee_Vault/Needs_Action/
```

You should see a new `FILE_test_file_*.md` file created.

---

## 📈 Next Steps (Silver Tier)

To upgrade to Silver Tier, add:

1. **Gmail Watcher** - Monitor Gmail for important emails
2. **WhatsApp Watcher** - Monitor WhatsApp for urgent messages
3. **MCP Server** - Enable sending emails and external actions
4. **Approval Workflow** - Human-in-the-loop for sensitive actions
5. **Scheduled Tasks** - Cron jobs for daily briefings

---

## 🐛 Troubleshooting

### Watcher doesn't detect files

- Ensure the drop folder path is correct
- Check file permissions on the drop folder
- Verify watchdog is installed: `pip show watchdog`

### Action files not created

- Check the watcher logs in `/Logs`
- Ensure the vault path is correct
- Verify write permissions on the vault folder

### Claude Code can't read vault

- Run `claude` from within the vault directory
- Or use: `claude --cwd /path/to/vault`

---

## 📚 Resources

- [Full Hackathon Guide](./Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Claude Code Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Obsidian Help](https://help.obsidian.md/)
- [Watchdog Documentation](https://pypi.org/project/watchdog/)

---

## 🤝 Weekly Research Meetings

- **When:** Wednesdays at 10:00 PM
- **Zoom:** [Join Meeting](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube:** [@panaversity](https://www.youtube.com/@panaversity)

---

## 📄 License

This project is part of the Personal AI Employee Hackathon. Feel free to use, modify, and share your implementations.

---

*Built with ❤️ for the Personal AI Employee Hackathon 2026*
