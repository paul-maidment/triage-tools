"""Triage ticket module"""
# pylint: disable=too-few-public-methods

class TriageTicket:
    """A class to model a triage ticket retrieved from Jira"""
    def __init__(self, issue):
        """Constructor"""
        self.key = issue.key
        self.issue = issue
        self.description = issue.fields.description
