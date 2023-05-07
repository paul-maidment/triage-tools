"""The grepper module"""
import re
from .log_search_config import LogSearchConfig

class Grepper:
    """Performs a very simple streamed regex search against a single file"""

    def __init__(self, log_search_config:LogSearchConfig):
        """Constructor"""
        self.log_search_config = log_search_config

    def file_matches(self, path) -> bool:
        """Does the specified file have a match against the search config?"""
        for item in self.log_search_config.items:
            # Check whether or not the current path is a match for the regex
            if re.search(item.path_regex, path) and self.file_pattern_matches(path, item.content_regex):
                return True
            # self.search_stats.record_match(f"Fake match {item.label}", path)
        # If nothing was found, there was no match
        return False

    def file_pattern_matches(self, path, pattern) -> bool:
        """Does the specified file have a match against the pattern?"""
        print(f"Checking for match {path} {pattern}")
        file = open(path, "r")
        for line in file:
            if re.search(pattern, line):
                return True

    