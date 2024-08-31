import os
from modules.utils import replace_line_in_file


# Improve pacman performance
print('\n#Improving pacman performance')
replace_line_in_file('/etc/pacman.conf', '#Color', 'Color')
replace_line_in_file('/etc/pacman.conf', '#ParallelDownloads = 5', 'ParallelDownloads = 15')
os.system('pacman -Sy')

# Generate locales
print('\n#Generate locales')
langs = ['#ru_RU.UTF-8 UTF-8', '#fr_FR.UTF-8 UTF-8']
for i, x in enumerate(langs):
    print(f'{i}) {langs[i]}')
lang = int(input('Choose a language (0-1): '))
replace_line_in_file('/etc/locale.gen', langs[lang], 'ru_RU.UTF-8 UTF-8')
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
os.system(f'useradd -m -G wheel,audio,video,storage {username}')
os.system(f'passwd {username}')

# Rebuild the kernel
print('\n#Rebuilding the kernel')
with open('/etc/mkinitcpio.conf', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if line.startswith('HOOKS'):
        temp = line.replace('=', ' ').replace('(', ' ').replace(')', ' ').split()
        temp = temp[:-1] + ['encrypt', 'lvm2'] + [temp[-1]]
        lines[i] = f'{temp[0]}=({" ".join(temp[1:])})\n'
        break
with open('/etc/mkinitcpio.conf', 'w') as f:
    f.writelines(lines)
os.system('mkinitcpio -p linux-zen')

# sudo configuration
print('#\nsudo configuration')
print('Uncomment: %wheel ALL=(ALL:ALL) ALL')
input('Press enter to continue')
os.system('sudo EDITOR=micro visudo')

# Installation loader
os.system('refind-install')
disk_path = input('Input path to main disk: ')
part_symbol = 'p' if 'nvme' in disk_path else ''
os.system(f'blkid -s UUID {disk_path}{part_symbol}3 > inf.txt')
with open('inf.txt', 'r') as f:
    disk_uuid = f.readline().split()[1][6:-1]
os.remove('inf.txt')
refind_config = '# prepare boot options for refind\n' + \
                f'BOOT_OPTIONS="cryptdevice=UUID={disk_uuid}:main root=/dev/mapper/main-root"\n\n' + \
                '''# configure refind
"Boot with standard options"  "${BOOT_OPTIONS} rw loglevel=3"
"Boot to single-user mode"    "${BOOT_OPTIONS} rw loglevel=3 single"
"Boot with minimal options"   "ro ${BOOT_OPTIONS}"'''
with open('/boot/refind_linux.conf', 'w') as f:
    f.write(refind_config)

# Enabling services
os.system('systemctl enable NetworkManager')
