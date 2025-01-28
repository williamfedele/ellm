<br/><br/>
<div>
    <h3 align="center">🌳 Ellm</h3>
    <p align="center">
      A simple CLI tool to interact and have conversations with LLM APIs from the terminal.
    </p>
</div>
<br><br>

_Work in progress_

## Getting Started
I'm currently using [uv](https://github.com/astral-sh/uv) for package management and execution. It's a great alternative to the mess that is Python's tooling ecosystem.

Conversations are stored in `~/.ellm/conversations/{uuid4}.json`

Config files are stored in: `~/.ellm/config.ini`

### Configuration
The following default config is generated after running:

```yaml
[DEFAULT]
base_url = NOTSET
api_key = NOTSET
model = NOTSET
api_type = openai
max_tokens = 1000
```

New conversations use the DEFAULT settings.

You can modify any field of the default settings using _DEFAULT_ as name in command below. You can also specify a new name to create a new config to be used on a conversation by conversation basis. This is helpful for optimizing API usage. For example: using Claude Sonnet for coding and Haiku for simpler tasks.
```shell
uv run ellm.py config NAME --base-url BASEURL --api-key APIKEY --model MODEL --api-type {openai, anthropic} --max-tokens MAXTOKENS
```
Examples:
```shell
uv run ellm.py config code --api-key 123abc --model claude-3-5-sonnet-20241022 --api-type anthropic --max-tokens 2048
```
```shell
uv run ellm.py config DeepSeekR1 --base-url https://api.deepseek.com --api-key cba321 --model deepseek-reasoner --api-type openai --max-tokens 4096
```

Omitting the base url will use the default from the providers SDK.

Omitting all fields will print that config.

## Running
```shell
uv run ellm.py
```

### Commands:

Commands are prefixed with slash. No leading slash will be interpreted as a message to be sent in the session.

- `/new`: Start a new chat.
- `/branch`: Create a new branched session from the current session.
- `/title`: Get session title: `title`. Set session title: `title <title_name>`.
- `/settings`: Show current settings: `settings`. Change settings: `settings <settings_name>`.
- `/list`: List all available chats.
- `/switch`: Switch to a different session: `switch <session_id>`.
- `/send`: Send a message in the current session: `send <message>`.
- `/history`: Show message history for the active chat session.
- `/tokens`: Show token usage for the current session.
- `/delete`: Delete a session: `/delete <session_id>`
- `/quit`: Exit the chat CLI.
- `/help`: Show available commands.


## Future

I'm currently working on this for fun.

### Plans:

- OpenAI API implementation
- Ability to pass in code blocks or files


## License

[MIT](https://github.com/williamfedele/ellm/blob/main/LICENSE)
