import os


def disk_partition(path, loader):
    """
    Partitions a disk using cfdisk, prompting for the desired loader type.
    """
    print('\nDisk Partition Instructions:')
    if loader == '1':
        print('1. 32M BIOS boot')
        print('2. 512M EFI System')
        print('3. 4G+ Linux SWAP')
        print('4. Remain Place Linux FS')
    elif loader == '2':
        print('1. 512M EFI System')
        print('2. 4G+ Linux SWAP')
        print('3. Remain Place Linux FS')
    else:
        print('Invalid loader type. Please choose 1 or 2.')
        exit()
    input('Press Enter to continue')
    os.system(f'cfdisk {path}')


def disk_encryption(disk_path, part_symbol, fs_partition_number):
    """
    Encrypts a disk partition using LUKS.
    """
    print('\n#Disk encrypting')
    os.system(f'cryptsetup luksFormat {disk_path}{part_symbol}{fs_partition_number}')
    os.system(f'cryptsetup open {disk_path}{part_symbol}{fs_partition_number} luks')
    os.system('pvcreate /dev/mapper/luks')
    os.system('vgcreate main /dev/mapper/luks')
    os.system('lvcreate -l 100%FREE main -n root')


def format_boot_partition(disk_path, part_symbol, fs_partition_number):
    """Formats a boot partition to Fat32."""
    print('\n#Formating boot partition to Fat32')
    os.system(f'mkfs.fat -F32 {disk_path}{part_symbol}{fs_partition_number - 2}')


def initialize_swap_partition(disk_path, part_symbol, fs_partition_number):
    """Initializes and activates a swap partition."""
    print('\n#Initializing and activating swap partition')
    os.system(f'mkswap {disk_path}{part_symbol}{fs_partition_number - 1}')
    os.system(f'swapon {disk_path}{part_symbol}{fs_partition_number - 1}')


def format_partition_ext4(disk_path, part_symbol, fs_partition_number, encryption):
    """Formats a partition to ext4."""
    print('\n#Formatting partition to ext4')
    os.system(
        f'mkfs.ext4 {'/dev/mapper/main-root' if encryption else disk_path + part_symbol + str(fs_partition_number)}')
