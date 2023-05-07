"""Jira client factory module."""
# pylint: disable=too-few-public-methods
import jira

from triage_tools import consts
class JiraClientFactory:
    """Jira client factory class."""
    @staticmethod
    def create(jira_access_token, validate=True):
        """Factory method to create a JiraClient."""
        client = jira.JIRA(\
            server=consts.JIRA_SERVER,\
            token_auth=jira_access_token,\
            validate=validate,\
            max_retries=0\
        )
        return client
