import time, signal, sys
from daemon.process import write_pid
from core.scheduler import GitScheduler

def run_daemon():
    gs = GitScheduler()
    write_pid()

    gs.scheduler.start()
    gs.load_jobs()

    def shutdown(*_):
        gs.scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        time.sleep(1)
