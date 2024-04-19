import os
import glob
import subprocess

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Search for the installer files in the current directory
installer_files = glob.glob(os.path.join(current_directory, "agent_installer-*.sh"))

if not installer_files:
    # Prompt the user to provide the location of the installer file
    installer_file = input("Please enter the location of the installer file: ")
else:
    # Use the first found installer file
    installer_file = installer_files[0]

# Make the installer file executable
os.chmod(installer_file, 0o755)

# Prompt the user to input the token
token = input("Please enter the token: ")

# Continue with the installation
print("Installing Rapid7 Insight Agent...")
subprocess.run(["sudo", installer_file, "install_start", "--token", token], check=True)

print("Installation completed successfully!")
