#!/usr/bin/env python3
"""
Install Rapid7 Insight Agent

This tool provides interactive installation of the Rapid7 Insight Agent
with support for configuration persistence and enhanced user experience.

Usage:
    # Interactive mode
    python install_insight_agent.py

    # CLI mode
    python install_insight_agent.py --installer <path> --token <token>
"""

import argparse
import glob
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rapid7.config import get_config  # noqa: E402
from src.rapid7.ui import create_ui  # noqa: E402


def find_installer_files(directory: Optional[str] = None) -> list:
    """
    Find Insight Agent installer files.

    Args:
        directory: Directory to search in (defaults to script directory)

    Returns:
        List of installer file paths
    """
    if directory is None:
        directory = os.path.dirname(os.path.abspath(__file__))

    return glob.glob(os.path.join(directory, "agent_installer-*.sh"))


def make_executable(filepath: str) -> None:
    """
    Make a file executable.

    Args:
        filepath: Path to file to make executable
    """
    os.chmod(filepath, 0o755)


def verify_agent_running() -> bool:
    """
    Verify if the Insight Agent is running.

    Returns:
        True if agent is running, False otherwise
    """
    try:
        result = subprocess.run(
            ["sudo", "service", "ir_agent", "status"],
            check=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "status", "ir_agent"],
                check=True,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def install_insight_agent(
    installer_path: str,
    token: str,
    ui=None
) -> bool:
    """
    Install the Rapid7 Insight Agent.

    Args:
        installer_path: Path to the installer script
        token: Installation token
        ui: Optional UI instance for formatted output

    Returns:
        True if installation successful, False otherwise
    """
    if ui:
        ui.print_header("Installing Rapid7 Insight Agent")
    else:
        print("\n=== Installing Rapid7 Insight Agent ===\n")

    # Verify installer exists
    if not os.path.exists(installer_path):
        if ui:
            ui.print_error(f"Installer not found: {installer_path}")
        else:
            print(f"ERROR: Installer not found: {installer_path}")
        return False

    # Make installer executable
    try:
        make_executable(installer_path)
        if ui:
            ui.print_info(f"Made installer executable: {installer_path}")
        else:
            print(f"Made installer executable: {installer_path}")
    except Exception as e:
        if ui:
            ui.print_error(f"Failed to make installer executable: {e}")
        else:
            print(f"ERROR: Failed to make installer executable: {e}")
        return False

    # Run installation
    try:
        if ui:
            ui.print_info("Running installer with sudo privileges...")
            ui.print_warning(
                "You may be prompted for your sudo password"
            )
        else:
            print("Running installer with sudo privileges...")
            print("You may be prompted for your sudo password")

        result = subprocess.run(
            ["sudo", installer_path, "install_start", "--token", token],
            check=True,
            capture_output=True,
            text=True
        )

        if ui:
            ui.print_success("Installation completed successfully!")
        else:
            print("✓ Installation completed successfully!")

        # Show output if available
        if result.stdout and ui:
            ui.print_info("Installation output:")
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        if ui:
            ui.print_error(f"Installation failed: {e}")
            if e.stderr:
                ui.print_error(f"Error output: {e.stderr}")
        else:
            print(f"ERROR: Installation failed: {e}")
            if e.stderr:
                print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        if ui:
            ui.print_error(f"Unexpected error during installation: {e}")
        else:
            print(f"ERROR: Unexpected error during installation: {e}")
        return False

    # Verify agent is running
    if ui:
        ui.print_info("Verifying agent status...")
    else:
        print("Verifying agent status...")

    if verify_agent_running():
        if ui:
            ui.print_success("Agent is running!")
        else:
            print("✓ Agent is running!")
        return True
    else:
        if ui:
            ui.print_warning("Agent may not be running. Check manually.")
        else:
            print("⚠ Agent may not be running. Check manually.")
        return True  # Installation succeeded even if we can't verify status


def interactive_mode() -> None:
    """
    Run the tool in interactive mode with user prompts.
    """
    ui = create_ui()
    config = get_config()

    ui.print_header("Rapid7 Insight Agent Installer")

    # Get tool-specific config
    tool_config = config.get_tool_config('install_insight_agent')

    # Find installer files
    ui.print_header("Finding Installer Files")

    search_dir = tool_config.get('search_directory')
    if search_dir:
        ui.print_info(f"Searching in: {search_dir}")
        installer_files = find_installer_files(search_dir)
    else:
        ui.print_info("Searching in current directory")
        installer_files = find_installer_files()

    if not installer_files:
        ui.print_warning("No installer files found automatically")
        installer_path = ui.prompt(
            "Enter the full path to the installer file"
        )
        if not installer_path:
            ui.print_error("No installer path provided. Exiting.")
            return
    elif len(installer_files) == 1:
        installer_path = installer_files[0]
        ui.print_info(f"Found installer: {installer_path}")
        if not ui.confirm("Use this installer?", default=True):
            installer_path = ui.prompt(
                "Enter the full path to the installer file"
            )
            if not installer_path:
                ui.print_error("No installer path provided. Exiting.")
                return
    else:
        ui.print_info(f"Found {len(installer_files)} installer files:")
        selection = ui.select_menu(
            "Select an installer",
            installer_files
        )
        if selection is None:
            ui.print_error("No installer selected. Exiting.")
            return
        installer_path = installer_files[selection]

    # Get token
    ui.print_header("Installation Token")

    last_token = tool_config.get('last_token')
    if last_token:
        ui.print_info("Previous token found (masked)")
        use_last = ui.confirm("Use previous token?", default=True)
        if use_last:
            token = last_token
        else:
            token = ui.prompt("Enter installation token")
    else:
        token = ui.prompt("Enter installation token")

    if not token:
        ui.print_error("No token provided. Exiting.")
        return

    # Preview and confirm
    ui.print_header("Installation Summary")
    ui.print_info(f"Installer: {installer_path}")
    ui.print_info(f"Token: {'*' * len(token)}")

    if not ui.confirm("\nProceed with installation?", default=True):
        ui.print_warning("Installation cancelled")
        return

    # Perform installation
    success = install_insight_agent(installer_path, token, ui)

    # Save configuration if successful
    if success:
        save_config = ui.confirm(
            "\nSave configuration for future use?",
            default=True
        )
        if save_config:
            tool_config['search_directory'] = os.path.dirname(installer_path)
            tool_config['last_token'] = token
            config.set_tool_config('install_insight_agent', tool_config)
            config.save()
            ui.print_success("Configuration saved")


def main() -> None:
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description='Install Rapid7 Insight Agent'
    )
    parser.add_argument(
        '--installer',
        help='Path to the installer script'
    )
    parser.add_argument(
        '--token',
        help='Installation token'
    )

    args = parser.parse_args()

    # If arguments provided, run in CLI mode
    if args.installer and args.token:
        ui = create_ui()
        success = install_insight_agent(args.installer, args.token, ui)
        sys.exit(0 if success else 1)
    elif args.installer or args.token:
        print("ERROR: Both --installer and --token must be provided")
        parser.print_help()
        sys.exit(1)
    else:
        # Run in interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
