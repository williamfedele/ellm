from .base import APIProvider


class AnthropicAPI(APIProvider):
    def prepare_request(self, config, messages):
        # Anthropic API requires a system message to be passed in the request
        system_msg = ""

        # Find system message and strip timestamp and token info from other messages
        stripped_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                stripped_messages.append({"role": msg.role, "content": msg.content})

        return {
            "model": config["model"],
            "max_tokens": int(config["max_tokens"]),
            "temperature": 0,
            "messages": stripped_messages,
            "system": system_msg,
            "stream": True,
        }

    def send_request(self, prepared_request) -> str:
        try:
            response = self.sdk.messages.create(**prepared_request)
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None
        return response

    def send(self, config, messages) -> str:
        """Convenience method to prepare and send in one call"""
        prepared_request = self.prepare_request(config, messages)
        return self.send_request(prepared_request)
