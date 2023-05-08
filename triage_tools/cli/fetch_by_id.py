"""Module for command line utility to fetch a single triage ticket"""
import argparse
import os
from triage_tools.jira_client import JiraClientFactory
from triage_tools.triage_ticket_search import TicketFetcher
from triage_tools.triage_ticket_search import TicketParser
from workflow_data import WorkflowData
from triage_tools.triage_ticket_search import JiraAttachmentDownloader

class FetchById:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []

    def run(self, workflow_data:"WorkflowData") -> "WorkflowData":
        """This runs the command"""
        self.workflow_data = workflow_data
        client = JiraClientFactory.create(self.args.jira_access_token)
        jira_attachment_downloader = JiraAttachmentDownloader(client)
        ticket_parser = TicketParser(jira_attachment_downloader)
        ticket_fetcher = TicketFetcher(client, ticket_parser)
        ticket_fetcher.fetch_single_ticket_by_key(\
            self.args.issue_id) # Ticket will now be stored in the download directory.
        self.workflow_data["issue_ids"] = [self.args.issue_id]
        # Once the ticket has been downloaded, return the workflow data with the ID processed
        return self.workflow_data

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
