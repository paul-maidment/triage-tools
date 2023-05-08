"""File path recursor module"""
import os
import re

class FilePathRecursor:
    """Recurses a filesystem and calls functions when files are encountered"""

    def __init__(self, on_file_action_class, recurse_after_action:bool, path_match_regex=None):
        """Constructor"""
        self.on_file_action_class = on_file_action_class
        self.recurse_after_action = recurse_after_action
        self.path_match_regex = path_match_regex

    def recurse(self, path:str):
        """Recursive function to navigate a file tree"""
        entries = os.listdir(path)
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                self.recurse(full_path)
            elif os.path.isfile(full_path):
                # This allows us to recurse a tree and perform an action on only the files that match the path_match_regex.
                # If the path_match_regex is not set (None) then the action will be performed on every file.
                if self.path_match_regex is None or re.search(self.path_match_regex, full_path):
                    new_path = self.on_file_action_class.file_action(full_path)
                    if new_path is not None and self.recurse_after_action:
                        self.recurse(new_path)


