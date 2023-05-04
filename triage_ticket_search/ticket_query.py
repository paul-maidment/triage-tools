"""TicketQuery module"""
import logging

class TicketQuery:
    """Represents a query to Jira for a triage ticket"""
    def __init__(self, jira_client, project_filter, component_filter):
        """Constructor"""
        self.jira_client = jira_client
        self.logger = logging.getLogger(__name__)
        self.project_filter = project_filter
        self.component_filter = component_filter
        self.queries = []
        self.columns = []

    @staticmethod
    def create(jira_client, project_filter = "AITRIAGE", \
        component_filter = "Cloud-Triage") -> "TicketQuery":
        """Create a TicketQuery"""
        return TicketQuery(jira_client, project_filter, component_filter).\
            project_filter_query().\
            component_filter_query()

    def column(self, name:str) -> "TicketQuery":
        """Specify output columns for the query"""
        self.columns += [name]
        return self

    def days_query(self, number_of_days:int) -> "TicketQuery":
        """Specifies how far back (in days) to look for tickets"""
        self.queries +=  [f"created >= -{number_of_days}d"]
        return self

    def project_filter_query(self) -> "TicketQuery":
        """Filter by the project filter"""
        self.queries += [f"project = \"{self.project_filter}\" "]
        return self

    def component_filter_query(self) -> "TicketQuery":
        """Filter by the component filter"""
        self.queries += [f"component = \"{self.component_filter}\""]
        return self

    def text_like_query(self, term:str) -> "TicketQuery":
        """Filter for text similar to term"""
        self.queries += [f"text ~ \"{term}\""]
        return self

    def build(self) -> str:
        """Build the query string"""
        return "(" + " AND ".join(self.queries) + ") ORDER BY created DESC"
