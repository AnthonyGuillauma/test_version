

from data.client_info import ClientInfo
from data.request_info import RequestInfo
from data.response_info import ResponseInfo
from data.metadata_info import MetadataInfo

class ApacheLogEntry:
    """
    Class representing a single entry from an Apache access log.

    This class encapsulates a single line from the access.log file, extracting all its fields.

    Attributes:
        client_info (ClientInfo): 
        request_info (RequestInfo): 
        response_info (ResponseInfo): 
        metadata_info (MetadataInfo): 
    """

    def __init__(
        self,
        client_info: ClientInfo,
        request_info: RequestInfo,
        response_info: ResponseInfo,
        metadata_info: MetadataInfo
    ):
        """
        Initializes a new Apache log entry.

        Args:
            client_info (ClientInfo): 
            request_info (RequestInfo): 
            response_info (ResponseInfo): 
            metadata_info (MetadataInfo): 
        """
        self.client_info = client_info
        self.request_info = request_info
        self.response_info = response_info
        self.metadata_info = metadata_info