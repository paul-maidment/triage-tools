"""Ticket Parser module"""
import os
import re
from .triage_ticket import TriageTicket
from .log_directory_downloader import LogDirectoryDownloader

class TicketParser:
    """Responsible for parsing ticket details and log file directory from the jira issue"""
    def __init__(self, log_directory_downloader:"LogDirectoryDownloader"):
        """Constructor"""
        self.log_directory_downloader = log_directory_downloader

    def parse(self, jira_issue) -> "TriageTicket":
        print(f"Parsing jira issue {jira_issue.key}...")
        """Parse a Jira issue and return a parsed TriageTicket ready for use"""
        if jira_issue is None:
            print("WARNING: Attempted to parse an empty Jira issue")
            return None
        triage_ticket = TriageTicket(jira_issue)
        triage_ticket = self.parse_logs_url(triage_ticket)
        triage_ticket.log_files = \
            self.log_directory_downloader.download(triage_ticket.logs_url, \
                os.path.join(os.path.expanduser('~'), "triage-tools-tickets"), triage_ticket.key)
        print(f"Parsing done for {jira_issue.key}...")
        return triage_ticket

    def parse_logs_url(self, triage_ticket:"TriageTicket") -> "TriageTicket":
        """Parse the logs url from the ticket description"""
        if triage_ticket.description is None:
            return triage_ticket
        match = re.search(r"(\bInstallation logs - requires VPN\|)(htt.*\/)",\
             triage_ticket.description)
        if match is not None:
            triage_ticket.logs_url = match.group(2).replace("#", "files")
        return triage_ticket
