import os

## Ping test
print('#Testing Internet connection')
os.system('ping nhentai.net')

## Time synchronization
print('\n#Time synchronization')
os.system('timedatectl set-ntp true')
os.system('timedatectl status')

## Disk partition
print('\n#Disk partitioning')
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
print('\n#Disk encrypting')
os.system(f'cryptsetup luksFormat {disk_path}{part_symbol}3')
os.system(f'cryptsetup open {disk_path}{part_symbol}3 luks')

# Create logical partitions inside the encrypted partition
os.system('pvcreate /dev/mapper/luks')
os.system('vgcreate main /dev/mapper/luks')

# Put 100% of the encrypted partition into the root logical partition
os.system('lvcreate -l 100%FREE main -n root')

# Format boot partition to Fat32
print('\n#Formating boot partition to Fat32')
os.system(f'mkfs.fat -F32 {disk_path}{part_symbol}1')

# Initialize and activate swap partition
print('\n#Initializing and activating swap partition')
os.system(f'mkswap {disk_path}{part_symbol}2')
os.system(f'swapon {disk_path}{part_symbol}2')

# Format the partition to ext4
print('\n#Formatting partition to ext4')
os.system('mkfs.ext4 /dev/mapper/main-root')

# Mount the partitions for installing the system
print('\n#Mounting the partitions for installing the system')
os.system('mount /dev/mapper/main-root /mnt')
os.system('mkdir /mnt/boot')
os.system(f'mount {disk_path}{part_symbol}1 /mnt/boot')


## Build the kernel and basic software
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

required_programs = ['base', 'linux-zen', 'linux-firmware', 'lvm2', 'refind', 'networkmanager', 'micro', 'sudo']

# Install basic software
print('\n#Installing basic software')
os.system(f'pacstrap -K /mnt {" ".join(required_programs)}')

# Generate fstab
print('\n#Generating fstab')
os.system('genfstab -U /mnt >> /mnt/etc/fstab')

# Enter chroot environment
print('\n#Entering chroot environment')
os.system('arch-chroot /mnt')
