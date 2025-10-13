"""
Tests for Rapid7 InsightVM config module.

Tests the config.py module for persistent configuration management.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile
import shutil

from rapid7.config import Config, get_config


class TestConfig:
    """Test Config class functionality."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary config directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_init_creates_directories(self, temp_config_dir):
        """Test that Config creates necessary directories."""
        config = Config(config_dir=temp_config_dir)
        
        assert config.config_dir.exists()
        assert config.state_dir.exists()
        assert config.config_dir == Path(temp_config_dir)

    def test_init_with_default_directory(self):
        """Test that Config uses default directory when not specified."""
        with patch('pathlib.Path.mkdir'):
            with patch('pathlib.Path.exists', return_value=False):
                config = Config()
                
                expected_dir = Path.home() / '.insightvm'
                assert config.config_dir == expected_dir

    def test_default_config_structure(self, temp_config_dir):
        """Test that default configuration has expected structure."""
        config = Config(config_dir=temp_config_dir)
        
        # Check top-level keys
        assert 'version' in config.data
        assert 'preferences' in config.data
        assert 'tools' in config.data
        
        # Check preferences
        prefs = config.data['preferences']
        assert 'confirm_destructive_operations' in prefs
        assert 'colored_output' in prefs
        assert 'show_progress_bars' in prefs
        assert 'verbose' in prefs
        
        # Check tools
        tools = config.data['tools']
        assert 'sonar_queries' in tools
        assert 'insight_agent' in tools
        assert 'scan_assistant' in tools

    def test_save_config(self, temp_config_dir):
        """Test saving configuration to file."""
        config = Config(config_dir=temp_config_dir)
        config.data['preferences']['verbose'] = True
        
        config.save()
        
        # Verify file was created
        assert config.config_file.exists()
        
        # Verify content
        with open(config.config_file, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data['preferences']['verbose'] is True

    def test_load_existing_config(self, temp_config_dir):
        """Test loading existing configuration from file."""
        # Create a config file
        config_file = Path(temp_config_dir) / 'config.json'
        config_data = {
            'version': '2.0.0',
            'preferences': {'verbose': True},
            'tools': {}
        }
        
        Path(temp_config_dir).mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        # Load config
        config = Config(config_dir=temp_config_dir)
        
        assert config.data['preferences']['verbose'] is True

    def test_get_preference(self, temp_config_dir):
        """Test getting a preference value."""
        config = Config(config_dir=temp_config_dir)
        
        value = config.get_preference('colored_output')
        assert value is True
        
        # Test with default value
        value = config.get_preference('nonexistent', default=False)
        assert value is False

    def test_set_preference(self, temp_config_dir):
        """Test setting a preference value."""
        config = Config(config_dir=temp_config_dir)
        
        config.set_preference('verbose', True)
        assert config.data['preferences']['verbose'] is True

    def test_get_tool_config(self, temp_config_dir):
        """Test getting tool configuration."""
        config = Config(config_dir=temp_config_dir)
        
        sonar_config = config.get_tool_config('sonar_queries')
        assert sonar_config is not None
        assert 'default_days' in sonar_config
        assert sonar_config['default_days'] == 30

    def test_set_tool_config(self, temp_config_dir):
        """Test setting tool configuration."""
        config = Config(config_dir=temp_config_dir)
        
        new_config = {'custom_setting': 'value'}
        config.set_tool_config('custom_tool', new_config)
        
        assert 'custom_tool' in config.data['tools']
        assert config.data['tools']['custom_tool']['custom_setting'] == 'value'

    def test_save_state(self, temp_config_dir):
        """Test saving tool state."""
        config = Config(config_dir=temp_config_dir)
        
        state_data = {'progress': 50, 'last_item': 'item_123'}
        config.save_state('test_tool', state_data)
        
        state_file = config.state_dir / 'test_tool_state.json'
        assert state_file.exists()
        
        with open(state_file, 'r') as f:
            saved_state = json.load(f)
        
        assert saved_state['progress'] == 50
        assert saved_state['last_item'] == 'item_123'

    def test_load_state(self, temp_config_dir):
        """Test loading tool state."""
        config = Config(config_dir=temp_config_dir)
        
        # Save state first
        state_data = {'progress': 75}
        config.save_state('test_tool', state_data)
        
        # Load state
        loaded_state = config.load_state('test_tool')
        
        assert loaded_state is not None
        assert loaded_state['progress'] == 75

    def test_load_state_nonexistent(self, temp_config_dir):
        """Test loading state that doesn't exist."""
        config = Config(config_dir=temp_config_dir)
        
        state = config.load_state('nonexistent_tool')
        assert state is None

    def test_clear_state(self, temp_config_dir):
        """Test clearing tool state."""
        config = Config(config_dir=temp_config_dir)
        
        # Save state
        config.save_state('test_tool', {'data': 'test'})
        state_file = config.state_dir / 'test_tool_state.json'
        assert state_file.exists()
        
        # Clear state
        config.clear_state('test_tool')
        assert not state_file.exists()

    def test_load_config_with_json_error(self, temp_config_dir):
        """Test handling of corrupted JSON config file."""
        config_file = Path(temp_config_dir) / 'config.json'
        Path(temp_config_dir).mkdir(parents=True, exist_ok=True)
        
        # Write invalid JSON
        with open(config_file, 'w') as f:
            f.write('{ invalid json }')
        
        # Should fall back to default config
        config = Config(config_dir=temp_config_dir)
        assert 'version' in config.data
        assert config.data['version'] == '2.0.0'


class TestGetConfig:
    """Test get_config helper function."""

    def test_get_config_singleton(self):
        """Test that get_config returns a singleton instance."""
        config1 = get_config()
        config2 = get_config()
        
        # Should return the same instance
        assert config1 is config2

    def test_get_config_returns_config_instance(self):
        """Test that get_config returns a Config instance."""
        config = get_config()
        
        assert isinstance(config, Config)
        assert hasattr(config, 'data')
        assert hasattr(config, 'save')
        assert hasattr(config, 'get_preference')
