"""The module for the main cli app"""
# pylint: disable=too-few-public-methods
import argparse
import logging
from fetch_by_id import FetchById
from triage_tools.cli.search_for_tickets import SearchForTickets
from search_by_path_and_content import SearchByPathAndContent
from generate_json_report import GenerateJSONReport
from workflow_data import WorkflowData
class App:
    """General launcher app for command line utilities"""
    def __init__(self, arguments:list[str]):
        self.args = arguments

    def run(self):
        """App entry point"""

        # Data structure to store results between workflows.
        workflow_data = WorkflowData()

        # Get the workflow to run
        cmds = self.setup_cmds()

        # Validate the parameters for the workflow the user has chosen.
        # We evaluate the params for all workflows at once to ensure timely feedback.
        for cmd in cmds:
            cmd.process_arguments()

        # Run the chosen workflow by running all cmds in the flow.
        for cmd in cmds:
            workflow_data = cmd.run(workflow_data)

    def setup_cmds(self):
        # Set up the workflow according to user settings
        cmds = []   
        if self.args.fetch is not None and self.args.fetch == "fetch_by_id":
            cmds += [FetchById()]
        elif self.args.fetch is not None and self.args.fetch == "search_for_tickets":
            cmds += [SearchForTickets()]
        cmds += [SearchByPathAndContent()]
        cmds += [GenerateJSONReport()]
        return cmds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    functionGroup = parser.add_argument_group(title="function")
    functionGroup.add_argument(
        "--fetch",
        required=False,
        help="The fetch function to use (if any)",
    )
    args, unknown = parser.parse_known_args()
    logging.basicConfig(level=logging.WARN, format="%(levelname)-10s %(message)s")
    logger = logging.getLogger(__name__)
    logging.getLogger("__main__").setLevel(logging.INFO)
    application = App(args)
    application.run()
