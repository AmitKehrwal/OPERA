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

# Add Opera repository
os.system('add-apt-repository -y "deb [arch=i386,amd64] https://deb.opera.com/opera-stable/ stable non-free" > /dev/null 2>&1')

# Install Opera
os.system('apt install -y opera-stable > /dev/null 2>&1')

# Install selenium version 4.2.0
os.system('pip install selenium==4.2.0 > /dev/null 2>&1')

# Install faker
os.system('pip install faker > /dev/null 2>&1')
