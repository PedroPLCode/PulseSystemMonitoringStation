import logging

pulse_log_filename = "pulse.log"
gunicorn_log_filename = "gunicorn.log"
logs = [pulse_log_filename, gunicorn_log_filename]

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)

general_handler = logging.FileHandler(pulse_log_filename)
general_handler.setLevel(logging.DEBUG)
general_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
general_handler.setFormatter(general_formatter)

logger.addHandler(general_handler)
