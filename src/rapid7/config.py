"""
Configuration management for InsightVM tools.

This module provides persistent configuration storage for user preferences,
last-used values, and tool settings. Configuration is stored in JSON format
in the user's home directory.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """
    Manages persistent configuration for InsightVM tools.

    Configuration is stored in ~/.insightvm/config.json and includes:
    - Tool-specific defaults
    - Last-used values
    - User preferences
    - Output formatting options
    """

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_dir: Optional custom config directory path.
                       Defaults to ~/.insightvm
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / '.insightvm'

        self.config_file = self.config_dir / 'config.json'
        self.state_dir = self.config_dir / 'state'

        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Load existing config or create default
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.

        Returns:
            Configuration dictionary
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config: {e}")
                return self._default_config()
        else:
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """
        Create default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            'version': '2.0.0',
            'preferences': {
                'confirm_destructive_operations': True,
                'colored_output': True,
                'show_progress_bars': True,
                'verbose': False
            },
            'tools': {
                'sonar_queries': {
                    'last_csv_path': '',
                    'default_days': 30,
                    'last_output_path': ''
                },
                'insight_agent': {
                    'last_installer_path': '',
                    'last_token': ''  # Note: Should be encrypted in production
                },
                'scan_assistant': {
                    'last_certificate': '',
                    'package_manager': ''
                }
            }
        }

    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path
                     (e.g., 'tools.sonar_queries.default_days')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> config = Config()
            >>> config.get('preferences.colored_output', True)
            True
        """
        keys = key_path.split('.')
        value = self.data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key_path: Dot-separated path
                     (e.g., 'tools.sonar_queries.default_days')
            value: Value to set

        Example:
            >>> config = Config()
            >>> config.set('tools.sonar_queries.default_days', 7)
            >>> config.save()
        """
        keys = key_path.split('.')
        data = self.data

        # Navigate to the parent dictionary
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]

        # Set the value
        data[keys[-1]] = value

    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool configuration dictionary
        """
        return self.get(f'tools.{tool_name}', {})

    def set_tool_config(self, tool_name: str, config: Dict[str, Any]) -> None:
        """
        Set configuration for a specific tool.

        Args:
            tool_name: Name of the tool
            config: Configuration dictionary
        """
        if 'tools' not in self.data:
            self.data['tools'] = {}
        self.data['tools'][tool_name] = config

    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get user preference value.

        Args:
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value or default
        """
        return self.get(f'preferences.{key}', default)

    def set_preference(self, key: str, value: Any) -> None:
        """
        Set user preference value.

        Args:
            key: Preference key
            value: Preference value
        """
        self.set(f'preferences.{key}', value)

    def save_state(self, tool_name: str, state: Dict[str, Any]) -> None:
        """
        Save operation state for resumable operations.

        Args:
            tool_name: Name of the tool
            state: State dictionary to save
        """
        state_file = self.state_dir / f'{tool_name}_state.json'
        try:
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state: {e}")

    def load_state(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Load operation state for resumable operations.

        Args:
            tool_name: Name of the tool

        Returns:
            State dictionary or None if not found
        """
        state_file = self.state_dir / f'{tool_name}_state.json'
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state: {e}")
        return None

    def clear_state(self, tool_name: str) -> None:
        """
        Clear saved state for a tool.

        Args:
            tool_name: Name of the tool
        """
        state_file = self.state_dir / f'{tool_name}_state.json'
        if state_file.exists():
            try:
                state_file.unlink()
            except IOError as e:
                print(f"Warning: Could not clear state: {e}")

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.data = self._default_config()
        self.save()


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get or create global configuration instance.

    Returns:
        Global Config instance
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
