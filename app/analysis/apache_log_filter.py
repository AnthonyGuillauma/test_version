
from datetime import datetime
from parse.apache_log_entry import ApacheLogEntry


class ApacheLogFilter:

    def __init__(self, status_code: int, 
                 timestamp: datetime, 
                 client_ip: str, 
                 request_method: str):
        self.filter_status_code = status_code
        self.filter_timestamp = timestamp
        self.filter_client_ip = client_ip
        self.filter_request_method = request_method

    def pass_filter(self, entry: ApacheLogEntry) -> bool:
        if self.filter_status_code:
            if self.filter_status_code != entry.response_info.status_code:
                return False
        if self.filter_timestamp:
            if self.filter_timestamp != entry.request_info.timestamp:
                return False
        if self.filter_client_ip:
            if self.filter_client_ip != entry.client_info.client_ip:
                return False
        if self.filter_request_method:
            if self.filter_request_method != entry.request_info.method:
                return False
        return True
    
    def to_dict(self):
        return {
            "status_code": self.filter_status_code,
            "timestamp": self.filter_timestamp,
            "client_ip": self.filter_client_ip,
            "request_method": self.filter_request_method
        }