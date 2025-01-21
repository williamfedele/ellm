<br/><br/>
<div>
    <h3 align="center">💬 HERMES</h3>
    <p align="center">
      A simple CLI tool to interact and have conversations with LLM APIs from the terminal.
    </p>
</div>
<br><br>

_Work in progress_

## Getting Started
I'm currently using [uv](https://github.com/astral-sh/uv) for package management and script execution. It's a great alternative to the mess that is Python's tooling ecosystem.

Conversations are stored in `~/.hermes/conversations/{uuid4}.json`

Config files are stored in: `~/.hermes/config.ini`


### Configuration
The following default config is generated after running:

```yaml
[DEFAULT]
api_key = NOTSET
model = NOTSET
max_tokens = 1000
```

New conversations use the DEFAULT settings.

To modify any field, run the following with the option you want to modify:
```shell
uv run hermes.py default_config --api-key {APIKEY} --model {MODEL} --max-tokens {MAXTOKENS}
```

You can also specify additional models to be used by individual models:
```shell
uv run hermes.py add_config {NAME} --api-key {APIKEY} --model {MODEL} --max-tokens {MAXTOKENS}
```
This is helpful for optimizing API usage. For example: use Claude Sonnet for coding and Haiku for faster responses in simpler tasks.

## Chatting
```shell
uv run hermes.py
```

Possible commands:

- help: Help menu. You can also do `help <command>` for more information on other commands.
- history: Show message history for the active chat session.
- list: List all available chats.
- new: Start a new chat.
- title: Get session title: `title`. Set session title: `title <title_name>`.
- send: Send a message in the current session: `send <message>`.
- switch: Switch to a different session: `switch <session_id>`.
- settings: Show current settings: `settings`. Change settings: `settings <settings_name>`.
- tokens: Show token usage for the current session.
- quit: Exit the chat CLI.

## Future

I'm currently working on this for fun. It may or may not stay in Python. Depends on if I feel another ecosystem is more suitable for future requirements. Apart from letting me chat with the LLM of my choice from the terminal, I'd also like to be able to pass code blocks which is not possible at the moment.

## License

[MIT](https://github.com/williamfedele/hermes/blob/main/LICENSE)
