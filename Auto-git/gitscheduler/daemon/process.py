import os, sys, subprocess, time
from pathlib import Path
from config.paths import PID_FILE, LOG_FILE

def write_pid():
    PID_FILE.write_text(str(os.getpid()))

def is_running():
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text())
        
        if sys.platform == "win32":
            # On Windows, use ctypes to check if process exists
            import ctypes
            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
            return False
        else:
            # On Unix, signal 0 checks if process exists
            os.kill(pid, 0)
            return True
    except:
        return False

def start_daemon_background():
    """Start the daemon as a background subprocess."""
    if is_running():
        return False  # Already running
    
    # Get the path to main.py and the project directory
    project_dir = Path(__file__).parent.parent
    main_py = project_dir / "main.py"
    
    if sys.platform == "win32":
        # On Windows, use DETACHED_PROCESS to run independently
        DETACHED_PROCESS = 0x00000008
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen(
            [sys.executable, str(main_py), "daemon"],
            cwd=str(project_dir),
            creationflags=DETACHED_PROCESS | CREATE_NO_WINDOW,
            close_fds=True,
        )
    else:
        # Unix: use nohup-like behavior
        subprocess.Popen(
            [sys.executable, str(main_py), "daemon"],
            cwd=str(project_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    
    # Wait a moment for daemon to start and write PID
    time.sleep(1)
    
    return True
