import os
import shutil
import gzip

class ActionExtractArchive:

    def __init__(self):
        self.archive_extensions = []
        for format in shutil.get_unpack_formats():
            self.archive_extensions.extend(format[1])

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

    def file_action(self, full_path):
        pathparts = full_path.split("/")
        name = pathparts[-1]
        path = '/'.join(pathparts[:-1])
        for ext in self.archive_extensions:
            if name.endswith(ext):
                archive_path = os.path.join(path, name)
                dest_path = os.path.join(path, f"extracted_" + name.replace(".", "_"))
                shutil.unpack_archive(archive_path, dest_path)
                os.remove(archive_path)
                return dest_path
        if name.endswith(".gz"):
            archive_path = os.path.join(path, name)
            dest_path = os.path.join(path, "extracted_" + name.replace(".", "_"))
            self.extract_gzip(archive_path, dest_path)
            os.remove(archive_path)
            return dest_path
        return None
