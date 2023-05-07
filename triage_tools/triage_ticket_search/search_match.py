"""The search match module"""

class SearchMatch:
    """Represents a match to a seach"""
    def __init__(self, issue_number, search_regex, matched_path):
        """Constructor to be called when registering a search match"""
        self.issue_number = issue_number
        self.search_regex = search_regex
        self.matched_path = matched_path
        pass