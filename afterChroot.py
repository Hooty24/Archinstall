import os

optional_programs = ['linux-zen-headers', 'base-devel', 'ark', 'bluez-utils', 'btop', 'code',
                     'dolphin', 'elisa', 'fastfetch', 'firefox', 'fish', 'fuse2', 'ffmpeg', 'git', 'github-cli',
                     'gparted',
                     'gwenview',
                     'kate', 'kdeconnect', 'konsole', 'micro', 'pass', 'pyenv', 'spectacle', 'speedtest-cli',
                     'telegram-desktop',
                     'timeshift', 'torbrowser-launcher', 'wireguard-tools', 'arj', 'lrzip', 'lzop', 'p7zip',
                     'unarchiver', 'unrar']
yay = ['yay', 'code-marketplace', 'waydroid', 'onlyoffice-bin']


# Generate locales
def replace_line_in_file(file_path, old_line, new_line):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == old_line.strip():
            print([lines[i]])
            lines[i] = new_line

    with open(file_path, 'w') as f:
        f.writelines(lines)


print('\n#Generate locales')
replace_line_in_file('/etc/locale.gen', '#ru_RU.UTF-8 UTF-8', 'ru_RU.UTF-8 UTF-8\n')
replace_line_in_file('/etc/locale.gen', '#en_US.UTF-8 UTF-8', 'en_US.UTF-8 UTF-8\n')
os.system('locale-gen')

# Set the time
print('\n#Set the time')
os.system('ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime')
os.system('hwclock --systohc')

# Specify the hostname
print('\n#Specify the hostname')
os.system('echo "arch" > /etc/hostname')
