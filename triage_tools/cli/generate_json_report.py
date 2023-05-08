"""Module for command line utility to fetch a single triage ticket"""
import argparse
from workflow_data import WorkflowData

class GenerateJSONReport:
    """Responsible for fetching a single ticket for a triage issue"""

    def __init__(self):
        """Constructor"""
        self.args = []
        self.unknown_args = []

    def run(self, workflow_data:"WorkflowData") -> "WorkflowData":
        """This runs the command"""
        self.workflow_data = workflow_data

        print(f"Processing finished: {workflow_data}")

        return self.workflow_data

    def process_arguments(self):
        """Process any command specific arguments"""

