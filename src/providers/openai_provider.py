from .base import APIProvider


class OpenAIAPI(APIProvider):
    def prepare_request(self, config, messages):
        pass

    def send_request(self, prepared_request):
        pass
