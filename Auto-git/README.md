# GitScheduler 🕒

**Schedule your git commits and pushes - Never miss a deadline again!**

A simple, user-friendly CLI tool that allows developers to schedule git commits and pushes for later execution. Perfect for when you need to step away but want your code pushed at a specific time.

---

## 🚀 Features

✅ **Simple Scheduling** - Schedule commits using easy time formats (`30m`, `2h`, or specific datetime)  
✅ **Auto Commit & Push** - Automatically commits all changes and pushes to your branch  
✅ **Multiple Schedules** - Queue multiple scheduled tasks  
✅ **Status Tracking** - Monitor pending, completed, and failed schedules  
✅ **Easy Management** - List, cancel, and clear schedules with simple commands  
✅ **Persistent Storage** - Schedules saved locally, survive restarts  
✅ **Detailed Logging** - Track all operations with timestamped logs  
✅ **Cross-Platform** - Works on Windows, macOS, and Linux  

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Git installed on your system
- A GitHub/GitLab/Bitbucket account

### Install Steps

1. **Clone or download the repository**
```bash
git clone https://github.com/yourusername/gitscheduler.git
cd gitscheduler
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Make the script executable** (Linux/macOS)
```bash
chmod +x gitscheduler.py
```

4. **Optional: Add to PATH for global access**

**On Linux/macOS:**
```bash
# Move to a directory in your PATH
sudo cp gitscheduler.py /usr/local/bin/gitscheduler

# Or create an alias in ~/.bashrc or ~/.zshrc
echo "alias gitscheduler='python3 /path/to/gitscheduler.py'" >> ~/.bashrc
source ~/.bashrc
```

**On Windows:**
```bash
# Create a batch file gitscheduler.bat in a directory in your PATH
@echo off
python C:\path\to\gitscheduler.py %*
```

---

## 🎯 Quick Start

### 1. Schedule a commit (30 minutes from now)
```bash
python gitscheduler.py schedule -m "Update documentation" -t 30m
```

### 2. Start the scheduler daemon
```bash
python gitscheduler.py daemon
```

### 3. View all schedules
```bash
python gitscheduler.py list
```

That's it! Your commit will be pushed automatically at the scheduled time.

---

## 📖 Usage Guide

### Schedule a Commit

**Relative time (minutes):**
```bash
python gitscheduler.py schedule -m "Fix bug in login" -t 30m
```

**Relative time (hours):**
```bash
python gitscheduler.py schedule -m "Add new feature" -t 2h
```

**Specific date and time:**
```bash
python gitscheduler.py schedule -m "Release v1.0" -t "2025-10-25 14:30"
```

**With custom branch:**
```bash
python gitscheduler.py schedule -m "Update docs" -t 1h -b develop
```

**For a specific repository:**
```bash
python gitscheduler.py schedule -m "Update config" -t 30m -p /path/to/repo
```

### Run the Scheduler Daemon

The daemon must be running to execute scheduled tasks:

```bash
python gitscheduler.py daemon
```

**Important:** Keep the terminal running or run it in the background!

**Run in background (Linux/macOS):**
```bash
nohup python gitscheduler.py daemon &
```

### List All Schedules

```bash
python gitscheduler.py list
```

Output:
```
================================================================================
Scheduled Commits
================================================================================

ID: 1
  Status: PENDING
  Message: Update documentation
  Branch: main
  Repository: /home/user/my-project
  Scheduled: 2025-10-25T09:45:00

ID: 2
  Status: COMPLETED
  Message: Fix bug in login
  Branch: main
  Repository: /home/user/my-project
  Scheduled: 2025-10-25T08:30:00
```

### Cancel a Schedule

```bash
python gitscheduler.py cancel 1
```

### Clear Completed/Failed Schedules

```bash
python gitscheduler.py clear
```

### View Logs

```bash
python gitscheduler.py logs
```

---

## 🔧 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `schedule` | Schedule a new commit | `gitscheduler schedule -m "message" -t 30m` |
| `list` | List all schedules | `gitscheduler list` |
| `cancel` | Cancel a pending schedule | `gitscheduler cancel 1` |
| `clear` | Remove completed/failed schedules | `gitscheduler clear` |
| `daemon` | Start the scheduler daemon | `gitscheduler daemon` |
| `logs` | View scheduler logs | `gitscheduler logs` |

### Schedule Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--message` | `-m` | Commit message (required) | `-m "Update README"` |
| `--time` | `-t` | Schedule time (required) | `-t 30m` or `-t "2025-10-25 14:30"` |
| `--branch` | `-b` | Branch name (default: main) | `-b develop` |
| `--path` | `-p` | Repository path (default: current) | `-p /path/to/repo` |

---

## 💡 Use Cases

### Emergency Scenario
```bash
# You need to leave urgently but want to push at 3 PM
python gitscheduler.py schedule -m "Critical hotfix" -t "2025-10-25 15:00"
python gitscheduler.py daemon &
# Now you can leave! The push will happen automatically
```

### Scheduled Release
```bash
# Schedule a release for midnight
python gitscheduler.py schedule -m "Release v2.0" -t "2025-10-26 00:00" -b production
```

### Meeting During Work
```bash
# You have a 1-hour meeting, push after it ends
python gitscheduler.py schedule -m "Complete feature X" -t 1h
```

---

## 📂 File Locations

GitScheduler stores its data in your home directory:

- **Config directory:** `~/.gitscheduler/`
- **Schedules:** `~/.gitscheduler/schedules.json`
- **Logs:** `~/.gitscheduler/scheduler.log`

---

## ⚠️ Important Notes

1. **Keep Computer Running:** Your computer must be on and the daemon running for scheduled tasks to execute
2. **Network Connection:** Ensure you have internet connectivity at the scheduled time for pushing
3. **Git Authentication:** Make sure git credentials are configured (SSH keys or credential manager)
4. **Uncommitted Changes:** The tool will commit ALL uncommitted changes in the repository
5. **Time Zone:** All times are in your local system time

---

## 🔒 Security

- All data is stored locally on your machine
- No external servers or cloud services involved
- Uses your existing git credentials
- Schedules are private to your user account

---

## 🐛 Troubleshooting

### "Not a git repository" error
**Solution:** Make sure you're in a git repository or use `-p` to specify the path.

### Authentication errors when pushing
**Solution:** Configure git credentials:
```bash
# For HTTPS
git config --global credential.helper store

# For SSH (recommended)
ssh-add ~/.ssh/id_rsa
```

### Daemon not executing schedules
**Solution:** 
- Check if daemon is still running
- Verify the scheduled time hasn't passed
- Check logs: `python gitscheduler.py logs`

### Permission denied errors
**Solution:** Make the script executable:
```bash
chmod +x gitscheduler.py
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Future Enhancements

- [ ] Desktop GUI application
- [ ] System tray integration
- [ ] Email notifications
- [ ] Recurring schedules
- [ ] Multi-repository support
- [ ] Cloud-based scheduling option
- [ ] Mobile app for monitoring

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

Created with ❤️ by Rupanjan Saha and Subarno Chakraborty

---

## 🙏 Acknowledgments

- Built with [GitPython](https://gitpython.readthedocs.io/)
- Scheduling powered by [APScheduler](https://apscheduler.readthedocs.io/)
- CLI interface using [Click](https://click.palletsprojects.com/)

---

## 📧 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Contact: your.email@example.com

---

**⭐ If you find this tool helpful, please star the repository!**
