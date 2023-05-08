"""Module for command line utility to fetch a single triage ticket"""
import argparse
from workflow_data import WorkflowData
from triage_tools.triage_ticket_search import FilePathRecursor
from triage_tools.triage_ticket_search import ActionGrep
import os

class SearchByPathAndContent:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []

    def run(self, workflow_data:"WorkflowData") -> "WorkflowData":
        """This runs the command"""

        # Set up the recursor to grep directories.
        self.workflow_data = workflow_data
        content_regex = ' '.join(self.args.content_regex)
        path_regex = ' '.join(self.args.path_regex)
        self.grep_recursor = FilePathRecursor(ActionGrep(content_regex, workflow_data), recurse_after_action=False, path_match_regex=path_regex)

        # Go through the downloaded Jira tickets and grep them for the desired content
        # If issue ID's have been supplied from a previous step, attempt to use those.
        root_dir = os.path.join(os.path.expanduser('~'), "triage-tools-tickets")
        if "issue_ids" not in workflow_data:
            entries = os.listdir(root_dir)
        else:
            entries = workflow_data["issue_ids"]
        for entry in entries:
            full_path = os.path.join(root_dir, entry)
            self.grep_recursor.recurse(full_path)

        return self.workflow_data

    def process_arguments(self):
        """Process any command specific arguments"""
        parser = argparse.ArgumentParser(add_help=False)
        path_and_content_group = parser.add_argument_group(title="path and content search parameters")
        path_and_content_args = path_and_content_group.add_argument_group()
        path_and_content_args.add_argument(
            '-c',
            "--content_regex",
            required=True,
            metavar='STRING',
            nargs='+',
            help='Regex of files in which text search should be performed'
        )
        path_and_content_args.add_argument(
            '-p',
            "--path_regex",
            required=True,
            metavar='STRING',
            nargs='+',
            help='Regex of files in which text search should be performed'
        )
        self.args, self.unknown_args = parser.parse_known_args()
