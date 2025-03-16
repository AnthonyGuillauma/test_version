
from typing import Optional
from user_agents.parsers import parse

class MetadataInfo:

    def __init__(self, referer: Optional[str], user_agent: Optional[str]):
        self.referer = referer
        self.user_agent = parse(user_agent) if user_agent else None

    def get_os(self) -> Optional[str]:
        if self.user_agent:
            return self.user_agent.os.family
        return None
    
    def get_browser(self) -> Optional[str]:
        if self.user_agent:
            return self.user_agent.browser.family
        return None
    
    def get_type_device(self) -> Optional[str]:
        if self.user_agent:
            if self.user_agent.is_pc:
                return "PC"
            elif self.user_agent.is_tablet:
                return "Tablet"
            elif self.user_agent.is_mobile:
                return "Mobile"
            else:
                return "Other"
        return None
    
    def is_bot(self) -> Optional[bool]:
        if self.user_agent:
            return self.user_agent.is_bot
        return None