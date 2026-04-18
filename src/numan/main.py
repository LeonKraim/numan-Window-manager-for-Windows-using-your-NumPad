import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from numan.config import CONFIG_DIR, Config
from numan.window_manager import WindowManager
from numan.keyboard_hook import KeyboardHook
from numan.tray import TrayApp
from numan.settings import SettingsWindow

logger = logging.getLogger("numan")
LOG_FILE = os.path.join(CONFIG_DIR, "numan.log")


def configure_logging():
    handlers = [logging.StreamHandler(sys.stdout)]
    file_logging_error = None

    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        handlers.append(
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=256 * 1024,
                backupCount=3,
                encoding="utf-8",
            )
        )
    except OSError as exc:
        file_logging_error = exc

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=handlers,
        force=True,
    )

    if file_logging_error is not None:
        logger.warning("Failed to initialize file logging: %s", file_logging_error)
    else:
        logger.info("Runtime logs: %s", LOG_FILE)


def main():
    configure_logging()
    logger.info("NumaN starting...")

    config = Config.load()
    wm = WindowManager()
    settings_window = SettingsWindow(config)

    hook = KeyboardHook(wm)
    tray = TrayApp(wm, hook, config, open_settings_fn=settings_window.open)
    tray.run()  # blocks on main thread


if __name__ == "__main__":
    main()
