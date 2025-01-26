import configparser
from .openai_provider import OpenAIAPI
from .anthropic_provider import AnthropicAPI

PROVIDERS = {"openai": OpenAIAPI, "anthropic": AnthropicAPI}


class ProviderManager:
    _instances = {}

    @classmethod
    def get_provider(cls, config: configparser.ConfigParser):
        key = (config["api_type"], config["base_url"], config["api_key"])
        if key not in cls._instances:
            provider_class = PROVIDERS.get(config["api_type"], OpenAIAPI)
            cls._instances[key] = provider_class(config)
        return cls._instances[key]
