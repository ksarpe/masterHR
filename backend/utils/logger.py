import logging
import coloredlogs

logging.addLevelName(15, 'SUCCESS')

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

        setattr(self.logger, 'success', lambda message, *args: self.logger._log(15, message, args))

        # Define custom colors for different log levels
        level_styles = {
            'warning': {'color': 'yellow'},
            'info': {'color': 'blue'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True},
            'success': {'color': 'green'},  # New log level styling
        }

        # Define a custom format for the log messages
        log_format = "%(asctime)s.%(msecs)03d - (%(programname)s:%(lineno)s - %(funcName)s()) - [%(levelname)s] - %(message)s"

        # Define custom colors
        field_styles = {
            'asctime': {'color': 'cyan'},
            'levelname': {'color': 'black', 'bold': True},
            'name': {'color': 'blue'},
            'programname': {'color': 'cyan'},
            'funcName': {'color': 'cyan'},
        }

        # Install the custom colored logs
        coloredlogs.install(level='DEBUG', level_styles=level_styles, fmt=log_format, field_styles=field_styles)

    def get_logger(self):
        return self.logger