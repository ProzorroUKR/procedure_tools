import threading
import time

from procedure_tools.utils.handlers import EX_OK
from procedure_tools.utils.runtime import RunController, get_controller, set_controller


def test_run_controller_summary_states():
    controller = RunController(["one", "two", "three"])
    set_controller(controller)
    try:
        controller.mark_started("one")
        controller.set_activity(None, "tender_create.json")
        assert controller.current_data_dir() == "one"
        controller.mark_finished("two", EX_OK, None)
        controller.mark_finished("three", 1, "failed hard")

        with controller._lock:
            assert controller._statuses["one"] == "running"
            assert controller._activity["one"] == "tender_create.json"
            assert controller._statuses["two"] == "success"
            assert controller._statuses["three"] == "failed"

        controller.mark_finished("one", None, None)
        with controller._lock:
            assert controller._statuses["one"] == "aborted"
            assert controller._activity["one"] is None
        assert controller.current_data_dir() is None
    finally:
        set_controller(None)
        assert get_controller() is None


def test_check_pause_blocks_until_resume():
    controller = RunController(["one"])
    released = threading.Event()

    def worker():
        controller.check_pause()
        released.set()

    controller._resume.clear()
    thread = threading.Thread(target=worker)
    thread.start()
    time.sleep(0.05)
    assert not released.is_set()
    controller._resume.set()
    thread.join(timeout=1)
    assert released.is_set()


def test_pause_waits_until_all_running_workers_are_quiet():
    controller = RunController(["one", "two"])
    controller.mark_started("one")
    controller.mark_started("two")
    quiet_seen = threading.Event()
    workers_ready = threading.Barrier(3)

    def worker():
        workers_ready.wait()
        controller.check_pause()

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()

    def pause_ui():
        workers_ready.wait()
        with controller._lock:
            controller._quiet.clear()
            controller._resume.clear()
            controller._maybe_signal_quiet_locked()
        assert not controller._quiet.is_set()
        assert controller._quiet.wait(timeout=1)
        quiet_seen.set()
        controller._resume.set()

    ui = threading.Thread(target=pause_ui)
    ui.start()
    ui.join(timeout=2)
    for thread in threads:
        thread.join(timeout=1)
    assert quiet_seen.is_set()


def test_pause_is_quiet_immediately_when_nothing_running():
    controller = RunController(["one", "two"])
    controller.mark_finished("one", EX_OK, None)
    with controller._lock:
        controller._quiet.clear()
        controller._resume.clear()
        controller._maybe_signal_quiet_locked()
        assert controller._quiet.is_set()
