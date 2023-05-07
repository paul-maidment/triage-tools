"""Module for command line utility to fetch a single triage ticket"""
import argparse
import os
from triage_tools.jira_client.jira_client_factory import JiraClientFactory
from triage_tools.triage_ticket_search import LogDirectoryDownloader
from triage_tools.triage_ticket_search.ticket_fetcher import TicketFetcher
from triage_tools.triage_ticket_search.ticket_parser import TicketParser
from triage_tools.triage_ticket_search.archive_extractor import ArchiveExtractor

class FetchTriageTicketCmd:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []

    def run(self):
        """This runs the command"""
        self.process_arguments()
        client = JiraClientFactory.create(self.args.jira_access_token)
        archive_extractor = ArchiveExtractor()
        log_directory_downloader = LogDirectoryDownloader(archive_extractor)
        ticket_parser = TicketParser(log_directory_downloader)
        ticket_fetcher = TicketFetcher(client, ticket_parser)
        ticket_fetcher.fetch_single_ticket_by_key(\
            self.args.issue_id) # Ticket will now be stored in the download directory.

    def process_arguments(self):
        """Process any command specific arguments"""
        parser = argparse.ArgumentParser(add_help=False)
        login_group = parser.add_argument_group(title="login options")
        login_args = login_group.add_argument_group()
        login_args.add_argument(
            "--jira-access-token",
            default=os.environ.get("JIRA_ACCESS_TOKEN"),
            required=True,
            help="PAT (personal access token) for accessing Jira",
        )
        query_group = parser.add_argument_group(title="query")
        query_args = query_group.add_argument_group()
        query_args.add_argument(
            "--issue-id",
            required=True,
            help="JIRA issue ID for the triage ticket"
        )
        self.args, self.unknown_args = parser.parse_known_args()
