from .base import APIProvider


class AnthropicAPI(APIProvider):
    def prepare_request(self, config, messages):
        pass

    def send_request(self, prepared_request):
        pass
