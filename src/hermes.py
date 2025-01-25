import argparse
from chatcli import ChatCLI
from constants import CONFIG_PATH
from config import ConfigManager


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    model_parser = subparsers.add_parser("config", help="Add additional model settings")
    model_parser.add_argument("name", help="Set the name for the model settings")
    model_parser.add_argument("--endpoint", help="Set the endpoint for the provider")
    model_parser.add_argument("--api-key", help="Set your API key")
    model_parser.add_argument("--model", help="Set your model version")
    model_parser.add_argument("--max-tokens", help="Set max tokens")

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
                    if k == "api_key":
                        v = v[:5] + "-" * (len(v) - 5)
                    print(f" - {k} -> {v}")
    else:
        ChatCLI(CONFIG_PATH).cmdloop()


if __name__ == "__main__":
    main()
