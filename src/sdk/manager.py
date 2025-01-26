from typing import Dict, Tuple, Any
from openai import OpenAI
from anthropic import Anthropic


class SDKManager:
    _instances: Dict[Tuple, Any] = {}

    @classmethod
    def get_sdk(cls, api_type: str, base_url: str, api_key: str) -> Any:
        key = (api_type, base_url, api_key)
        if key not in cls._instances:
            if api_type == "openai":
                cls._instances[key] = OpenAI(
                    base_url=base_url if base_url != "NOTSET" else None, api_key=api_key
                )
            elif api_type == "anthropic":
                cls._instances[key] = Anthropic(
                    base_url=base_url if base_url != "NOTSET" else None, api_key=api_key
                )
        return cls._instances[key]
