import os
from modules.system import improve_pacman_performance, generate_locales

# Improve pacman performance
improve_pacman_performance()

# Generate locales
langs = list(map(int, input('Languages to generate(type with space separate):\n1. Russian\n>> ').split()))
generate_locales([0] + langs)

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
        temp = temp[:-2] + ['encrypt', 'lvm2'] + [temp[-2:]]
        lines[i] = f'{temp[0]}=({" ".join(temp[1:])})\n'
        break
with open('/etc/mkinitcpio.conf', 'w') as f:
    f.writelines(lines)
os.system('mkinitcpio -p linux-zen')

# sudo configuration
print('\n#sudo configuration')
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
