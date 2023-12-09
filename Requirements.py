import os

# Install wget
os.system('apt install wget -y > /dev/null 2>&1')

# Install webdriver_manager
os.system('pip install webdriver_manager > /dev/null 2>&1')

# Upgrade webdriver_manager
os.system('pip install --upgrade webdriver_manager > /dev/null 2>&1')

# Add Opera repository key
os.system('wget -qO- https://deb.opera.com/archive.key | apt-key add - > /dev/null 2>&1')

# Set DEBIAN_FRONTEND to non-interactive mode
os.environ['DEBIAN_FRONTEND'] = 'noninteractive'

import subprocess

# Install wget
subprocess.run(["apt", "install", "wget", "-y"])

# Install webdriver_manager
subprocess.run(["pip", "install", "webdriver_manager"])

# Upgrade webdriver_manager
subprocess.run(["pip", "install", "--upgrade", "webdriver_manager"])

# Install curl
subprocess.run(["apt", "install", "curl", "-y"])

# Download Brave keyring
subprocess.run(["curl", "-fsSLo", "/usr/share/keyrings/brave-browser-archive-keyring.gpg", "https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg"])

# Add Brave repository
subprocess.run(["echo", "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main", "|", "sudo", "tee", "/etc/apt/sources.list.d/brave-browser-release.list"])

# Update package list
subprocess.run(["apt-get", "update"])

# Install Brave browser
subprocess.run(["apt", "install", "brave-browser"])


# Install selenium version 4.2.0
os.system('pip install selenium==4.2.0 > /dev/null 2>&1')

# Install faker
os.system('pip install indian_names > /dev/null 2>&1')
