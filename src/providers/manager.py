import configparser
from .base import APIProvider
from .openai_provider import OpenAIAPI
from .anthropic_provider import AnthropicAPI
from typing import Tuple, Dict

PROVIDERS = {"openai": OpenAIAPI, "anthropic": AnthropicAPI}


class ProviderManager:
    _instances: Dict[Tuple, APIProvider] = {}

    @classmethod
    def get_provider(cls, config: configparser.ConfigParser) -> APIProvider:
        key = (str(config["api_type"]), str(config["base_url"]), str(config["api_key"]))
        if key not in cls._instances:
            provider_class = PROVIDERS.get(str(config["api_type"]))
            if provider_class is None:
                raise ValueError(f"API type {config['api_type']} is not supported")
            cls._instances[key] = provider_class(config)
        return cls._instances[key]
