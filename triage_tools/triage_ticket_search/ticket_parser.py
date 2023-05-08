"""Ticket Parser module"""
from .triage_ticket import TriageTicket
from .jira_attachment_downloader import JiraAttachmentDownloader

class TicketParser:
    """Responsible for parsing ticket details and log file directory from the jira issue"""
    def __init__(self, jira_attachment_downloader:"JiraAttachmentDownloader"):
        """Constructor"""
        self.jira_attachment_downloader = jira_attachment_downloader

    def parse(self, jira_issue) -> "TriageTicket":
        """Parse a Jira issue and return a parsed TriageTicket ready for use"""
        if jira_issue is None:
            print("WARNING: Attempted to parse an empty Jira issue")
            return None
        triage_ticket = TriageTicket(jira_issue)
        self.jira_attachment_downloader.download_attachments_for_ticket(triage_ticket.issue)
        return triage_ticket


