
from typing import List
from parse.apache_log_entry import ApacheLogEntry

class ApacheLogFile:
    """
    Class representing an Apache log file containing multiple log entries.

    This class encapsulates the information about a Apache log file.

    Attributes:
        path (str): The path of the file.
        entries (List[ApacheLogEntry]): The list of the entries founded in the file.
    """

    def __init__(self, path):
        self.path = path
        self.entries = []

    def add_entry(self, entry: List[ApacheLogEntry]):
        """
        Add a new entry.

        Args:
            entry (LogEntry): The entry of the Apache log.
        """
        self.entries.append(entry)