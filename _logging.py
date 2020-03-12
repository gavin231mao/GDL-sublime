# logger based on <https://github.com/SublimeText/PackageDev/blob/master/_logging.py>
# Python docs <https://docs.python.org/3/library/logging.html>

import logging
import sublime

# usage in other files in package:
# log = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_LEVEL_NAME = logging.getLevelName(DEFAULT_LOG_LEVEL)
EVENT_LEVEL = logging.INFO

package_logger = logging.getLogger(__package__)
handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="[{name}] {levelname}: {message}", style='{')
handler.setFormatter(formatter)
package_logger.addHandler(handler)
package_logger.setLevel(DEFAULT_LOG_LEVEL)

logger = logging.getLogger(__name__)


def _settings():
	return sublime.load_settings("GDLDev.sublime-settings")


def plugin_loaded():
	def on_settings_reload():
		cur_log_level = package_logger.getEffectiveLevel()
		cur_log_level_name = logging.getLevelName(cur_log_level)
		new_log_level_name = _settings().get('log_level', DEFAULT_LOG_LEVEL_NAME).upper()
		new_log_level = getattr(logging, new_log_level_name, DEFAULT_LOG_LEVEL)

		if new_log_level_name != cur_log_level_name:
			if cur_log_level > EVENT_LEVEL and new_log_level <= EVENT_LEVEL:
				# Only set level before emitting log event if it would not be seen otherwise
				package_logger.setLevel(new_log_level)
			logger.log(EVENT_LEVEL,
					   "Changing log level from %r to %r",
					   cur_log_level_name, new_log_level_name)
			package_logger.setLevel(new_log_level)  # Just set it again to be sure

	_settings().add_on_change(__name__, on_settings_reload)
	on_settings_reload()  # trigger on inital settings load, too


def plugin_unloaded():
	_settings().clear_on_change(__name__)
	package_logger.removeHandler(handler)