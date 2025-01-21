<br/><br/>
<div>
    <h3 align="center">💬 Hermes</h3>
    <p align="center">
      A simple CLI tool to interact and have conversations with LLM APIs from the terminal.
    </p>
</div>
<br><br>

_Work in progress: the following is in development state._

## Getting Started
I'm currently using [uv](https://github.com/astral-sh/uv) for package management and script execution. It's a great alternative to the mess that is Python's tooling ecosystem.

Conversations are stored in `~/.hermes/conversations/{uuid4}.json`

Config files are stored in: `~/.hermes/config.ini`


### Configuration
The following default config is generated after running:

```yaml
[DEFAULT]
api_key =
model =
max_tokens = 1000
```

To modify any field, run the following with the option you want to modify:
```shell
uv run hermes.py config --api-key {APIKEY} --model {MODEL} --max-tokens {MAXTOKENS}
```

## Chatting
```shell
uv run hermes.py
```

Possible commands:

- help: Help menu. You can also do `help <command>` for more information on other commands.
- history: Show message history for the active chat session.
- list: List all available chats.
- new: Start a new chat.
- send: Send a message in the current session: `send <message>`
- switch: Switch to a different session: `switch <session_id>`
- quit: Exit the chat CLI

## Future

I'm currently working on this for fun. It may or may not stay in Python. Depends on if I feel another ecosystem is more suitable for future requirements. Apart from letting me chat with the LLM of my choice from the terminal, I'd also like to be able to pass code blocks which is not possible at the moment.

## License

[MIT](https://github.com/williamfedele/hermes/blob/main/LICENSE)
