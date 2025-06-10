import os
import toml
import warnings
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Config:
    def __init__(self, config_file: str = "config.toml"):
        # Load the TOML config
        with open(config_file, "r") as f:
            self._config = toml.load(f)

        # Override with environment variables where they exist
        self._override_with_env()

        # Validate essential config values
        self._validate()

    def _override_with_env(self):
        """Override config values with environment variables if they exist."""

        self._config.setdefault("api", {})
        self._config.setdefault("app", {})

        # API settings
        if os.getenv("OPENROUTER_API_KEY"):
            self._config["api"]["api_key"] = os.getenv("OPENROUTER_API_KEY")

        if os.getenv("API_BASE_URL"):
            self._config["api"]["base_url"] = os.getenv("API_BASE_URL")

        if os.getenv("API_TEMPERATURE"):
            self._config["api"]["temperature"] = float(os.getenv("API_TEMPERATURE"))

        if os.getenv("API_MAX_TOKENS"):
            self._config["api"]["max_tokens"] = int(os.getenv("API_MAX_TOKENS"))

        # App settings
        if os.getenv("LLM_MODEL"):
            self._config["app"]["model"] = os.getenv("LLM_MODEL")

        if os.getenv("SYSTEM_PROMPT"):
            self._config["app"]["system_prompt"] = os.getenv("SYSTEM_PROMPT")

    def _validate(self):
        required = {
            "api": ["api_key", "base_url"],
            "app": ["model", "system_prompt"],
        }
        for section, keys in required.items():
            for key in keys:
                if key not in self._config.get(section, {}):
                    warnings.warn(f"Missing required config: [{section}] {key}")

    def get(self, section: str, key: str = None, default=None):
        if key is None:
            return self._config.get(section, default)
        return self._config.get(section, {}).get(key, default)

    def get_nested(self, *keys, default=None):
        val = self._config
        for key in keys:
            val = val.get(key, {})
        return val or default

    @property
    def app(self):
        return self._config.get("app", {})

    @property
    def api(self):
        return self._config.get("api", {})

    @property
    def ui(self):
        return self._config.get("ui", {})

    @property
    def chat(self):
        return self._config.get("chat", {})

    @property
    def sidebar(self):
        return self._config.get("sidebar", {})

    @property
    def labels(self):
        return self._config.get("labels", {})

    @property
    def messages(self):
        return self._config.get("messages", {})

    @property
    def prompts(self):
        return self._config.get("prompts", {})

    @property
    def styles(self):
        return self._config.get("styles", {})


# Global config instance
config = Config()
