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
        }

    def send_request(self, prepared_request):
        response = self.sdk.chat.completions.create(**prepared_request)
        return response.choices[0].message.content

    def send(self, config, messages) -> str:
        """Convenience method to prepare and send in one call"""
        prepared_request = self.prepare_request(config, messages)
        return self.send_request(prepared_request)
