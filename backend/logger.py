import logging


class FileLogger:
    def __init__(self, log_file_name):

        # Define the path to the log file
        self.log_file_path = f'./backend/{log_file_name}'

        # Create a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Set the log level to INFO

        # Create a file handler and set the log file path
        self.file_handler = logging.FileHandler(self.log_file_path)
        self.file_handler.setLevel(logging.INFO)

        # Create a formatter
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)

        # Add the file handler to the logger
        self.logger.addHandler(self.file_handler)

    def log(self, message):
        # Log the message
        self.logger.info(message)
