import argparse
from chatcli import ChatCLI


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    config_parser = subparsers.add_parser(
        "default_config", help="Configure default model settings"
    )
    config_parser.add_argument("--api-key", help="Set API key for your provider")
    config_parser.add_argument("--model", help="Set your model version")
    config_parser.add_argument("--max-tokens", help="Set max tokens")

    model_parser = subparsers.add_parser(
        "add_config", help="Add additional model settings"
    )
    model_parser.add_argument("name", help="Set the name for the model settings")
    model_parser.add_argument("--api-key", help="Set API key for your provider")
    model_parser.add_argument("--model", help="Set your model version")
    model_parser.add_argument("--max-tokens", help="Set max tokens")

    args = parser.parse_args()
    if args.action == "default_config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        ChatCLI().save_config(args_dict)
    elif args.action == "add_config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        del args_dict["name"]
        ChatCLI().save_config(args_dict, args.name)
    else:
        ChatCLI().cmdloop()


if __name__ == "__main__":
    main()
