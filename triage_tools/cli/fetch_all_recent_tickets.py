"""Module for command line utility to fetch a single triage ticket"""
import argparse
import json
import math
import os
import time
from triage_tools.jira_client.jira_client_factory import JiraClientFactory
from triage_tools.triage_ticket_search import LogDirectoryDownloader
from triage_tools.triage_ticket_search.ticket_fetcher import TicketFetcher
from triage_tools.triage_ticket_search.ticket_parser import TicketParser
from triage_tools.triage_ticket_search.archive_extractor import ArchiveExtractor
from triage_tools.triage_ticket_search.ticket_query import TicketQuery
from triage_tools.triage_ticket_search.log_search_config import ConfigParser
from triage_tools.triage_ticket_search.grepper import Grepper
from triage_tools.triage_ticket_search.search_stats import SearchStats

class FetchRecentTriageTicketsCmd:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []
        self._process_arguments()
        
    def _get_ticket_fetcher(self, client):
        self.config = self.load_config_file()
        client = JiraClientFactory.create(self.args.jira_access_token)
        
        # Set up the search config
        search_config = ConfigParser.get_log_search_config(self.config)
        grepper = Grepper(search_config)
        archive_extractor = ArchiveExtractor(grepper)
        log_directory_downloader = LogDirectoryDownloader(archive_extractor, grepper)
        ticket_parser = TicketParser(log_directory_downloader)
        return TicketFetcher(client, ticket_parser)

    def load_config_file(self):
        """Loads the config file from disk"""
        with open(self.args.query_file, 'r') as f:
             data = json.load(f)
        return data

    def run(self):
        """This runs the command"""
        # Set up the ticket fetcher
        client = JiraClientFactory.create(self.args.jira_access_token)
        ticket_fetcher = self._get_ticket_fetcher(client)

        # Map the query parameters
        query = TicketQuery.create(client).days_query(self.config['query']['days'])
        jql_clauses = ConfigParser.get_jira_queries(self.config)
        for jql in jql_clauses:
            query = query.jql_clause(jql)

        # Fetch the tickets in pages
        page_size = 100
        number_of_items = ticket_fetcher.count_for_query(query)
        for startIndex in range(0, number_of_items, page_size):
            ticket_fetcher.fetch_page_by_query(query, page_size, startIndex)
            time.sleep(2)

    def _process_arguments(self):
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
        query_group = parser.add_argument_group(title="query_file")
        query_args = query_group.add_argument_group()
        query_args.add_argument(
            "--query_file",
            required=False,
            default="",
            help="The path to a JSON formatted query file to supply parameters for your query"
        )
        self.args, self.unknown_args = parser.parse_known_args()
