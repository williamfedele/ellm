from abc import ABC, abstractmethod
import configparser
from message import Message
from typing import List, Dict, Any


class APIProvider(ABC):
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


class OpenAIAPI(APIProvider):
    def prepare_request(self, config, messages):
        pass

    def send_request(self, prepared_request):
        pass


class AnthropicAPI(APIProvider):
    def prepare_request(self, config, messages):
        pass

    def send_request(self, prepared_request):
        pass


PROVIDERS = {"openai": OpenAIAPI, "anthropic": AnthropicAPI}


def create_provider(api_type):
    provider_class = PROVIDERS.get(api_type)
    if not provider_class:
        return None
    return provider_class()
