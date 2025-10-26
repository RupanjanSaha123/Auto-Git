# Auto-Git(GitScheduler) 🕒

Schedule your git commits and pushes - Never miss a deadline again!

A simple, user-friendly CLI tool that allows developers to schedule git commits and pushes for later execution. Perfect for when you need to step away but want your code pushed at a specific time.

🚀 Features
✅ Simple Scheduling - Schedule commits using easy time formats (30m, 2h, or specific datetime)
✅ Auto Commit & Push - Automatically commits all changes and pushes to your branch
✅ Multiple Schedules - Queue multiple scheduled tasks
✅ Status Tracking - Monitor pending, completed, and failed schedules
✅ Easy Management - List, cancel, and clear schedules with simple commands
✅ Persistent Storage - Schedules saved locally, survive restarts
✅ Detailed Logging - Track all operations with timestamped logs
✅ Cross-Platform - Works on Windows, macOS, and Linux

📦 Installation
Prerequisites
Python 3.7 or higher
Git installed on your system
A GitHub/GitLab/Bitbucket account
Install Steps
Clone or download the repository
git clone https://github.com/yourusername/gitscheduler.git
cd gitscheduler
Install dependencies
pip install -r requirements.txt
Make the script executable (Linux/macOS)
chmod +x gitscheduler.py
Optional: Add to PATH for global access
On Linux/macOS:

# Move to a directory in your PATH
sudo cp gitscheduler.py /usr/local/bin/gitscheduler

# Or create an alias in ~/.bashrc or ~/.zshrc
echo "alias gitscheduler='python3 /path/to/gitscheduler.py'" >> ~/.bashrc
source ~/.bashrc
On Windows:

# Create a batch file gitscheduler.bat in a directory in your PATH
@echo off
python C:\path\to\gitscheduler.py %*
🎯 Quick Start
1. Schedule a commit (30 minutes from now)
python gitscheduler.py schedule -m "Update documentation" -t 30m
2. Start the scheduler daemon
python gitscheduler.py daemon
3. View all schedules
python gitscheduler.py list
That's it! Your commit will be pushed automatically at the scheduled time.

📖 Usage Guide
Schedule a Commit
Relative time (minutes):

python gitscheduler.py schedule -m "Fix bug in login" -t 30m
Relative time (hours):

python gitscheduler.py schedule -m "Add new feature" -t 2h
Specific date and time:

python gitscheduler.py schedule -m "Release v1.0" -t "2025-10-25 14:30"
With custom branch:

python gitscheduler.py schedule -m "Update docs" -t 1h -b develop
For a specific repository:

python gitscheduler.py schedule -m "Update config" -t 30m -p /path/to/repo
Run the Scheduler Daemon
The daemon must be running to execute scheduled tasks:

python gitscheduler.py daemon
Important: Keep the terminal running or run it in the background!

Run in background (Linux/macOS):

nohup python gitscheduler.py daemon &
List All Schedules
python gitscheduler.py list
Output:

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
Cancel a Schedule
python gitscheduler.py cancel 1
Clear Completed/Failed Schedules
python gitscheduler.py clear
View Logs
python gitscheduler.py logs
🔧 Commands Reference
Command	Description	Example
schedule	Schedule a new commit	gitscheduler schedule -m "message" -t 30m
list	List all schedules	gitscheduler list
cancel	Cancel a pending schedule	gitscheduler cancel 1
clear	Remove completed/failed schedules	gitscheduler clear
daemon	Start the scheduler daemon	gitscheduler daemon
logs	View scheduler logs	gitscheduler logs
Schedule Options
Option	Short	Description	Example
--message	-m	Commit message (required)	-m "Update README"
--time	-t	Schedule time (required)	-t 30m or -t "2025-10-25 14:30"
--branch	-b	Branch name (default: main)	-b develop
--path	-p	Repository path (default: current)	-p /path/to/repo
💡 Use Cases
Emergency Scenario
# You need to leave urgently but want to push at 3 PM
python gitscheduler.py schedule -m "Critical hotfix" -t "2025-10-25 15:00"
python gitscheduler.py daemon &
# Now you can leave! The push will happen automatically
Scheduled Release
# Schedule a release for midnight
python gitscheduler.py schedule -m "Release v2.0" -t "2025-10-26 00:00" -b production
Meeting During Work
# You have a 1-hour meeting, push after it ends
python gitscheduler.py schedule -m "Complete feature X" -t 1h
📂 File Locations
GitScheduler stores its data in your home directory:

Config directory: ~/.gitscheduler/
Schedules: ~/.gitscheduler/schedules.json
Logs: ~/.gitscheduler/scheduler.log
⚠️ Important Notes
Keep Computer Running: Your computer must be on and the daemon running for scheduled tasks to execute
Network Connection: Ensure you have internet connectivity at the scheduled time for pushing
Git Authentication: Make sure git credentials are configured (SSH keys or credential manager)
Uncommitted Changes: The tool will commit ALL uncommitted changes in the repository
Time Zone: All times are in your local system time
🔒 Security
All data is stored locally on your machine
No external servers or cloud services involved
Uses your existing git credentials
Schedules are private to your user account
🐛 Troubleshooting
"Not a git repository" error
Solution: Make sure you're in a git repository or use -p to specify the path.

Authentication errors when pushing
Solution: Configure git credentials:

# For HTTPS
git config --global credential.helper store

# For SSH (recommended)
ssh-add ~/.ssh/id_rsa
Daemon not executing schedules
Solution:

Check if daemon is still running
Verify the scheduled time hasn't passed
Check logs: python gitscheduler.py logs
Permission denied errors
Solution: Make the script executable:

chmod +x gitscheduler.py
🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
📝 Future Enhancements
 Desktop GUI application
 System tray integration
 Email notifications
 Recurring schedules
 Multi-repository support
 Cloud-based scheduling option
 Mobile app for monitoring
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Created with ❤️ by Rupanjan Saha.

🙏 Acknowledgments
Built with GitPython
Scheduling powered by APScheduler
CLI interface using Click
📧 Support
If you encounter any issues or have questions:

Open an issue on GitHub
Contact: rupanjan1203@gmail.com

⭐ If you find this tool helpful, please star the reposito
