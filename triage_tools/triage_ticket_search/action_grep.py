import os
import re
import subprocess
from subprocess import PIPE

class ActionGrep:

    def __init__(self, pattern, workflow_data):
        self.pattern = pattern
        self.workflow_data = workflow_data

    def get_id_from_aitriage_path(self, path) -> str:
        result = re.findall(r"(AITRIAGE-\d*)", path)
        if len(result) > 0:
            return result[0]
        return None

    def store_match(self, issue_id, full_path):
        if "matches" not in self.workflow_data:
            self.workflow_data["matches"] = {}
        if issue_id not in self.workflow_data["matches"]:
            self.workflow_data["matches"][issue_id] = []
        self.workflow_data["matches"][issue_id] += [full_path]

    def parse_and_store_matches(self, issue_id, matched:list[str]):
        for match in matched:
            self.store_match(issue_id, match)

    def file_action(self, full_path):
        process = subprocess.Popen(['/bin/grep', '-lir', self.pattern, full_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        if process.returncode == 2: # Indicates that there was an error
            print(f"Got an error: {full_path}")
            raise Exception(f"Error during grep for content regex {self.pattern} error was {error}")
        if process.returncode == 1: # Indicates that no lines were selected.
            print(f"Got no match: {full_path}")
            return False
        if process.returncode == 0: # Lines were selected.
            print(f"Got a match: {full_path}")
            self.parse_and_store_matches(self.get_id_from_aitriage_path(full_path), output.decode("utf-8").split("\n"))
            return True
