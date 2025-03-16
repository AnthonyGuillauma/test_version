
import os
from re import compile
from datetime import datetime
from parse.apache_log_file import ApacheLogFile
from parse.apache_log_entry import ApacheLogEntry
from data.client_info import ClientInfo
from data.request_info import RequestInfo
from data.response_info import ResponseInfo
from data.metadata_info import MetadataInfo

class InvalidFormatApacheLogException(Exception):

    def __init__(self, line):
        super().__init__(f'The format of the line "{line}" is invalid.')

class ApacheLogParser:

    LOG_PATTERN = compile(
        r'(?P<ip>\S+) (?P<rfc>\S+) (?P<user>\S+)'
        r' \[?(?P<timestamp>.+?)\]? "((?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)|-)"'
        r' (?P<status>\d+) (?P<size>\S+)'
        r'\s?("(?P<referer>.*?)" "(?P<user_agent>.*?)")?'
    )

    def __init__(self, path: str):
        #Check if file exists
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Le fichier {path} est introuvable.")
        self.path = path

    def get_file_parsed(self):
        return self.__parse_file()

    def __parse_file(self) -> ApacheLogFile:
        #Check if file exists
        if not os.path.isfile(self.path):
            raise FileNotFoundError()
        #Get lines of the file
        log_file = ApacheLogFile(self.path)
        with open(self.path, 'r') as file:
            for line in file:
                log_file.add_entry(self.__parse_line(line))
        return log_file

    def __parse_line(self, line: str) -> ApacheLogEntry:
        #Analyse of the line
        match =  self.LOG_PATTERN.match(line)
        if not match:
            raise InvalidFormatApacheLogException()
        #Get the datas of the line
        datas_line = match.groupdict()
        #Get the information of the client
        client_ip = datas_line["ip"]
        rfc_id = datas_line["rfc"]
        remote_user = datas_line["user"]
        client_info = ClientInfo(client_ip, rfc_id, remote_user)
        #Get the information of the request of the client
        method = datas_line["method"]
        url = datas_line["url"]
        protocol = datas_line["protocol"]
        timestamp = datetime.strptime(datas_line["timestamp"], "%d/%b/%Y:%H:%M:%S %z") if datas_line["timestamp"] else None
        request_info = RequestInfo(method, url, protocol, timestamp)
        #Get the information of the response of the server
        status_code = int(datas_line["status"]) if datas_line["status"] != "-" else None
        response_size = int(datas_line["size"]) if datas_line["size"] != "-" else None
        response_info = ResponseInfo(status_code, response_size)
        #Get the metadatas of the request
        referer = datas_line["referer"]
        user_agent = datas_line["user_agent"]
        metadata_info = MetadataInfo(referer, user_agent)
        return ApacheLogEntry(client_info, request_info, response_info, metadata_info)
