
from dataclasses import dataclass

@dataclass
class ResponseInfo:
    status_code: int
    response_size: int

    def get_status_code_class(self):
        if self.status_code >= 500:
            return "5xx"
        elif self.status_code >= 400:
            return "4xx"
        elif self.status_code >= 300:
            return "3xx"
        elif self.status_code >= 200:
            return "2xx"
        else:
            return "1xx"