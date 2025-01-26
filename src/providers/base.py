from abc import ABC, abstractmethod
from typing import List, Dict, Any
import configparser
from models.message import Message
from sdk.manager import SDKManager


class APIProvider(ABC):
    def __init__(self, config: configparser.ConfigParser):
        self.sdk = SDKManager.get_sdk(
            config["api_type"], config["base_url"], config["api_key"]
        )

    @abstractmethod
    def prepare_request(
        self, config: configparser.ConfigParser, messages: List[Message]
    ) -> Dict[str, Any]:
        """Prepare request for specific API provider"""
        pass

    @abstractmethod
    def send_request(self, prepared_request: Dict[str, Any]) -> str:
        """Send request and return response"""
        pass
