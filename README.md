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
This project uses [uv](https://github.com/astral-sh/uv) for package management and execution.

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

- `base_url`: The endpoint for your provider.
- `api_key`: Your API key for authentication.
- `model`: The model to use for the conversation.
- `api_type`: The type of API (e.g., openai, anthropic).
- `max_tokens`: The maximum number of tokens for the response.

New conversations automatically use the DEFAULT settings.

You can modify any field of the default settings using `DEFAULT` as the name. You can also create a new config for specific conversations. This helps optimize API usage. For example, using Claude Sonnet for coding and gpt-o3-mini for other tasks.

```shell
uv run ellm config NAME --base-url BASEURL --api-key APIKEY --model MODEL --api-type {openai, anthropic} --max-tokens MAXTOKENS
```

Omitting the base URL will use the default from the provider's SDK. Omitting all fields will print the config.

### Examples:
```shell
uv run ellm config code --api-key 123abc --model claude-3-5-sonnet-20241022 --api-type anthropic --max-tokens 2048
```
```shell
uv run ellm config DeepSeekR1 --base-url https://api.deepseek.com --api-key cba321 --model deepseek-reasoner --api-type openai --max-tokens 4096
```

Ollama:

Ollama has experiment compatibility with the OpenAI API. Make sure Ollama is running on your machine with your model downloaded. Use `http://localhost:11434/v1/` as the base url. The api key is mandatory, but is ignored (you can put anything). Select the model name as it appears in `ollama list`.
```shell
uv run ellm config ollama --base-url http://localhost:11434/v1/ --api-key ollama --model llama3.2:latest
```

## Running
```shell
uv run ellm
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

- Ability to pass in code blocks or files


## License

[MIT](https://github.com/williamfedele/ellm/blob/main/LICENSE)
