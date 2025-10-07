#!/usr/bin/env python3
"""
Install Rapid7 Scan Assistant

This tool provides interactive installation of the Rapid7 Scan Assistant
with support for configuration persistence and enhanced user experience.

Usage:
    # Interactive mode
    python install_scan_assistant.py

    # CLI mode
    python install_scan_assistant.py --certificate <cert>
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.rapid7.config import get_config  # noqa: E402
from src.rapid7.ui import create_ui  # noqa: E402


def check_package_system() -> str:
    """
    Check the package system of the operating system.

    Returns:
        Package system type ("deb", "rpm", or "Unknown")
    """
    try:
        subprocess.run(
            ["dpkg", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "deb"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        subprocess.run(
            ["rpm", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "rpm"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return "Unknown"


def check_internet_connection() -> bool:
    """
    Check if there is an internet connection.

    Returns:
        True if connection available, False otherwise
    """
    try:
        subprocess.run(
            ["ping", "-c", "1", "rapid7.com"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        try:
            subprocess.run(
                ["ping", "-c", "1", "1.1.1.1"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False


def is_wget_curl_installed() -> Optional[str]:
    """
    Check if wget or curl is installed.

    Returns:
        "wget" or "curl" if installed, None otherwise
    """
    try:
        subprocess.run(
            ["wget", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "wget"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(
                ["curl", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return "curl"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None


def download_package(
    package_manager: str,
    ui=None
) -> bool:
    """
    Download the Scan Assistant package.

    Args:
        package_manager: Package manager type ("rpm" or "deb")
        ui: Optional UI instance

    Returns:
        True if successful, False otherwise
    """
    if ui:
        ui.print_header("Downloading Scan Assistant")

    # Check internet connection
    if ui:
        ui.print_info("Checking internet connection...")
    if not check_internet_connection():
        if ui:
            ui.print_error("No internet connection")
        else:
            print("ERROR: No internet connection")
        return False

    # Check for download tool
    if ui:
        ui.print_info("Checking for wget or curl...")
    tool = is_wget_curl_installed()
    if not tool:
        if ui:
            ui.print_error("Neither wget nor curl is installed")
        else:
            print("ERROR: Neither wget nor curl is installed")
        return False

    if ui:
        ui.print_success(f"Using {tool} for download")

    # Construct URLs
    base_url = "https://download2.rapid7.com/download/InsightVM/"
    file_extension = "rpm" if package_manager == 'rpm' else "deb"
    file_name = f"R7ScanAssistant_amd64.{file_extension}"
    file_url = base_url + file_name
    checksum_url = file_url + ".sha512sum"

    # Determine download command
    if tool == "wget":
        download_cmd = ["wget"]
    else:
        download_cmd = ["curl", "-O"]

    # Download files
    try:
        if ui:
            ui.print_info(f"Downloading {file_name}...")
        subprocess.run(download_cmd + [file_url], check=True)

        if ui:
            ui.print_info("Downloading checksum...")
        subprocess.run(download_cmd + [checksum_url], check=True)

        if ui:
            ui.print_success("Download complete")
        return True
    except subprocess.CalledProcessError as e:
        if ui:
            ui.print_error(f"Download failed: {e}")
        else:
            print(f"ERROR: Download failed: {e}")
        return False


def verify_checksum(package_manager: str, ui=None) -> bool:
    """
    Verify the SHA512 checksum of the downloaded package.

    Args:
        package_manager: Package manager type ("rpm" or "deb")
        ui: Optional UI instance

    Returns:
        True if checksum matches, False otherwise
    """
    if ui:
        ui.print_header("Verifying Checksum")

    file_extension = "rpm" if package_manager == 'rpm' else "deb"
    file_name = f"R7ScanAssistant_amd64.{file_extension}"
    checksum_file = f"{file_name}.sha512sum"

    try:
        # Calculate checksum
        result = subprocess.run(
            ['sha512sum', file_name],
            stdout=subprocess.PIPE,
            check=True,
            text=True
        )
        calculated = result.stdout.split()[0]

        # Read expected checksum
        with open(checksum_file, 'r', encoding='utf-8') as f:
            expected = f.read().split()[0]

        if calculated == expected:
            if ui:
                ui.print_success("Checksum verified")
            return True
        else:
            if ui:
                ui.print_error("Checksum mismatch")
            else:
                print("ERROR: Checksum mismatch")
            return False
    except Exception as e:
        if ui:
            ui.print_error(f"Checksum verification failed: {e}")
        else:
            print(f"ERROR: Checksum verification failed: {e}")
        return False


def create_config_file(certificate: str, ui=None) -> bool:
    """
    Create the Scan Assistant configuration file.

    Args:
        certificate: PEM client certificate
        ui: Optional UI instance

    Returns:
        True if successful, False otherwise
    """
    if ui:
        ui.print_header("Creating Configuration")

    package_manager = check_package_system()

    config_data = {
        "ClientCertificate": certificate,
        "ResponseTimeout": 300,
        "Debug": False,
        "PackageManager": package_manager
    }

    file_path = "/etc/rapid7/ScanAssistant/config.json"

    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write config
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)

        if ui:
            ui.print_success(f"Configuration saved to {file_path}")
        return True
    except Exception as e:
        if ui:
            ui.print_error(f"Failed to create config: {e}")
        else:
            print(f"ERROR: Failed to create config: {e}")
        return False


def install_package(package_manager: str, ui=None) -> bool:
    """
    Install the Scan Assistant package.

    Args:
        package_manager: Package manager type ("rpm" or "deb")
        ui: Optional UI instance

    Returns:
        True if successful, False otherwise
    """
    if ui:
        ui.print_header("Installing Package")

    file_extension = "rpm" if package_manager == 'rpm' else "deb"
    file_name = f"R7ScanAssistant_amd64.{file_extension}"

    if package_manager == 'rpm':
        cmd = ["sudo", "rpm", "-Uvh", "--replacefiles",
               "--replacepkgs", file_name]
    else:  # deb
        cmd = ["sudo", "dpkg", "-i", "--force-overwrite", file_name]

    try:
        if ui:
            ui.print_info("Running installation...")
            ui.print_warning("You may be prompted for your sudo password")

        subprocess.run(cmd, check=True)

        if ui:
            ui.print_success("Installation complete")
        return True
    except subprocess.CalledProcessError as e:
        if ui:
            ui.print_error(f"Installation failed: {e}")
        else:
            print(f"ERROR: Installation failed: {e}")
        return False


def verify_installation(package_manager: str, ui=None) -> bool:
    """
    Verify the Scan Assistant installation.

    Args:
        package_manager: Package manager type ("rpm" or "deb")
        ui: Optional UI instance

    Returns:
        True if verified, False otherwise
    """
    if ui:
        ui.print_header("Verifying Installation")

    # Check package
    try:
        if package_manager == 'rpm':
            subprocess.run(
                ["rpm", "-qa", "R7ScanAssistant"],
                check=True,
                capture_output=True,
                text=True
            )
        else:  # deb
            subprocess.run(
                ["dpkg-query", "-l", "r7scanassistant"],
                check=True,
                capture_output=True,
                text=True
            )

        if ui:
            ui.print_success("Package installed")
    except subprocess.CalledProcessError:
        if ui:
            ui.print_error("Package not found")
        return False

    # Check service
    try:
        subprocess.run(
            ["pgrep", "-f", "ScanAssistant"],
            check=True,
            capture_output=True,
            text=True
        )
        if ui:
            ui.print_success("Service running")
        return True
    except subprocess.CalledProcessError:
        if ui:
            ui.print_warning("Service may not be running")
        return True  # Don't fail if service check fails


def cleanup(package_manager: str, ui=None) -> bool:
    """
    Clean up installation files.

    Args:
        package_manager: Package manager type ("rpm" or "deb")
        ui: Optional UI instance

    Returns:
        True if successful, False otherwise
    """
    if ui:
        ui.print_header("Cleaning Up")

    file_extension = "rpm" if package_manager == 'rpm' else "deb"
    files = [
        f"R7ScanAssistant_amd64.{file_extension}",
        f"R7ScanAssistant_amd64.{file_extension}.sha512sum"
    ]

    try:
        for file in files:
            if os.path.exists(file):
                os.remove(file)
                if ui:
                    ui.print_info(f"Removed {file}")

        if ui:
            ui.print_success("Cleanup complete")
        return True
    except Exception as e:
        if ui:
            ui.print_warning(f"Cleanup warning: {e}")
        return True  # Don't fail on cleanup errors


def interactive_mode() -> None:
    """
    Run the tool in interactive mode with user prompts.
    """
    ui = create_ui()
    config = get_config()

    ui.print_header("Rapid7 Scan Assistant Installer")

    # Check package system
    package_manager = check_package_system()
    if package_manager not in ['rpm', 'deb']:
        ui.print_error(f"Unsupported package manager: {package_manager}")
        ui.print_info("This tool supports RPM and DEB systems only")
        return

    ui.print_success(f"Detected package manager: {package_manager}")

    # Get tool-specific config
    tool_config = config.get_tool_config('install_scan_assistant')

    # Get certificate
    ui.print_header("Client Certificate")
    ui.print_info(
        "Enter the one-line PEM client certificate from InsightVM console"
    )

    last_cert = tool_config.get('last_certificate')
    if last_cert:
        ui.print_info("Previous certificate found (masked)")
        use_last = ui.confirm("Use previous certificate?", default=True)
        if use_last:
            certificate = last_cert
        else:
            certificate = ui.prompt("Enter certificate (or leave blank)")
    else:
        certificate = ui.prompt("Enter certificate (or leave blank)")

    # Summary
    ui.print_header("Installation Summary")
    ui.print_info(f"Package Manager: {package_manager}")
    ui.print_info(
        f"Certificate: {'Provided' if certificate else 'Not provided'}"
    )

    if not ui.confirm("\nProceed with installation?", default=True):
        ui.print_warning("Installation cancelled")
        return

    # Download
    if not download_package(package_manager, ui):
        return

    # Verify checksum
    if not verify_checksum(package_manager, ui):
        if not ui.confirm("Continue despite checksum failure?", default=False):
            ui.print_warning("Installation cancelled")
            cleanup(package_manager, ui)
            return

    # Create config
    if certificate:
        if not create_config_file(certificate, ui):
            if not ui.confirm("Continue without config?", default=False):
                ui.print_warning("Installation cancelled")
                cleanup(package_manager, ui)
                return

    # Install
    if not install_package(package_manager, ui):
        cleanup(package_manager, ui)
        return

    # Verify
    verify_installation(package_manager, ui)

    # Cleanup
    cleanup(package_manager, ui)

    # Save configuration
    if certificate:
        save_config = ui.confirm(
            "\nSave certificate for future use?",
            default=True
        )
        if save_config:
            tool_config['last_certificate'] = certificate
            config.set_tool_config('install_scan_assistant', tool_config)
            config.save()
            ui.print_success("Configuration saved")

    ui.print_success("\nInstallation process complete!")


def main() -> None:
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description='Install Rapid7 Scan Assistant'
    )
    parser.add_argument(
        '--certificate',
        help='PEM client certificate'
    )
    parser.add_argument(
        '--skip-verify',
        action='store_true',
        help='Skip checksum verification'
    )

    args = parser.parse_args()

    # If certificate provided, run in CLI mode
    if args.certificate is not None:
        ui = create_ui()
        package_manager = check_package_system()

        if package_manager not in ['rpm', 'deb']:
            ui.print_error(f"Unsupported package manager: {package_manager}")
            sys.exit(1)

        success = (
            download_package(package_manager, ui) and
            (args.skip_verify or verify_checksum(package_manager, ui)) and
            (not args.certificate or
             create_config_file(args.certificate, ui)) and
            install_package(package_manager, ui) and
            verify_installation(package_manager, ui)
        )

        cleanup(package_manager, ui)
        sys.exit(0 if success else 1)
    else:
        # Run in interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
