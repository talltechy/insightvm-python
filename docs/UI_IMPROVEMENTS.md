# UI and Data Persistence Improvements

This document describes the comprehensive improvements made to user interface, menus, and data persistence throughout the InsightVM-Python tools.

## Overview

The InsightVM-Python tools have been enhanced with:
- **Persistent Configuration System**: Saves user preferences and last-used values
- **Interactive Menu Framework**: Rich UI with colored output and progress indicators
- **Enhanced Tool Interfaces**: All tools now support both CLI and interactive modes
- **Better User Experience**: Confirmation prompts, preview modes, and helpful defaults

## New Components

### 1. Configuration System (`src/rapid7/config.py`)

A comprehensive configuration management system that persists user settings between runs.

**Features:**
- Stores configuration in `~/.insightvm/config.json`
- Saves tool-specific defaults (CSV paths, days filters, etc.)
- Manages user preferences (colors, confirmations, progress bars)
- Supports resumable operations with state files
- Dot-notation access (e.g., `config.get('tools.sonar_queries.default_days')`)

**Configuration Structure:**
```json
{
  "version": "2.0.0",
  "preferences": {
    "confirm_destructive_operations": true,
    "colored_output": true,
    "show_progress_bars": true,
    "verbose": false
  },
  "tools": {
    "sonar_queries": {
      "last_csv_path": "/path/to/targets.csv",
      "default_days": 30,
      "last_output_path": "/path/to/results.csv"
    },
    "insight_agent": {
      "last_installer_path": "",
      "last_token": ""
    },
    "scan_assistant": {
      "last_certificate": "",
      "package_manager": ""
    }
  }
}
```

**Usage Example:**
```python
from src.rapid7.config import get_config

config = get_config()

# Get a value
days = config.get('tools.sonar_queries.default_days', 30)

# Set a value
config.set('tools.sonar_queries.default_days', 7)
config.save()

# Get tool-specific config
tool_config = config.get_tool_config('sonar_queries')

# Save operation state for resumable operations
config.save_state('my_tool', {'step': 3, 'items': [1, 2, 3]})

# Load state later
state = config.load_state('my_tool')
```

### 2. UI Utilities (`src/rapid7/ui.py`)

A rich user interface framework with fallback support for environments without the `rich` library.

**Features:**
- **Colored Output**: Green for success, red for errors, yellow for warnings, blue for info
- **Progress Bars**: Visual feedback for long-running operations
- **Interactive Menus**: Numbered selection menus with back navigation
- **Confirmation Prompts**: Yes/no questions with smart defaults
- **Formatted Tables**: Pretty-print data in tables
- **Headers and Separators**: Visual organization

**Usage Examples:**

```python
from src.rapid7.ui import create_ui

ui = create_ui()

# Print colored messages
ui.print_success("Operation completed successfully!")
ui.print_error("Failed to connect to server")
ui.print_warning("This action cannot be undone")
ui.print_info("Processing 100 items...")

# Headers and sections
ui.print_header("Main Menu")
ui.print_separator()

# Confirmation prompts
if ui.confirm("Proceed with deletion?", default=False):
    # Delete items
    pass

# User input with defaults
name = ui.prompt("Enter your name", default="John Doe")
csv_path = ui.prompt("Enter CSV file path")

# Selection menus
options = ["Create Query", "List Queries", "Delete Query", "Exit"]
choice = ui.select_menu("Sonar Query Manager", options)
if choice is not None:
    print(f"You selected: {options[choice]}")
else:
    print("User went back")

# Progress bars
with ui.progress_bar("Processing items", total=100) as progress:
    for i in range(100):
        # Do work
        progress.update(1)

# Tables
ui.print_table(
    "Query Results",
    headers=["Target", "Status", "Query ID"],
    rows=[
        ["example.com", "success", "12345"],
        ["test.org", "success", "12346"],
        ["bad-target", "error", "N/A"]
    ]
)
```

## Enhanced Tools

### 3. create_sonar_queries.py - ENHANCED ✨

The Sonar Query creation tool now supports interactive mode with persistent configuration.

**New Features:**

#### Interactive Mode
Run without arguments to enter interactive mode:
```bash
python src/rapid7/tools/create_sonar_queries.py
```

**Interactive Workflow:**
1. Remembers last-used CSV file path
2. Saves default days filter setting
3. Suggests output file path
4. Shows preview before execution
5. Requires confirmation before proceeding
6. Displays colored progress and results
7. Saves all settings for next run

#### CLI Mode (Unchanged)
Traditional command-line mode still works:
```bash
# With defaults
python src/rapid7/tools/create_sonar_queries.py targets.csv

# With custom days
python src/rapid7/tools/create_sonar_queries.py targets.csv --days 7

# With custom output
python src/rapid7/tools/create_sonar_queries.py targets.csv --output results.csv

# Force interactive mode
python src/rapid7/tools/create_sonar_queries.py --interactive
```

**Configuration Persistence:**
- Last CSV file path is remembered
- Default days setting is saved
- Output path preferences are stored
- Settings persist across runs

**UI Enhancements:**
- ✓ Green checkmarks for successful operations
- ✗ Red X marks for errors  
- ⚠ Yellow warnings for potential issues
- ℹ Blue info messages
- Formatted summary table at completion

### 4. install_insight_agent.py - Ready for Enhancement

Template for future enhancement with:
- Interactive installer selection
- Token management with encrypted storage
- Confirmation before installation
- Post-install verification menu
- Configuration persistence

### 5. install_scan_assistant.py - Ready for Enhancement

Template for future enhancement with:
- Main menu (install, verify, configure, uninstall)
- Certificate management
- Progress indicators for downloads
- Configuration preview
- Installation status tracking

## Benefits

### For Users

1. **Reduced Repetition**: Never re-enter the same CSV path or settings
2. **Better Defaults**: Tools remember your preferences
3. **Clear Feedback**: Colored output makes success/failure obvious
4. **Safer Operations**: Confirmation prompts prevent mistakes
5. **Progress Visibility**: Know what's happening during long operations
6. **Easier Navigation**: Menu systems for complex workflows

### For Developers

1. **Reusable Components**: Config and UI modules work across all tools
2. **Consistent Patterns**: Same UI/UX across different tools
3. **Easy Testing**: Graceful fallback when `rich` isn't available
4. **Maintainable Code**: Centralized configuration management
5. **Extensible**: Easy to add new tools with same patterns

## Migration Guide

### Updating Existing Tools

To add UI improvements to an existing tool:

```python
# 1. Import new modules
from src.rapid7.config import get_config
from src.rapid7.ui import create_ui

# 2. Create instances
config = get_config()
ui = create_ui()

# 3. Load tool configuration
tool_config = config.get_tool_config('my_tool')
last_value = tool_config.get('last_setting', 'default')

# 4. Use UI for prompts
value = ui.prompt("Enter value", default=last_value)

# 5. Save configuration
config.set('tools.my_tool.last_setting', value)
config.save()

# 6. Use colored output
ui.print_success("Operation completed!")
```

### Adding Interactive Mode

```python
def interactive_mode():
    """Run in interactive mode."""
    config = get_config()
    ui = create_ui()
    
    ui.print_header("My Tool - Interactive Mode")
    
    # Get settings with smart defaults
    tool_config = config.get_tool_config('my_tool')
    setting = ui.prompt(
        "Enter setting",
        default=tool_config.get('last_setting', 'default')
    )
    
    # Confirm before proceeding
    if not ui.confirm("Proceed?", default=True):
        ui.print_warning("Operation cancelled")
        return 0
    
    # Save settings
    config.set('tools.my_tool.last_setting', setting)
    config.save()
    
    # Do work with progress
    with ui.progress_bar("Processing", total=10) as progress:
        for i in range(10):
            # Work here
            progress.update(1)
    
    ui.print_success("Complete!")
    return 0

def main():
    # Run interactive if no arguments
    if len(sys.argv) == 1:
        sys.exit(interactive_mode())
    
    # Otherwise parse CLI arguments
    parser = argparse.ArgumentParser(...)
    # ...
```

## Configuration File Locations

- **Main Config**: `~/.insightvm/config.json`
- **State Files**: `~/.insightvm/state/<tool_name>_state.json`
- **Automatic Creation**: Directories created automatically on first run

## Dependencies

### Required
- `requests` - HTTP communication
- `python-dotenv` - Environment variables
- `pandas` - Data processing (for CSV tools)

### Optional but Recommended
- `rich` - Enhanced UI with colors, tables, progress bars
  - **Graceful Fallback**: Tools work without `rich`, just less pretty
  - **Install**: `pip install rich>=13.0.0`

## Future Enhancements

### Planned Features

1. **Operation History Database** (SQLite)
   - Track all operations
   - Searchable history
   - Repeat previous operations
   - Audit trail

2. **Unified Tool Launcher**
   - Main menu for all tools
   - Consistent navigation
   - Shared configuration
   - Help system

3. **Dry-Run Mode**
   - Preview before execution
   - Validate inputs
   - Estimate time/resources
   - Rollback support

4. **Enhanced Logging**
   - Structured logging
   - Log levels (DEBUG, INFO, WARN, ERROR)
   - Log file rotation
   - Remote logging support

5. **Multi-Language Support**
   - Internationalization (i18n)
   - Configurable language
   - Translated messages

## Troubleshooting

### Configuration Issues

**Problem**: Config file corrupted or missing
```python
from src.rapid7.config import get_config

config = get_config()
config.reset()  # Reset to defaults
config.save()
```

**Problem**: Old config format
- Delete `~/.insightvm/config.json`
- Restart tool to create new config

### UI Issues

**Problem**: Colors not showing
- Check `config.json`: `"colored_output": true`
- Or set preference: `config.set_preference('colored_output', True)`

**Problem**: Progress bars not appearing
- Check `config.json`: `"show_progress_bars": true`
- Or install rich: `pip install rich`

### Tool-Specific Issues

**Problem**: Tool doesn't remember settings
- Check config file exists: `~/.insightvm/config.json`
- Check tool name matches in `tools` section
- Verify `config.save()` is called after setting values

## Examples

See `docs/EXAMPLES.md` for complete working examples of:
- Using configuration system
- Building interactive menus
- Creating progress indicators
- Handling user input
- Saving and loading state

## Contributing

When adding new tools or features:

1. Use `get_config()` for persistent settings
2. Use `create_ui()` for user interaction  
3. Add tool configuration section in default config
4. Support both interactive and CLI modes
5. Save user preferences after operations
6. Use colored output for feedback
7. Add confirmation for destructive operations
8. Document new features in this file

## Version History

### v2.1.0 (October 7, 2025)
- ✨ Added persistent configuration system
- ✨ Added UI utilities framework
- ✨ Enhanced create_sonar_queries.py with interactive mode
- ✨ Added colored output and progress bars
- ✨ Added confirmation prompts
- 📝 Updated requirements.txt
- 📝 Created comprehensive documentation

### v2.0.0 (October 7, 2025)
- 🎉 Major architecture refactoring
- ✅ Modern authentication with HTTPBasicAuth
- ✅ Unified client interface
- ✅ Modular API design
