"""Search report module"""
from .search_match import SearchMatch

class SearchReport:
    """Represents a search report"""

    def __init__(self, jql, total_issue_count, file_regex, search_regex):
        """Constructor"""
        self.jql = jql
        self.total_issue_count = total_issue_count
        self.number_of_issues_with_logs = 0
        self.file_regex = file_regex
        self.search_regex = search_regex
        self.matches = []

    def increment_issues_with_logs(self, qty:int):
        """Increment the number of registered issues"""
        self.number_of_issues_with_logs += qty

    def add_match(self, match:"SearchMatch"):
        """To be called when registering a match"""
        self.matches += [match]

    
