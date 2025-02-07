from .base import APIProvider


class OpenAIAPI(APIProvider):
    def prepare_request(self, config, messages):
        # Strip timestamp and token info from messages
        stripped_messages = []
        for msg in messages:
            stripped_messages.append({"role": msg.role, "content": msg.content})

        return {
            "model": config["model"],
            "max_tokens": int(config["max_tokens"]),
            "temperature": 0,
            "messages": stripped_messages,
            "stream": True,
        }

    def send_request(self, prepared_request):
        try:
            response = self.sdk.chat.completions.create(**prepared_request)
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None
        return response

    def send(self, config, messages) -> str:
        """Convenience method to prepare and send in one call"""
        prepared_request = self.prepare_request(config, messages)
        return self.send_request(prepared_request)
