"""Triage ticket module"""
# pylint: disable=too-few-public-methods

class TriageTicket:
    """A class to model a triage ticket retrieved from Jira"""
    def __init__(self, issue):
        """Constructor"""
        self.key = issue.key
        self.raw = issue.raw
        self.description = issue.fields.description
        self.logs_url = None
        self.log_files = []
