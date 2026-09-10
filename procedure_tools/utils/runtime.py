import logging
import select
import sys
import threading
import time

from procedure_tools.utils.handlers import EX_OK
from procedure_tools.utils.style import (
    STYLE_DIM,
    fore,
    fore_error,
    fore_info,
    fore_success,
    fore_warning,
)

try:
    import termios
    import tty
except ImportError:  # pragma: no cover - non-POSIX
    termios = None
    tty = None

_controller = None
_PAUSE_HINT = "Press P to pause and show summary, S to show summary"
_thread_data_dir = threading.local()
_QUIET_SETTLE_SECONDS = 0.05


def get_controller():
    return _controller


def set_controller(controller):
    global _controller
    _controller = controller


def status_from_code(code):
    if code is None:
        return "aborted"
    if code == EX_OK:
        return "success"
    return "failed"


def status_label(status, activity=None):
    if status == "success":
        return fore_success("success")
    if status == "failed":
        return fore_error("failed")
    if status == "aborted":
        return fore_warning("aborted")
    if status == "running":
        label = fore_info("running")
        if activity:
            label = f"{label} ({activity})"
        return label
    return fore(str(status), STYLE_DIM) if STYLE_DIM else status


def log_summary(rows):
    rows = list(rows)
    if not rows:
        return
    width = max(len(str(data_dir)) for data_dir, *_ in rows)
    lines = ["Summary"]
    errors = []
    for row in rows:
        data_dir = row[0]
        status = row[1]
        activity = row[2] if len(row) > 2 else None
        error = row[3] if len(row) > 3 else None
        lines.append(f" - {data_dir:<{width}}\t{status_label(status, activity)}")
        if status == "failed" and error:
            errors.append((data_dir, error))
    logging.info("\n".join(lines) + "\n")
    if errors:
        error_lines = ["Errors"]
        for data_dir, error in errors:
            error_text = str(error).strip().splitlines() or [str(error).strip()]
            error_lines.append(f" - {data_dir}")
            for error_line in error_text:
                error_lines.append(f"   {fore_error(error_line)}")
        logging.info("\n".join(error_lines) + "\n")
    for handler in logging.root.handlers:
        handler.flush()


def log_results_summary(results):
    rows = []
    for data_dir, code, error in results:
        status = status_from_code(code)
        rows.append((data_dir, status, None, error if status == "failed" else None))
    log_summary(rows)


class RunController:
    def __init__(self, data_dirs):
        self._lock = threading.Lock()
        self._stdin_lock = threading.RLock()
        self._resume = threading.Event()
        self._resume.set()
        self._quiet = threading.Event()
        self._quiet.set()
        self._stop = threading.Event()
        self._waiting = 0
        self._statuses = {data_dir: "pending" for data_dir in data_dirs}
        self._results = {data_dir: (None, None) for data_dir in data_dirs}
        self._activity = {data_dir: None for data_dir in data_dirs}
        self._data_dirs = list(data_dirs)
        self._listener = None
        self._fd = None
        self._old_termios = None
        self._cbreak = False
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    def current_data_dir(self):
        return getattr(_thread_data_dir, "value", None)

    def start(self):
        if termios is None or tty is None or not sys.stdin.isatty():
            return
        try:
            self._fd = sys.stdin.fileno()
            self._old_termios = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
            self._cbreak = True
        except (termios.error, ValueError, OSError):
            self._fd = None
            self._old_termios = None
            return
        self._enabled = True
        self._listener = threading.Thread(target=self._listen_loop, name="pause-listener", daemon=True)
        self._listener.start()
        logging.info(f"{_PAUSE_HINT}\n")

    def stop(self):
        self._stop.set()
        self._resume.set()
        self._quiet.set()
        if self._listener and self._listener.is_alive() and threading.current_thread() is not self._listener:
            self._listener.join(timeout=1)
        self._restore_terminal()
        self._enabled = False
        if getattr(_thread_data_dir, "value", None) is not None:
            _thread_data_dir.value = None

    def mark_started(self, data_dir):
        _thread_data_dir.value = data_dir
        with self._lock:
            self._statuses[data_dir] = "running"
            self._activity[data_dir] = None
            if not self._resume.is_set():
                self._maybe_signal_quiet_locked()

    def mark_finished(self, data_dir, code, error=None):
        if getattr(_thread_data_dir, "value", None) == data_dir:
            _thread_data_dir.value = None
        with self._lock:
            self._statuses[data_dir] = status_from_code(code)
            self._results[data_dir] = (code, error)
            self._activity[data_dir] = None
            if not self._resume.is_set():
                self._maybe_signal_quiet_locked()

    def set_activity(self, data_dir, activity):
        data_dir = data_dir or self.current_data_dir()
        if not data_dir:
            return
        with self._lock:
            if self._statuses.get(data_dir) == "running":
                self._activity[data_dir] = activity

    def check_pause(self):
        with self._lock:
            if self._resume.is_set():
                return
            self._waiting += 1
            self._maybe_signal_quiet_locked()
        try:
            self._resume.wait()
        finally:
            with self._lock:
                self._waiting -= 1

    def wait_for_enter(self, prompt="Press Enter key to continue..."):
        with self._stdin_lock:
            was_cbreak = self._cbreak
            if was_cbreak:
                self._restore_terminal()
            try:
                input(prompt)
            finally:
                if was_cbreak and not self._stop.is_set():
                    self._enable_cbreak()

    def pause_aware_sleep(self, seconds):
        end = time.monotonic() + max(0, seconds)
        while True:
            self.check_pause()
            remaining = end - time.monotonic()
            if remaining <= 0:
                return
            time.sleep(min(0.5, remaining))

    def log_summary(self):
        with self._lock:
            rows = []
            for data_dir in self._data_dirs:
                status = self._statuses.get(data_dir, "pending")
                activity = self._activity.get(data_dir)
                _, error = self._results.get(data_dir, (None, None))
                rows.append((data_dir, status, activity, error if status == "failed" else None))
        log_summary(rows)

    def _running_count_locked(self):
        return sum(1 for status in self._statuses.values() if status == "running")

    def _maybe_signal_quiet_locked(self):
        running = self._running_count_locked()
        if running == 0 or self._waiting >= running:
            self._quiet.set()

    def _listen_loop(self):
        while not self._stop.is_set():
            if not self._resume.is_set():
                time.sleep(0.1)
                continue
            if not self._stdin_lock.acquire(blocking=False):
                time.sleep(0.1)
                continue
            try:
                if self._stop.is_set() or not self._cbreak:
                    continue
                ready, _, _ = select.select([sys.stdin], [], [], 0.2)
                if not ready:
                    continue
                char = sys.stdin.read(1)
                if not char:
                    continue
                key = char.lower()
                if key == "p":
                    self._pause_from_listener()
                elif key == "s":
                    self.log_summary()
            except (ValueError, OSError, termios.error if termios else OSError):
                break
            finally:
                self._stdin_lock.release()

    def _pause_from_listener(self):
        if not self._resume.is_set():
            return
        with self._lock:
            self._quiet.clear()
            self._resume.clear()
            self._maybe_signal_quiet_locked()
        logging.info("Pausing...\n")
        while not self._quiet.wait(timeout=0.2):
            if self._stop.is_set():
                self._resume.set()
                return
        for handler in logging.root.handlers:
            handler.flush()
        time.sleep(_QUIET_SETTLE_SECONDS)
        logging.info("Paused.\n")
        self.log_summary()
        was_cbreak = self._cbreak
        if was_cbreak:
            self._restore_terminal()
        try:
            input("Press Enter key to continue...")
            print()
        except EOFError:
            print()
        finally:
            if was_cbreak and not self._stop.is_set():
                self._enable_cbreak()
            self._resume.set()
            logging.info("Resumed.\n")

    def _enable_cbreak(self):
        if termios is None or tty is None or self._fd is None:
            return
        try:
            if self._old_termios is None:
                self._old_termios = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
            self._cbreak = True
        except (termios.error, ValueError, OSError):
            self._cbreak = False

    def _restore_terminal(self):
        if termios is None or self._fd is None or self._old_termios is None:
            self._cbreak = False
            return
        try:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_termios)
        except (termios.error, ValueError, OSError):
            pass
        self._cbreak = False
