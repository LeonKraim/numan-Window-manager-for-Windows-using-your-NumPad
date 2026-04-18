import ctypes
import ctypes.wintypes
import threading
import logging

logger = logging.getLogger(__name__)

LRESULT = ctypes.c_ssize_t
ULONG_PTR = ctypes.c_size_t
HHOOK = ctypes.c_void_p

# Windows constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
VK_NUMLOCK = 0x90

# Numpad VK codes when NumLock is ON (produce digits)
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69

# Numpad VK codes when NumLock is OFF (produce navigation)
VK_END = 0x23
VK_DOWN = 0x28
VK_NEXT = 0x22  # Page Down
VK_LEFT = 0x25
VK_CLEAR = 0x0C
VK_RIGHT = 0x27
VK_HOME = 0x24
VK_UP = 0x26
VK_PRIOR = 0x21  # Page Up

# Map VK codes to slot numbers (1-9)
NUMPAD_ON_MAP = {
    VK_NUMPAD1: 1, VK_NUMPAD2: 2, VK_NUMPAD3: 3,
    VK_NUMPAD4: 4, VK_NUMPAD5: 5, VK_NUMPAD6: 6,
    VK_NUMPAD7: 7, VK_NUMPAD8: 8, VK_NUMPAD9: 9,
}

# Numpad navigation keys mapped to slots (when NumLock is OFF)
# These share VK codes with real arrow/nav keys — we distinguish by scan code.
# Numpad scan codes (standardized):
NUMPAD_SCANCODES = {
    0x4F: 1,  # Numpad 1 / End
    0x50: 2,  # Numpad 2 / Down
    0x51: 3,  # Numpad 3 / PgDn
    0x4B: 4,  # Numpad 4 / Left
    0x4C: 5,  # Numpad 5 / Clear
    0x4D: 6,  # Numpad 6 / Right
    0x47: 7,  # Numpad 7 / Home
    0x48: 8,  # Numpad 8 / Up
    0x49: 9,  # Numpad 9 / PgUp
}

NUMPAD_OFF_MAP = {
    VK_END: 1,
    VK_DOWN: 2,
    VK_NEXT: 3,
    VK_LEFT: 4,
    VK_CLEAR: 5,
    VK_RIGHT: 6,
    VK_HOME: 7,
    VK_UP: 8,
    VK_PRIOR: 9,
}

# KBDLLHOOKSTRUCT flags
LLKHF_EXTENDED = 0x01


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.wintypes.DWORD),
        ("scanCode", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


HOOKPROC = ctypes.WINFUNCTYPE(
    LRESULT,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.SetWindowsHookExW.argtypes = (
    ctypes.c_int,
    HOOKPROC,
    ctypes.wintypes.HINSTANCE,
    ctypes.wintypes.DWORD,
)
user32.SetWindowsHookExW.restype = HHOOK
user32.CallNextHookEx.argtypes = (
    HHOOK,
    ctypes.c_int,
    ctypes.wintypes.WPARAM,
    ctypes.wintypes.LPARAM,
)
user32.CallNextHookEx.restype = LRESULT
user32.UnhookWindowsHookEx.argtypes = (HHOOK,)
user32.UnhookWindowsHookEx.restype = ctypes.wintypes.BOOL


def is_numlock_on():
    return bool(user32.GetKeyState(VK_NUMLOCK) & 1)


class KeyboardHook:
    def __init__(self, window_manager):
        self.wm = window_manager
        self._hook = None
        self._thread = None
        self._stop_event = threading.Event()
        # Must keep a reference to the callback to prevent GC
        self._hook_proc = HOOKPROC(self._ll_keyboard_proc)

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name="kb-hook")
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._hook:
            user32.UnhookWindowsHookEx(self._hook)
            self._hook = None
        # Post WM_QUIT to unblock GetMessage
        if self._thread and self._thread.is_alive():
            tid = self._thread.ident
            if tid:
                user32.PostThreadMessageW(tid, 0x0012, 0, 0)  # WM_QUIT

    def _run(self):
        self._hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self._hook_proc,
            None,
            0,
        )
        if not self._hook:
            logger.error("Failed to install keyboard hook: %s", ctypes.GetLastError())
            return

        logger.info("Keyboard hook installed")

        # Message pump — required for low-level hooks to work
        msg = ctypes.wintypes.MSG()
        while not self._stop_event.is_set():
            result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result <= 0:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        if self._hook:
            user32.UnhookWindowsHookEx(self._hook)
            self._hook = None
        logger.info("Keyboard hook removed")

    def _ll_keyboard_proc(self, nCode, wParam, lParam):
        if nCode >= 0 and wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            slot = self._get_numpad_slot(kb)
            if slot is not None:
                self._handle_numpad(slot)
                return 1  # suppress this key

        return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

    def _get_numpad_slot(self, kb):
        vk = kb.vkCode
        scan = kb.scanCode
        flags = kb.flags
        is_extended = bool(flags & LLKHF_EXTENDED)
        numlock_on = is_numlock_on()

        # NumLock ON: only physical numpad digit keys 1-9 are accepted.
        if numlock_on and vk in NUMPAD_ON_MAP and not is_extended:
            return NUMPAD_ON_MAP[vk]

        # NumLock OFF: only numpad 1-9 nav equivalents are accepted, and they
        # must match both the expected VK code and numpad scan code.
        if not numlock_on and not is_extended and vk in NUMPAD_OFF_MAP:
            slot = NUMPAD_OFF_MAP[vk]
            if NUMPAD_SCANCODES.get(scan) == slot:
                return slot

        return None

    def _handle_numpad(self, slot):
        numlock_on = is_numlock_on()
        if numlock_on:
            # Assign mode
            result = self.wm.assign(slot)
            if result:
                hwnd, title = result
                logger.info("Slot %d assigned: %s", slot, title)
        else:
            # Focus mode
            focus_result = self.wm.focus(slot)
            if focus_result in ("missing", "stale"):
                result = self.wm.assign(slot)
                if result:
                    hwnd, title = result
                    logger.info("Slot %d was %s; assigned current window: %s", slot, focus_result, title)
                else:
                    logger.debug("Slot %d was %s, and no assignable window was found", slot, focus_result)
            elif focus_result == "error":
                logger.info("Slot %d focus failed; preserved existing assignment", slot)
