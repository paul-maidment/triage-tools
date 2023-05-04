"""Ticket fetcher module"""

import jira
from tools import consts
from .ticket_query import TicketQuery
from .ticket_parser import TicketParser
from .triage_ticket import TriageTicket


class TicketFetcher:
    """Responsible for fetching tickets from Jira in response to queries"""
    def __init__(self, jira_client:"jira", ticket_parser:"TicketParser"):
        """Constructor"""
        self.client = jira_client
        self.ticket_parser = ticket_parser

    def fetch_single_ticket_by_key(self, key) -> "TriageTicket":
        """Fetches a single triage ticket from Jira using the key"""
        try:
            issue = self.client.issue(key)
            if issue is not None:
                if issue.fields.components[0].name != consts.TRIAGE_TICKET_SEARCH_COMPONENT:
                    print(f"WARNING: Ticket fetched for ID {key} \
                        but the component indicates that this is not a triage ticket. \
                        Returning None for this ticket.")
                    return None
                print(f"Fetched {key}, parsing...")
                return self.ticket_parser.parse(issue)
            return None
        except jira.exceptions.JIRAError as exception:
            if exception.status_code == 404:
                print(f"Jira issue with ID {key} was not found!")
                return None
            raise

    def count_for_query(self, query:"TicketQuery"):
        """Helper for pagination, provides a total item count for a query in an efficient way"""
        query_text = query.build()
        return self.client.search_issues(query_text, maxResults=1).total

    def fetch_page_by_query(self, query:"TicketQuery", page_size, start_index) \
        -> list["TriageTicket"]:
        """Fetches a specific page of a query, given a pagesize and startindex"""
        tickets = [TriageTicket]
        query_text = query.build()
        issues = self.client.search_issues(query_text, maxResults=page_size, startAt=start_index)
        for issue in issues:
            tickets += self.ticket_parser.parse(issue)
