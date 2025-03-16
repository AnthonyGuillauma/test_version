
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RequestInfo:
    method: str
    url: str
    protocol: str
    timestamp: Optional[datetime]