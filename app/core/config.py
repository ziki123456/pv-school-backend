from pathlib import Path
import yaml


class ConfigError(Exception):
    pass


class AppConfig:
    def __init__(self, config_path: Path):
        if not config_path.exists():
            raise ConfigError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._validate(data)
        self.db = data["db"]
        self.app = data["app"]

    @staticmethod
    def _validate(data: dict):
        if not isinstance(data, dict):
            raise ConfigError("Config file must contain a YAML mapping")

        for section in ("db", "app"):
            if section not in data:
                raise ConfigError(f"Missing '{section}' section in config")

        for key in ("host", "port", "database", "user", "password"):
            if key not in data["db"]:
                raise ConfigError(f"Missing db.{key} in config")

        for key in ("host", "port"):
            if key not in data["app"]:
                raise ConfigError(f"Missing app.{key} in config")
