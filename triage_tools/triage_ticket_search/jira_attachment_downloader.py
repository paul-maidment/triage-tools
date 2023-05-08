import sys
import time
import jira
import os
from .file_path_recursor import FilePathRecursor
from .action_extract_archive import ActionExtractArchive

class JiraAttachmentDownloader:

    def __init__(self, jira_client:"jira"):
        self.jira_client = jira_client
        self.extraction_recursor = FilePathRecursor(ActionExtractArchive(), recurse_after_action=True)

    def download_attachments_for_ticket(self, issue):
        time.sleep(5) # Don't hammer the server with download requests
        destination_path = os.path.join(os.path.expanduser('~'), "triage-tools-tickets", issue.key)
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        for attachment in issue.fields.attachment:
            content = attachment.get()
            write_path = os.path.join(destination_path, attachment.filename)
            self.write_content_to_file(content, write_path)
        self.extraction_recursor.recurse(destination_path)

    def write_content_to_file(self, content, path:str):
        """Download a file from a url to a specific download path"""
        try:
            with open(path, "wb") as file:
                file.write(content)
        except (IOError, FileNotFoundError, FileExistsError) as exception:
            print(f"Fatal Error: Unable to write file to {path} due to excpetion {exception}")
            sys.exit()

    



    