"""
Tests for Rapid7 InsightVM UI module.

Tests the ui.py module for user interface utilities.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from rapid7.ui import Color, UI, SimpleProgressBar, create_ui


class TestColor:
    """Test Color enum."""

    def test_color_enum_values(self):
        """Test that Color enum has expected values."""
        assert Color.RESET.value == '\033[0m'
        assert Color.RED.value == '\033[91m'
        assert Color.GREEN.value == '\033[92m'
        assert Color.YELLOW.value == '\033[93m'
        assert Color.BLUE.value == '\033[94m'


class TestUI:
    """Test UI class functionality."""

    @pytest.fixture
    def ui_with_colors(self):
        """Create UI instance with colored output."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = True
            mock_config.return_value = config
            
            with patch('rapid7.ui.RICH_AVAILABLE', False):
                ui = UI()
                ui.colored = True
                return ui

    @pytest.fixture
    def ui_without_colors(self):
        """Create UI instance without colored output."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = False
            mock_config.return_value = config
            
            with patch('rapid7.ui.RICH_AVAILABLE', False):
                ui = UI()
                ui.colored = False
                return ui

    def test_ui_init(self):
        """Test UI initialization."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = True
            mock_config.return_value = config
            
            ui = UI()
            
            assert ui.config is not None
            assert hasattr(ui, 'colored')

    def test_print_success_with_colors(self, ui_with_colors, capsys):
        """Test printing success message with colors."""
        ui_with_colors.print_success("Test message")
        
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "✓" in captured.out

    def test_print_success_without_colors(self, ui_without_colors, capsys):
        """Test printing success message without colors."""
        ui_without_colors.print_success("Test message")
        
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "✓" in captured.out
        # Should not contain ANSI codes
        assert '\033[' not in captured.out

    def test_print_error_with_colors(self, ui_with_colors, capsys):
        """Test printing error message with colors."""
        ui_with_colors.print_error("Error message")
        
        captured = capsys.readouterr()
        assert "Error message" in captured.err
        assert "✗" in captured.err

    def test_print_error_without_colors(self, ui_without_colors, capsys):
        """Test printing error message without colors."""
        ui_without_colors.print_error("Error message")
        
        captured = capsys.readouterr()
        assert "Error message" in captured.err
        assert "✗" in captured.err
        assert '\033[' not in captured.err

    def test_print_warning_with_colors(self, ui_with_colors, capsys):
        """Test printing warning message with colors."""
        ui_with_colors.print_warning("Warning message")
        
        captured = capsys.readouterr()
        assert "Warning message" in captured.out
        assert "⚠" in captured.out

    def test_print_info_with_colors(self, ui_with_colors, capsys):
        """Test printing info message with colors."""
        ui_with_colors.print_info("Info message")
        
        captured = capsys.readouterr()
        assert "Info message" in captured.out
        assert "ℹ" in captured.out

    def test_print_header(self, ui_without_colors, capsys):
        """Test printing header."""
        ui_without_colors.print_header("Test Header")
        
        captured = capsys.readouterr()
        assert "Test Header" in captured.out
        assert "=" in captured.out

    def test_print_separator(self, ui_without_colors, capsys):
        """Test printing separator."""
        ui_without_colors.print_separator()
        
        captured = capsys.readouterr()
        assert "-" * 80 in captured.out

    def test_print_table(self, ui_without_colors, capsys):
        """Test printing table."""
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"]
        ]
        
        ui_without_colors.print_table("User Data", headers, rows)
        
        captured = capsys.readouterr()
        assert "User Data" in captured.out
        assert "Name" in captured.out
        assert "Alice" in captured.out
        assert "Bob" in captured.out

    def test_confirm_yes(self, ui_without_colors):
        """Test confirm prompt with yes answer."""
        with patch('builtins.input', return_value='y'):
            result = ui_without_colors.confirm("Continue?")
            assert result is True

    def test_confirm_no(self, ui_without_colors):
        """Test confirm prompt with no answer."""
        with patch('builtins.input', return_value='n'):
            result = ui_without_colors.confirm("Continue?")
            assert result is False

    def test_confirm_default(self, ui_without_colors):
        """Test confirm prompt with default value."""
        with patch('builtins.input', return_value=''):
            result = ui_without_colors.confirm("Continue?", default=True)
            assert result is True

    def test_prompt(self, ui_without_colors):
        """Test text prompt."""
        with patch('builtins.input', return_value='test value'):
            result = ui_without_colors.prompt("Enter value:")
            assert result == "test value"

    def test_prompt_with_default(self, ui_without_colors):
        """Test text prompt with default value."""
        with patch('builtins.input', return_value=''):
            result = ui_without_colors.prompt("Enter value:", default="default")
            assert result == "default"

    def test_select_menu(self, ui_without_colors):
        """Test selecting from a menu."""
        options = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='2'):
            result = ui_without_colors.select_menu("Choose:", options)
            assert result == 1  # Zero-indexed

    def test_progress_bar_creation(self, ui_without_colors):
        """Test creating a progress bar."""
        progress = ui_without_colors.progress_bar("Processing", total=100)
        
        assert progress is not None
        assert isinstance(progress, SimpleProgressBar)


class TestSimpleProgressBar:
    """Test SimpleProgressBar class."""

    @pytest.fixture
    def mock_ui(self):
        """Create a mock UI for SimpleProgressBar."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = True
            mock_config.return_value = config
            return UI()

    def test_simple_progress_bar_init(self, mock_ui):
        """Test SimpleProgressBar initialization."""
        progress = SimpleProgressBar("Test", total=100, ui=mock_ui)
        
        assert progress.description == "Test"
        assert progress.total == 100
        assert progress.current == 0

    def test_simple_progress_bar_context_manager(self, mock_ui, capsys):
        """Test SimpleProgressBar as context manager."""
        with SimpleProgressBar("Test", total=100, ui=mock_ui) as progress:
            progress.update(50)
        
        captured = capsys.readouterr()
        assert "Test" in captured.out
        assert "Done" in captured.out

    def test_simple_progress_bar_update(self, mock_ui, capsys):
        """Test updating progress bar."""
        with SimpleProgressBar("Test", total=100, ui=mock_ui) as progress:
            progress.update(50)
        
        captured = capsys.readouterr()
        assert "Test" in captured.out


class TestCreateUI:
    """Test create_ui helper function."""

    def test_create_ui_returns_ui_instance(self):
        """Test that create_ui returns a UI instance."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = True
            mock_config.return_value = config
            
            ui = create_ui()
            
            assert isinstance(ui, UI)
            assert hasattr(ui, 'print_success')
            assert hasattr(ui, 'print_error')


class TestUIWithRich:
    """Test UI class with rich library available."""

    @pytest.fixture
    def ui_with_rich(self):
        """Create UI instance with rich available."""
        with patch('rapid7.ui.get_config') as mock_config:
            config = Mock()
            config.get_preference.return_value = True
            mock_config.return_value = config
            
            with patch('rapid7.ui.RICH_AVAILABLE', True):
                with patch('rapid7.ui.Console') as mock_console_class:
                    mock_console = Mock()
                    mock_console_class.return_value = mock_console
                    
                    ui = UI()
                    ui.console = mock_console
                    return ui

    def test_print_success_with_rich(self, ui_with_rich):
        """Test printing success with rich."""
        ui_with_rich.print_success("Test message")
        
        # Verify console.print was called
        ui_with_rich.console.print.assert_called_once()
        call_args = ui_with_rich.console.print.call_args[0][0]
        assert "Test message" in call_args
        assert "[green]" in call_args

    def test_print_error_with_rich(self, ui_with_rich):
        """Test printing error with rich."""
        ui_with_rich.print_error("Error message")
        
        # Verify console.print was called with stderr
        ui_with_rich.console.print.assert_called_once()
        call_args = ui_with_rich.console.print.call_args[0][0]
        assert "Error message" in call_args
        assert "[red]" in call_args
