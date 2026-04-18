import logging
import pystray
from pystray import MenuItem
from numan.icon import create_icon_image

logger = logging.getLogger(__name__)


class TrayApp:
    def __init__(self, window_manager, keyboard_hook, config, open_settings_fn):
        self.wm = window_manager
        self.hook = keyboard_hook
        self.config = config
        self._open_settings_fn = open_settings_fn
        self._icon = None

    def run(self):
        image = create_icon_image(64)
        self._icon = pystray.Icon(
            "numan",
            image,
            "NumaN — Numpad Window Manager",
            menu=self._build_menu(),
        )
        self._icon.run(setup=self._on_setup)

    def _on_setup(self, icon):
        icon.visible = True
        self.hook.start()
        self.wm.start_watcher()
        self.wm.set_on_change(self._refresh_menu)
        logger.info("NumaN started")

    def _build_menu(self):
        slot_items = []
        info = self.wm.get_slot_info()
        for i in range(1, 10):
            title = info.get(i)
            if title:
                short = title[:35] + "..." if len(title) > 35 else title
                label = f"{i}: {short}"
            else:
                label = f"{i}: (empty)"
            slot_items.append(MenuItem(label, None, enabled=False))

        return pystray.Menu(
            MenuItem("NumaN Slots", pystray.Menu(*slot_items)),
            pystray.Menu.SEPARATOR,
            MenuItem("Clear All Windows", self._on_clear_all),
            MenuItem("Settings", self._on_settings),
            MenuItem("Quit", self._on_quit),
        )

    def _refresh_menu(self):
        if self._icon:
            self._icon.menu = self._build_menu()
            self._icon.update_menu()

    def _on_clear_all(self, icon=None, item=None):
        self.wm.clear_all_slots()

    def _on_settings(self, icon=None, item=None):
        self._open_settings_fn()

    def _on_quit(self, icon=None, item=None):
        logger.info("Quitting NumaN")
        self.hook.stop()
        self.wm.stop_watcher()
        if self._icon:
            self._icon.stop()
