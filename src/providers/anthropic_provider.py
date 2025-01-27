from .base import APIProvider


class AnthropicAPI(APIProvider):
    def prepare_request(self, config, messages):
        system_msg = ""

        anthropic_msgs = []
        for msg in messages:
            if msg.role == "system":
                system_msg = msg.content
            else:
                anthropic_msgs.append({"role": msg.role, "content": msg.content})

        request_params = {
            "model": config["model"],
            "max_tokens": int(config["max_tokens"]),
            "temperature": 0,
            "messages": anthropic_msgs,
            "system": system_msg,
        }
        return request_params

    def send_request(self, prepared_request) -> str:
        response = self.sdk.messages.create(**prepared_request)
        return response.content[0].text

    def send(self, config, messages) -> str:
        """Convenience method to prepare and send in one call"""
        prepared_request = self.prepare_request(config, messages)
        return self.send_request(prepared_request)
