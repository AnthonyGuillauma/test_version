
import os
import json

class ExportationException(Exception):

    def __init__(self, *args):
        super().__init__(*args)

class Exporter:

    def __init__(self, export_path: str, override: bool):
        self.override_mode = override
        if self.__can_create_file(export_path):
            self.export_path = export_path

    def __can_create_file(self, path: str):
        absolute_path = os.path.abspath(path)
        if not self.override_mode:
            if os.path.isfile(absolute_path):
                raise ExportationException(f"The file {absolute_path} already exists.")
        parent_directory = os.path.dirname(absolute_path)
        if not os.path.isdir(parent_directory):
            raise ExportationException(f"The directory {parent_directory} doesn't exist.")
        if not os.access(parent_directory, os.W_OK):
            raise ExportationException(f"No right to write in the directory {parent_directory}")
        return True

    def export_to_json(self, datas):
        """
        Export the given datas in a json file.
        The path of the file was given in the __init__

        Args:
            datas (object) : the datas that will be included in the json file
        """
        with open(self.export_path, 'w') as file:
            json.dump(datas, file, indent=4)