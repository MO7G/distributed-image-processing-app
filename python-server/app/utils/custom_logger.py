import logging

class CustomLogger:
    def __init__(self, log_file_path='app.log', print_to_terminal=True, log_level=logging.DEBUG):
        self.log_file_path = log_file_path
        self.print_to_terminal = print_to_terminal
        self.log_level = log_level
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)

        if self.print_to_terminal:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)



# for testing here 
if __name__ == "__main__":
    logger = CustomLogger(log_file_path='my_app.log', print_to_terminal=False, log_level=logging.DEBUG)
    logger.debug("Debug message")  # This won't be logged because the logging level is set to INFO
    logger.info("Info message")    # This will be logged
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
