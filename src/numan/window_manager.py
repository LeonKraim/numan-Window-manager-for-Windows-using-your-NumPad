import threading
import ctypes
import ctypes.wintypes
import logging

import win32gui
import win32con

logger = logging.getLogger(__name__)

FOCUS_RESULT_FOCUSED = "focused"
FOCUS_RESULT_MISSING = "missing"
FOCUS_RESULT_STALE = "stale"
FOCUS_RESULT_ERROR = "error"

# Allow our process to set foreground window freely
ASFW_ANY = -1
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
user32.AllowSetForegroundWindow(ASFW_ANY)
user32.AttachThreadInput.argtypes = (
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.BOOL,
)
user32.AttachThreadInput.restype = ctypes.wintypes.BOOL
user32.BringWindowToTop.argtypes = (ctypes.wintypes.HWND,)
user32.BringWindowToTop.restype = ctypes.wintypes.BOOL
user32.SetForegroundWindow.argtypes = (ctypes.wintypes.HWND,)
user32.SetForegroundWindow.restype = ctypes.wintypes.BOOL
user32.ShowWindow.argtypes = (ctypes.wintypes.HWND, ctypes.c_int)
user32.ShowWindow.restype = ctypes.wintypes.BOOL


class WindowManager:
    def __init__(self):
        self.slots: dict[int, int] = {}  # slot (1-9) -> hwnd
        self._lock = threading.Lock()
        self._watcher_stop = threading.Event()
        self._on_change = None  # callback for slot changes

    def set_on_change(self, callback):
        self._on_change = callback

    def _notify_change(self):
        if self._on_change:
            try:
                self._on_change()
            except Exception:
                pass

    def _get_window_thread_id(self, hwnd: int):
        process_id = ctypes.wintypes.DWORD()
        return user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))

    def _get_window_title(self, hwnd: int):
        if not hwnd:
            return ""
        try:
            return win32gui.GetWindowText(hwnd)
        except Exception:
            return ""

    def assign(self, slot: int):
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd or not win32gui.IsWindow(hwnd):
            return None
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return None
        with self._lock:
            self.slots[slot] = hwnd
        logger.info("Slot %d assigned: hwnd=%d title=%s", slot, hwnd, title)
        self._notify_change()
        return (hwnd, title)

    def focus(self, slot: int):
        with self._lock:
            hwnd = self.slots.get(slot)
        if hwnd is None:
            logger.info("Slot %d has no assigned window", slot)
            return FOCUS_RESULT_MISSING
        if not win32gui.IsWindow(hwnd):
            with self._lock:
                self.slots.pop(slot, None)
            logger.info("Slot %d contained a stale window and was cleared: hwnd=%d", slot, hwnd)
            self._notify_change()
            return FOCUS_RESULT_STALE

        foreground_before = win32gui.GetForegroundWindow()
        if foreground_before == hwnd:
            logger.info("Slot %d target is already foreground: hwnd=%d", slot, hwnd)
            return FOCUS_RESULT_FOCUSED

        target_title = self._get_window_title(hwnd)
        foreground_title = self._get_window_title(foreground_before)
        current_tid = kernel32.GetCurrentThreadId()
        target_tid = self._get_window_thread_id(hwnd)
        foreground_tid = self._get_window_thread_id(foreground_before) if foreground_before else 0
        attached_tids = []

        try:
            if win32gui.IsIconic(hwnd):
                user32.ShowWindow(hwnd, win32con.SW_RESTORE)
            else:
                user32.ShowWindow(hwnd, win32con.SW_SHOW)

            for thread_id in (foreground_tid, target_tid):
                if thread_id and thread_id != current_tid and thread_id not in attached_tids:
                    if user32.AttachThreadInput(current_tid, thread_id, True):
                        attached_tids.append(thread_id)
                    else:
                        logger.debug(
                            "AttachThreadInput failed: current_tid=%d other_tid=%d last_error=%d",
                            current_tid,
                            thread_id,
                            ctypes.GetLastError(),
                        )

            bring_result = bool(user32.BringWindowToTop(hwnd))
            foreground_result = bool(user32.SetForegroundWindow(hwnd))
            foreground_after = win32gui.GetForegroundWindow()

            if foreground_after != hwnd:
                logger.warning(
                    "Foreground request did not take effect for slot %d: target_hwnd=%d target_title=%s foreground_before=%d foreground_before_title=%s foreground_after=%d foreground_after_title=%s bring_to_top=%s set_foreground=%s",
                    slot,
                    hwnd,
                    target_title,
                    foreground_before,
                    foreground_title,
                    foreground_after,
                    self._get_window_title(foreground_after),
                    bring_result,
                    foreground_result,
                )
                return FOCUS_RESULT_ERROR

            logger.info(
                "Focused slot %d: hwnd=%d bring_to_top=%s set_foreground=%s",
                slot,
                hwnd,
                bring_result,
                foreground_result,
            )
            return FOCUS_RESULT_FOCUSED
        except Exception as e:
            logger.warning("Failed to focus slot %d and preserved existing assignment: %s", slot, e)
            return FOCUS_RESULT_ERROR
        finally:
            for thread_id in reversed(attached_tids):
                user32.AttachThreadInput(current_tid, thread_id, False)

    def get_slot_info(self):
        with self._lock:
            result = {}
            for slot, hwnd in list(self.slots.items()):
                if win32gui.IsWindow(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    result[slot] = title if title else f"(hwnd {hwnd})"
                else:
                    del self.slots[slot]
            return result

    def cleanup_dead(self):
        with self._lock:
            dead = [s for s, h in self.slots.items() if not win32gui.IsWindow(h)]
            for s in dead:
                del self.slots[s]
        if dead:
            logger.info("Cleaned up dead slots: %s", dead)
            self._notify_change()

    def clear_all_slots(self):
        with self._lock:
            cleared = len(self.slots)
            self.slots.clear()
        if cleared > 0:
            logger.info("Cleared all %d slots", cleared)
            self._notify_change()

    def start_watcher(self):
        self._watcher_stop.clear()
        t = threading.Thread(target=self._watcher_loop, daemon=True, name="wm-watcher")
        t.start()
        return t

    def stop_watcher(self):
        self._watcher_stop.set()

    def _watcher_loop(self):
        while not self._watcher_stop.wait(timeout=2.0):
            self.cleanup_dead()
