"""The module for the main cli app"""
# pylint: disable=too-few-public-methods
import argparse
import logging
from triage_tools.cli.fetch_triage_ticket_cmd import FetchTriageTicketCmd
from triage_tools.cli.fetch_all_recent_tickets import FetchRecentTriageTicketsCmd
# from jira_client import JiraClientFactory
class App:
    """General launcher app for command line utilities"""
    def __init__(self, arguments:list[str]):
        self.args = arguments

    def run(self):
        """The entry point of the cli"""
        print(f"App->run() {self.args}")
        
        if self.args.function == "fetch_triage_ticket":
            cmd = FetchTriageTicketCmd()
            cmd.run()
        elif self.args.function == "fetch_all_recent_tickets":
            cmd = FetchRecentTriageTicketsCmd()
            cmd.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    functionGroup = parser.add_argument_group(title="function")
    functionGroup.add_argument(
        "--function",
        required=True,
        help="The function of the app we wish to use",
    )
    args, unknown = parser.parse_known_args()
    logging.basicConfig(level=logging.WARN, format="%(levelname)-10s %(message)s")
    logger = logging.getLogger(__name__)
    logging.getLogger("__main__").setLevel(logging.INFO)
    application = App(args)
    application.run()
