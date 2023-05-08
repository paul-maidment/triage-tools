"""Module for command line utility to fetch a single triage ticket"""
import argparse
import json
import os
import time
from triage_tools.jira_client import JiraClientFactory
from triage_tools.triage_ticket_search import TicketFetcher
from triage_tools.triage_ticket_search import TicketParser
from triage_tools.triage_ticket_search import TicketQuery
from triage_tools.triage_ticket_search import JiraAttachmentDownloader

from workflow_data import WorkflowData

class SearchForTickets:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []
        
    def run(self, workflow_data:"WorkflowData") -> "WorkflowData":
        """This runs the command"""
        # Set up the ticket fetcher
        self.workflow_data = workflow_data
        client = JiraClientFactory.create(self.args.jira_access_token)
        jira_attachment_downloader = JiraAttachmentDownloader(client)
        ticket_parser = TicketParser(jira_attachment_downloader)
        ticket_fetcher = TicketFetcher(ticket_parser, client)

        # Set up the JQL query
        query = TicketQuery.create(client).days_query(self.args.days)
        if self.args.jql is not None:
            query = query.jql_clause(' '.join(self.args.jql))

        # Paginate and process the query
        # This causes the logs to be downloaded and extracted if this has not already been done
        page_size = 100
        number_of_items = ticket_fetcher.count_for_query(query)
        self.workflow_data["number_of_items"] = number_of_items
        print(f"Number of items: {number_of_items}")
        self.workflow_data["issue_ids"] = []
        for startIndex in range(0, number_of_items, page_size):
            tickets = ticket_fetcher.fetch_page_by_query(query, page_size, startIndex)
            for ticket in tickets:
                self.workflow_data["issue_ids"] += [ticket.key]
            # Some throttling to prevent timeouts and overloads.
            time.sleep(2)

        # Once all tickets have been downloaded, return the workflow data with the ID's processed
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
        query_group = parser.add_argument_group(title="query parameters")
        query_args = query_group.add_argument_group()
        query_args.add_argument(
            '-j',
            "--jql",
            required=False,
            default=None,
            metavar='STRING',
            nargs='+',
            help='Additional JQL statement'
        )
        query_args.add_argument(
            '-d',
            "--days",
            required=True,
            default=7,
            help='Number of days worth of tickets to pull'
        )
        self.args, self.unknown_args = parser.parse_known_args()
