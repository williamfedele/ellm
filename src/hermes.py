import argparse
from cli.chatcli import ChatCLI
from utils.constants import CONFIG_PATH
from config.manager import ConfigManager


def positive_int(value) -> str:
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
        return str(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    model_parser = subparsers.add_parser("config", help="Add additional model settings")
    model_parser.add_argument("name", help="Set the name for the model settings")
    model_parser.add_argument("--base-url", help="Set the base url for the provider")
    model_parser.add_argument("--api-key", help="Set your API key")
    model_parser.add_argument("--model", help="Set your model version")
    model_parser.add_argument(
        "--api-type",
        choices=["openai", "anthropic"],
        help="Set the api type (OpenAI API, AnthropicAPI, etc)",
    )
    model_parser.add_argument("--max-tokens", type=positive_int, help="Set max tokens")

    args = parser.parse_args()
    if args.action == "config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        del args_dict["name"]
        if args_dict:
            ConfigManager(CONFIG_PATH).save_config(args_dict, args.name)
        else:
            config = ConfigManager(CONFIG_PATH).get_config(args.name)
            if not config:
                print(f"No config named {args.name}")
            else:
                print(f"{args.name} config:")
                for k, v in config.items():
                    if k == "api_key" and v != "NOTSET":
                        v = v[:5] + "-" * (len(v) - 5)
                    print(f" - {k} -> {v}")
    else:
        ChatCLI(CONFIG_PATH).cmdloop()


if __name__ == "__main__":
    main()
