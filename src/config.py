from typing import List, Dict
import configparser


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.configs: configparser.ConfigParser = self._load_configs()

    def _load_configs(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()

        if self.config_file_path.exists():
            config.read(self.config_file_path)
        else:
            config["DEFAULT"] = {
                "base_url": "NOTSET",
                "api_key": "NOTSET",
                "model": "NOTSET",
                "api_type": "openai",
                "max_tokens": "1000",
            }
            self.config_file_path.parent.mkdir(exist_ok=True)
            with open(self.config_file_path, "w") as f:
                config.write(f)

        return config

    def save_config(self, config_opts: Dict[str, str], settings_name: str) -> None:
        if settings_name not in self.configs:
            self.configs[settings_name] = {
                "base_url": "NOTSET",
                "api_key": "NOTSET",
                "model": "NOTSET",
                "api_type": "openai",
                "max_tokens": "1000",
            }

        for k, v in config_opts.items():
            self.configs[settings_name][k] = v

        self.config_file_path.parent.mkdir(exist_ok=True)
        with open(self.config_file_path, "w") as f:
            self.configs.write(f)

    def get_config(self, name):
        if name not in self.configs:
            return None

        return self.configs[name]

    def get_config_names(self) -> List[str]:
        return self.configs.keys()
