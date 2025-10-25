# GitScheduler - Quick Start Guide

## Installation (3 Easy Steps)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test the Tool
```bash
python gitscheduler.py --help
```

### Step 3: Make it Globally Accessible (Optional)

**On Linux/macOS:**
```bash
# Option A: Create an alias
echo "alias gitscheduler='python3 $(pwd)/gitscheduler.py'" >> ~/.bashrc
source ~/.bashrc

# Option B: Install as a package
pip install -e .
```

**On Windows:**
```bash
# Install as a package
pip install -e .
```

---

## First Time Usage

### 1. Navigate to your git repository
```bash
cd /path/to/your/project
```

### 2. Schedule a commit (5 minutes from now for testing)
```bash
python gitscheduler.py schedule -m "Test scheduled commit" -t 5m
```

### 3. Start the daemon
```bash
python gitscheduler.py daemon
```

### 4. Watch it work!
The daemon will wait 5 minutes and then automatically commit and push your changes.

---

## Common Commands Cheatsheet

```bash
# Schedule for 30 minutes from now
python gitscheduler.py schedule -m "Your message" -t 30m

# Schedule for 2 hours from now
python gitscheduler.py schedule -m "Your message" -t 2h

# Schedule for specific time
python gitscheduler.py schedule -m "Your message" -t "2025-10-25 15:30"

# Schedule for different branch
python gitscheduler.py schedule -m "Your message" -t 30m -b develop

# List all schedules
python gitscheduler.py list

# Cancel a schedule
python gitscheduler.py cancel 1

# Start the daemon (required for execution)
python gitscheduler.py daemon

# Run daemon in background (Linux/macOS)
nohup python gitscheduler.py daemon > /dev/null 2>&1 &

# View logs
python gitscheduler.py logs

# Clear completed schedules
python gitscheduler.py clear
```

---

## Real-World Example

**Scenario:** You need to leave for an emergency in 5 minutes, but want your code pushed in 30 minutes.

```bash
# 1. Navigate to your project
cd ~/my-project

# 2. Schedule the push
python gitscheduler.py schedule -m "Emergency commit - bug fix" -t 30m

# 3. Start daemon in background
nohup python gitscheduler.py daemon &

# 4. You can now leave! The commit will happen automatically in 30 minutes
```

---

## Troubleshooting

**Problem:** Command not found
**Solution:** Use `python gitscheduler.py` instead of just `gitscheduler`

**Problem:** Permission denied
**Solution:** Run `chmod +x gitscheduler.py`

**Problem:** Module not found errors
**Solution:** Run `pip install -r requirements.txt`

**Problem:** Git authentication errors
**Solution:** Set up SSH keys or credential helper:
```bash
# For SSH (recommended)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-add ~/.ssh/id_rsa

# For HTTPS
git config --global credential.helper store
```

---

## Tips

1. **Always run the daemon** - Schedules won't execute without it
2. **Keep computer running** - Your computer must be on at the scheduled time
3. **Test with short times first** - Use `5m` to test before longer schedules
4. **Check logs for errors** - `python gitscheduler.py logs`
5. **One daemon per machine** - You only need one daemon running for all repositories

---

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Set up the daemon to auto-start on system boot
- Configure notifications (future feature)
- Share feedback and contribute!

---

**Need help?** Open an issue on GitHub!
