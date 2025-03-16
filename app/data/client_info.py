
from typing import Optional
from dataclasses import dataclass

@dataclass
class ClientInfo:
    client_ip: Optional[str]
    rfc_id: Optional[str]
    remote_user: Optional[str]