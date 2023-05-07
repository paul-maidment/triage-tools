"""Log directory downloader module"""
# pylint: disable=too-few-public-methods
import json
import os
import shutil
import sys
from urllib.parse import urljoin
import requests
import time
from .archive_extractor import ArchiveExtractor
from .grepper import Grepper

class LogDirectoryDownloader:
    """Responsible for the download of the entire directory structure \
        indicated by the log url - including subdirectories"""

    def __init__(self, archive_extractor:"ArchiveExtractor", grepper:"Grepper"):
        self.archive_extractor = archive_extractor
        self.grepper = grepper

    def download(self, logs_url:str, download_path:str, ticket_id:str):
        print(f"Downloading files for {ticket_id}\n\
            Logs URL is {logs_url}\n\
            Downloading to path {os.path.join(download_path, ticket_id)}")
        """Download all of the logs under the given URL to the specified download path"""
        if logs_url is None:
            print(f"WARNING: No logs URL specified, \
                unable to download logs for ticket ID {ticket_id}")
            return
        response = self.requestWithRetry(logs_url)
        if response.status_code == 200 and response.content != "":
            full_path = os.path.join(download_path, ticket_id)
            self.process_dir(logs_url, full_path)

    def process_dir(self, url:str, download_path:str):
        """Process one level of downloads, recursing or creating files as necessary"""
        self.mkdir(download_path)
        try:
            response = requests.get(url, timeout=120, allow_redirects=True)
            if response.status_code == 200 and response.content != "":
                file_list_json = json.loads(response.content)
                for item in file_list_json:
                    name = item["name"]
                    if item["type"] == "directory":
                        self.process_dir(urljoin(url , name + "/"), os.path.join(download_path, name))
                    elif item["type"] == "file":
                        self.download_file(urljoin(url, name), os.path.join(download_path, name))
        except (IOError, FileNotFoundError, FileExistsError) as exception:
            print(f"Fatal Error: Unable to obtain JSON manifest\
                 for path {url} due to exception {exception}")
            sys.exit()

    def mkdir(self, path):
        """Make a directory if it does not exist"""
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except (IOError, FileNotFoundError, FileExistsError) as exception:
                print(f"Fatal Error: Unable to mkdir {path} due to excpetion {exception}")
                sys.exit()

    def requestWithRetry(self, url, numberOfRetries=10, backOffSeconds=10, timeout=20):
        """A more resilient download with some retries and delays as needed"""
        lastException = None
        for tries in range(numberOfRetries):
            try:
                return requests.get(url, timeout=timeout)
            except requests.exceptions.RequestException as exception:  # This is the correct syntax
                lastException = exception
                print(f"Request to {url} timed out {tries}/{numberOfRetries}")
                time.sleep(backOffSeconds)
        raise lastException

    def download_file(self, url:str, download_path:str):
        """Download a file from a url to a specific download path"""
        try:
            response = self.requestWithRetry(url)
            with open(download_path, "wb") as file:
                file.write(response.content)
        except (IOError, FileNotFoundError, FileExistsError) as exception:
            print(f"Fatal Error: Unable to down load file from \
                {url} to {download_path} due to excpetion {exception}")
            sys.exit()

        # Now decide whether or not we should extract and recurse, or grep the file
        if self.archive_extractor.is_supported_archive(download_path):
            # Decompress any downloaded archive "in place"
            path_parts = download_path.split("/")
            path_parts[-1] = "extracted_" +path_parts[-1].replace(".", "_")
            extraction_directory = "/".join(path_parts)
            self.archive_extractor.try_extract(download_path, extraction_directory)
        # else:
        #    self.grepper.file_matches(download_path)
