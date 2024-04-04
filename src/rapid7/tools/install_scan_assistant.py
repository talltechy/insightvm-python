import json
import os
import subprocess
import sys

def check_package_system():
    """
    Checks the package system of the operating system.

    Returns:
        str: The package system of the operating system. Possible values are "deb" for Debian-based systems,
        "rpm" for Red Hat-based systems, and "Unknown" if the package system cannot be determined.
    """
    try:
        # Check if dpkg is available
        subprocess.run(["dpkg", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "deb"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        # Check if rpm is available
        subprocess.run(["rpm", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "rpm"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return "Unknown"


def check_internet_connection():
    """
    Check if there is an internet connection.
    Returns True if there is a connection, False otherwise.
    """
    try:
        # Check if we can reach rapid7.com, if that fails check 1.1.1.1
        subprocess.run(
            ["ping", "-c", "1", "rapid7.com"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(
                ["ping", "-c", "1", "1.1.1.1"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            return False

def is_wget_curl_installed():
    """
    Checks if either 'wget' or 'curl' is installed on the system.

    Returns:
        str: The name of the installed utility ('wget' or 'curl').
        None: If neither 'wget' nor 'curl' is installed.
    """
    try:
        subprocess.run(["wget", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "wget"
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["curl", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "curl"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

def download_install_package():
    """
    Downloads and installs the Scan Assistant package.

    This function checks for an internet connection, the availability of either wget or curl,
    and the supported package manager (rpm or deb). It constructs the file URLs, determines
    the correct download command based on the available tool, and downloads the package and
    checksum using the chosen tool.

    Raises:
        SystemExit: If there is no internet connection, neither wget nor curl is installed,
                    or the package manager is unsupported.
    """
    if not check_internet_connection():
        sys.exit("No internet connection. Please check your connection.")

    wget_or_curl = is_wget_curl_installed()
    if not wget_or_curl:
        sys.exit("Neither wget nor curl is installed. Please install one of them to continue.")

    package_manager = check_package_system()
    if package_manager not in ['rpm', 'deb']:
        sys.exit("Unsupported package manager.")

    # Construct the file URLs
    base_url = "https://download2.rapid7.com/download/InsightVM/"
    file_extension = "rpm" if package_manager == 'rpm' else "deb"
    file_name = f"R7ScanAssistant_amd64.{file_extension}"
    file_url = base_url + file_name
    checksum_url = file_url + ".sha512sum"

    # Determine the correct download command based on available tool
    if wget_or_curl == "wget":
        download_command = ["wget"]
    else:  # curl
        download_command = ["curl", "-O"]

    # Download the package and checksum using the chosen tool
    try:
        subprocess.run(download_command + [file_url], check=True)
        subprocess.run(download_command + [checksum_url], check=True)
    except subprocess.CalledProcessError:
        sys.exit(f"Failed to download {file_name}. Please check your connection and try again.")


def sha512sum_verify():
    """
    Verify the SHA512 sum of the downloaded package.

    This function checks the SHA512 sum of the downloaded package against the expected SHA512 sum.
    It uses the `check_package_system` function to determine the package manager and performs the
    verification accordingly. If the SHA512 sum matches, it prints a success message. If the SHA512
    sum does not match, it prints an error message, downloads the package again, and recursively
    calls itself to verify the new download.

    Returns:
        None
    """
    # Use the check_package_system function to determine package manager
    package_manager = check_package_system()

    # Check the sha512sum of the downloaded package
    if package_manager == 'rpm':
        sha512sum = subprocess.run(['sha512sum', 'R7ScanAssistant_amd64.rpm'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').split()[0]
        with open('R7ScanAssistant_amd64.rpm.sha512sum', 'r', encoding='utf-8') as f:
            expected_sha512sum = f.read().split()[0]
    elif package_manager == 'deb':
        sha512sum = subprocess.run(['sha512sum', 'R7ScanAssistant_amd64.deb'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').split()[0]
        with open('R7ScanAssistant_amd64.deb.sha512sum', 'r', encoding='utf-8') as f:
            expected_sha512sum = f.read().split()[0]
    else:
        print("Unsupported package manager.")
        return

    if sha512sum == expected_sha512sum:
        print("SHA512 sum matches.")
    else:
        print("SHA512 sum does not match. Downloading again.")
        download_install_package()
        sha512sum_verify()

def generate_config_file():
    """
    This function prompts the user to enter a one line PEM file client certificate that was generated via the InsightVM console.
    It then creates a JSON configuration file with the provided client certificate and other configuration parameters.
    The configuration file is saved at the specified file path: /etc/rapid7/ScanAssistant/config.json.
    """
    package_manager = check_package_system()
    if package_manager not in ['rpm', 'deb']:
        sys.exit("Unsupported package manager.")
    # The one line PEM file that was created on the Security Console can be pasted into the config.json between the quotations in the ClientCertificate field
    client_certificate = input("Enter the one line PEM file client certificate that was generated via the InsightVM console(or press Enter to leave blank): ")
    # Define the dictionary for the JSON content
    config_data = {
        "ClientCertificate": client_certificate,
        "ResponseTimeout": 300,
        "Debug": False,
        "PackageManager": os.getenv(package_manager)
    }

    # Define the file path
    file_path = "/etc/rapid7/ScanAssistant/config.json"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the JSON content to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=4)

def install_package():
    """
    Installs the Scan Assistant package based on the package manager detected.

    Raises:
        subprocess.CalledProcessError: If the installation command fails.
        SystemExit: If the package manager is unsupported or the installation fails.
    """
    package_manager = check_package_system()
    if package_manager == 'rpm':
        try:
            subprocess.run(["sudo", "rpm", "-Uvh", "--replacefiles", "--replacepkgs", "R7ScanAssistant_amd64.rpm"], check=True)
        except subprocess.CalledProcessError:
            sys.exit("Failed to install the package.")
    elif package_manager == 'deb':
        try:
            subprocess.run(["sudo", "dpkg", "-i", "--force-overwrite", "R7ScanAssistant_amd64.deb"], check=True)
        except subprocess.CalledProcessError:
            sys.exit("Failed to install the package.")
    else:
        sys.exit("Unsupported package manager.")

def verify_installation():
    """
    Verifies the installation of the Scan Assistant package.

    This function checks the package manager system and verifies if the Scan Assistant package is installed.
    If the package is installed, it also checks if the Scan Assistant service is running.

    Raises:
        subprocess.CalledProcessError: If the package is not installed or the service is not running.
        sys.exit: If an unsupported package manager is detected.

    """
    package_manager = check_package_system()
    if package_manager == 'rpm':
        try:
            result = subprocess.run(["rpm", "-qa", "|", "grep", "R7ScanAssistant"], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError:
            sys.exit("Package not installed.")
    elif package_manager == 'deb':
        try:
            result = subprocess.run(["dpkg-query", "-l", "|", "grep", "r7scanassistant"], check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError:
            sys.exit("Package not installed.")
    else:
        sys.exit("Unsupported package manager.")

    try:
        result = subprocess.run(["ps", "-ef", "|", "grep", "ScanAssistant"], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError:
        sys.exit("Service not running.")

def cleanup():
    """
    Removes the install files for the R7ScanAssistant_amd64.

    This function attempts to remove the install files for the R7ScanAssistant_amd64.
    If the removal fails, the function will exit with an error message.

    Raises:
        subprocess.CalledProcessError: If the removal of the install files fails.

    """
    try:
        subprocess.run(["rm", "R7ScanAssistant_amd64.*"], check=True)
    except subprocess.CalledProcessError:
        sys.exit("Failed to cleanup the install files.")
    # Exit the script
    sys.exit("Installation and cleanup complete.")

def main():
    """
    This is the main function that orchestrates the installation process of the scan assistant.

    It performs the following steps:
    1. Downloads and installs the package.
    2. Verifies the integrity of the package using SHA512 checksum.
    3. Generates the configuration file.
    4. Installs the package.
    5. Verifies the installation.
    6. Cleans up any temporary files.

    """
    download_install_package()
    sha512sum_verify()
    generate_config_file()
    install_package()
    verify_installation()
    cleanup()

if __name__ == "__main__":
    main()
