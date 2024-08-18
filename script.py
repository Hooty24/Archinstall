import os

os.system = print

## Ping test
print('#Test Internet Connection')
os.system('ping nhentai.com')

## Time synchronization
print('\n#Time synchronization')
os.system('timedatectl set-ntp true')
os.system('timedatectl status')

## Disk partition
print('\n#Disk partition')
disk_path = input('Input path to main disk: ')
part_symbol = 'p' if 'nvme' in disk_path else ''

# Display instructions
print("Disk Partition Instructions:")
print('1. "g" for gpt table')
print('2. New partition:')
print('\t1. "n" for new partition')
print('\t2. Enter')
print('\t3. Enter')
print('\t4. +(number)(M/G)/Enter (for Linux FS)')
print('3. Set partition type (EFI & swap):')
print('\t1. "t" for set type')
print('\t2. (1/2) - (efi/swap)')
print('\t3. (1/19) - (efi/swap)')
print('4. "w" for write changes')

# Run fdisk
os.system(f'fdisk {disk_path}')

## Disk encryption
print('\n#Disk encryption')
os.system(f'cryptsetup luksFormat {disk_path}{part_symbol}3')
os.system(f'cryptsetup open {disk_path}{part_symbol}3 luks')

# Create logical partitions inside the encrypted partition
os.system('pvcreate /dev/mapper/luks')
os.system('vgcreate main /dev/mapper/luks')

# Put 100% of the encrypted partition into the root logical partition
os.system('lvcreate -l 100%FREE main -n root')

## Partition preparation and mounting
print('\n#Partition preparation and mounting')

# Format boot partition to Fat32
os.system(f'mkfs.fat -F32 {disk_path}{part_symbol}1')

# Initialize and activate swap partition
os.system(f'mkswap {disk_path}{part_symbol}2')
os.system(f'swapon {disk_path}{part_symbol}2')

# Format the partition to ext4
os.system('mkfs.ext4 /dev/mapper/main-root')

# Mount the partitions for installing the system
os.system('mount /dev/mapper/main-root /mnt')
os.system('mkdir /mnt/boot')
os.system(f'mount {disk_path}{part_symbol}1 /mnt/boot')

## Build the kernel and basic software
required_programs = ['base', 'linux-zen', 'linux-firmware', 'lvm2', 'refind', 'networkmanager']
optional_programs = ['linux-zen-headers', 'base-devel', 'ark', 'bluez-utils', 'btop', 'code',
                     'dolphin', 'elisa', 'fastfetch', 'firefox', 'fish', 'fuse2', 'ffmpeg', 'git', 'github-cli',
                     'gparted',
                     'gwenview',
                     'kate', 'kdeconnect', 'konsole', 'micro', 'pass', 'pyenv', 'spectacle', 'speedtest-cli',
                     'telegram-desktop',
                     'timeshift', 'torbrowser-launcher', 'wireguard-tools', 'arj', 'lrzip', 'lzop', 'p7zip',
                     'unarchiver', 'unrar']
yay = ['yay', 'code-marketplace', 'waydroid', 'onlyoffice-bin']

# Install basic software
print('\n#Install basic software')
os.system(f'pacstrap -K /mnt {" ".join(required_programs)}')

# Generate fstab
print('\n#Generate fstab')
os.system('genfstab -U /mnt >> /mnt/etc/fstab')

# Configure the system
print('\n#Configure the system')
os.system('arch-chroot /mnt')

# Generate locales
print('\n#Generate locales')


def replace_line_in_file(file_path, old_line, new_line):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == old_line.strip():
            print([lines[i]])
            lines[i] = new_line

    with open(file_path, 'w') as f:
        f.writelines(lines)


replace_line_in_file('/etc/locale.gen', '#ru_RU.UTF-8 UTF-8', 'ru_RU.UTF-8 UTF-8\n')
replace_line_in_file('/etc/locale.gen', '#en_US.UTF-8 UTF-8', 'en_US.UTF-8 UTF-8\n')
os.system('locale-gen')

# Set the time
print('\n#Set the time')
os.system('ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime')
os.system('hwclock --systohc')
