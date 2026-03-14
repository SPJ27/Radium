import os
import sys
import time
import signal
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

APP_MODULE = os.getenv("APP_MODULE", "app:app")  # ← points to app.py
HOST       = os.getenv("HOST",       "127.0.0.1")
PORT       = os.getenv("PORT",       "8000")
WORKERS    = os.getenv("WORKERS",    "4")
THREADS    = os.getenv("THREADS",    "4")
WATCH_DIR  = os.getenv("WATCH_DIR",  ".")

IS_WINDOWS = sys.platform == "win32"


def get_mtime(watch_dir):
    mtimes = []
    for root, _, files in os.walk(watch_dir):
        for f in files:
            if f.endswith(".py"):
                try:
                    mtimes.append(os.path.getmtime(os.path.join(root, f)))
                except OSError:
                    pass
    return max(mtimes, default=0)


def kill_proc(proc):
    if proc is None or proc.poll() is not None:
        return
    if IS_WINDOWS:
        proc.terminate()
    else:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def make_proc(cmd):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([os.getcwd(), env.get("PYTHONPATH", "")])
    kwargs = {"env": env}
    if not IS_WINDOWS:
        kwargs["start_new_session"] = True
    return subprocess.Popen(cmd, **kwargs)


def dev_server():
    print(f"[dev] Watching '{WATCH_DIR}' for changes...")
    print(f"[dev] Running: {APP_MODULE} on http://{HOST}:{PORT}")
    print("[dev] Press Ctrl+C to stop.\n")

    cmd        = [sys.executable, "-m", "waitress", "--host", HOST, "--port", PORT, "--threads", THREADS, APP_MODULE]
    last_mtime = get_mtime(WATCH_DIR)
    proc       = make_proc(cmd)

    try:
        while True:
            time.sleep(1)
            new_mtime = get_mtime(WATCH_DIR)
            if new_mtime != last_mtime:
                print("[dev] Change detected — reloading...")
                kill_proc(proc)
                proc       = make_proc(cmd)
                last_mtime = new_mtime
                print(f"[dev] Reloaded at http://{HOST}:{PORT}")
    except KeyboardInterrupt:
        print("\n[dev] Stopping...")
        kill_proc(proc)


def prod_server():
    print(f"[prod] Starting production server: {APP_MODULE} on {HOST}:{PORT}")

    if IS_WINDOWS:
        print("[prod] Platform: Windows — using Waitress")
        cmd = [
            sys.executable, "-m", "waitress",
            "--host",    HOST,
            "--port",    PORT,
            "--threads", THREADS,
            APP_MODULE,
        ]
    else:
        print("[prod] Platform: Linux/macOS — using Gunicorn")
        cmd = [
            "gunicorn",
            "--bind",    f"{HOST}:{PORT}",
            "--workers", WORKERS,
            "--threads", THREADS,
            "--access-logfile", "-",
            "--error-logfile",  "-",
            APP_MODULE,
        ]

    proc = make_proc(cmd)

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[prod] Shutting down...")
        kill_proc(proc)


def main():
    global HOST, PORT, WORKERS, THREADS, APP_MODULE, WATCH_DIR

    parser = argparse.ArgumentParser(
        description="App server runner",
        epilog="Defaults work out of the box — no .env required for dev.",
    )
    parser.add_argument("--mode",      choices=["dev", "prod"], default="dev",
                        help="Run mode (default: dev)")
    parser.add_argument("--host",      default=HOST,       help=f"Host (default: {HOST})")
    parser.add_argument("--port",      default=PORT,       help=f"Port (default: {PORT})")
    parser.add_argument("--workers",   default=WORKERS,    help=f"Gunicorn workers (default: {WORKERS})")
    parser.add_argument("--threads",   default=THREADS,    help=f"Threads (default: {THREADS})")
    parser.add_argument("--app",       default=APP_MODULE, help=f"WSGI module (default: {APP_MODULE})")
    parser.add_argument("--watch-dir", default=WATCH_DIR,  help=f"Dir to watch in dev (default: {WATCH_DIR})")
    args = parser.parse_args()

    HOST       = args.host
    PORT       = args.port
    WORKERS    = args.workers
    THREADS    = args.threads
    APP_MODULE = args.app
    WATCH_DIR  = args.watch_dir

    if args.mode == "prod":
        prod_server()
    else:
        dev_server()


if __name__ == "__main__":
    main()