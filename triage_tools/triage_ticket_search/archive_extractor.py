"""Recursive extractor module"""
import gzip
import os
import shutil
import tarfile
import lzma
from .grepper import Grepper

class ArchiveExtractor:
    """Responsible for the recursive extraction of archives"""
    def __init__(self, grepper:"Grepper"):
        self.grepper = grepper

    def is_supported_archive(self, filename) -> bool:
        return tarfile.is_tarfile(filename) or filename.endswith(".gz") or filename.endswith(".xz")

    def extract_xz(self, src_file, dest_dir):
        """Support for extraction of xz format"""
        file_content = ""
        basename = os.path.basename(src_file)
        dest_path = os.path.join(dest_dir, basename[:basename.rindex('.')])
        with lzma.open(src_file, 'rb') as f:
            file_content = f.read()
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        with open(dest_path, "wb") as out:
            out.write(file_content)

    def extract_gzip(self, src_file, dest_dir):
        """Support for extraction of gzip format"""
        file_content = ""
        basename = os.path.basename(src_file)
        dest_path = os.path.join(dest_dir, basename[:basename.rindex('.')])
        with gzip.open(src_file, 'rb') as f:
            file_content = f.read()
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        with open(dest_path, "wb") as out:
            out.write(file_content)

    def try_extract(self, src_file:str, dest_dir:str):
        """Try to extract the specified file into the desitination directory"""
        try:
            is_tarfile = tarfile.is_tarfile(src_file)
            is_gz = src_file.endswith(".gz")
            is_xz = src_file.endswith(".xz")
            if is_tarfile:
                print(f"Extracting tarfile: {src_file} {dest_dir}")
                tarfile.open(src_file).extractall(path=dest_dir)
            elif is_gz:
                print(f"Extracting gzip file: {src_file} {dest_dir}")
                self.extract_gzip(src_file, dest_dir)
            elif is_xz:
                print(f"Extracting xz file: {src_file} {dest_dir}")
                self.extract_xz(src_file, dest_dir)
            if is_tarfile or is_gz or is_xz:
                os.remove(src_file) 
                self.scan_dir(dest_dir)
                return
        except Exception as e:
            print(f"Ignoring {src_file} due to extraction errors during extraction to {dest_dir}, please check that the file is a valid archive. src path length:{len(src_file)} {e}")
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)

    def scan_dir(self, path:str):
        """Recursively scan for new archives"""
        entries = os.listdir(path)
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                self.scan_dir(full_path)
            elif os.path.isfile(full_path):
                if self.is_supported_archive(full_path):
                    subdir = entry.split("/")[-1].replace(".", "_")
                    extraction_directory = os.path.join(path, subdir)
                    self.try_extract(full_path, extraction_directory)
                # else:
                #    self.grepper.file_matches(full_path)
