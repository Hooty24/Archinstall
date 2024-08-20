import os

optional_programs = ['linux-zen-headers', 'base-devel', 'bluez-utils', 'btop', 'fastfetch', 'firefox', 'fish',
                     'fuse2', 'git', 'github-cli', 'code',
                     'micro', 'pass', 'pyenv', 'python-poetry', 'speedtest-cli', 'telegram-desktop', 'timeshift',
                     'torbrowser-launcher', 'wireguard-tools']

temporary_programs = ['kitty']

needs = '''file manager, archiver, text editor, photo viewer, screenshot program, music player'''

yay = ['yay', 'waydroid', 'onlyoffice-bin', 'code-marketplace']


def replace_line_in_file(file_path, old_line, new_line):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == old_line.strip():
            lines[i] = new_line + '\n'

    with open(file_path, 'w') as f:
        f.writelines(lines)


# Improve pacman performance
print('\n#Improving pacman performance')
replace_line_in_file('/etc/pacman.conf', '#Color', 'Color')
replace_line_in_file('/etc/pacman.conf', '#ParallelDownloads = 5', 'ParallelDownloads = 15')
replace_line_in_file('/etc/pacman.conf', '#[multilib]', '[multilib]')
replace_line_in_file('/etc/pacman.conf', '#Include = /etc/pacman.d/mirrorlist', 'Include = /etc/pacman.d/mirrorlist')
os.system('pacman -Sy')

# Generate locales
print('\n#Generate locales')
replace_line_in_file('/etc/locale.gen', '#ru_RU.UTF-8 UTF-8', 'ru_RU.UTF-8 UTF-8')
replace_line_in_file('/etc/locale.gen', '#en_US.UTF-8 UTF-8', 'en_US.UTF-8 UTF-8')
os.system('locale-gen')

# Set the time
print('\n#Setting the time')
os.system('ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime')
os.system('hwclock --systohc')

# Specify the hostname
print('\n#Specifying the hostname')
os.system('echo "arch" > /etc/hostname')

# Specify the password for the root user
print('\n#Specifying the password for the root user')
os.system('passwd')

# Add new user with groups
print('\n#Adding new user with groups')
username = input('Enter username: ')
os.system(f'useradd -m -G wheel,audio,video,storage  {username}')
os.system(f'passwd {username}')

# Rebuild the kernel
print('\n#Rebuilding the kernel')
with open('/etc/mkinitcpio.conf', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.startswith('HOOKS'):
        temp = line.replace('=', ' ').replace('(', ' ').replace(')', ' ').split()
        temp = temp[:-1] + ['encrypt', 'lvm2'] + [temp[-1] + '\n']
        lines[i] = f'{temp[0]}=({" ".join(temp[1:])})'
with open('/etc/mkinitcpio.conf', 'w') as f:
    f.writelines(lines)
os.system('mkinitcpio -p linux-zen')

# sudo configuration
print('#\nsudo configuration')
print('Uncomment: %wheel ALL=(ALL:ALL) ALL')
os.system('sudo EDITOR=micro visudo')
