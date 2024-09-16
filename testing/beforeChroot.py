import os
from modules.network import ping_test, time_synchronization
from modules.disk import disk_partition, disk_encryption, format_boot_partition, initialize_swap_partition, \
    format_partition_ext4
from modules.system import mount_partitions, improve_pacman_performance, install_basic_software, generate_fstab

# Ping test
ping_test()

# Time synchronization
time_synchronization()

## Disk partition
disk_path = input('Input path to main disk: ')
part_symbol = 'p' if 'nvme' in disk_path else ''
loader = input('What loader you want to use:\n1. GRUB(BIOS)\n2. Refind(UEFI)')
fs_partition_number = 3 if loader == '2' else 4
disk_partition(disk_path, fs_partition_number)

# Disk encryption
disk_encryption(disk_path, part_symbol, loader)

# Format boot partition to Fat32
format_boot_partition(disk_path, part_symbol, fs_partition_number)

# Initialize and activate swap partition
initialize_swap_partition(disk_path, part_symbol, fs_partition_number)

# Format the partition to ext4
format_partition_ext4()

# Mount the partitions for installing the system
mount_partitions(disk_path, part_symbol, fs_partition_number)

# Improve pacman performance
improve_pacman_performance()

required_programs = ['base', 'linux-zen', 'linux-firmware', 'lvm2', 'networkmanager', 'micro', 'sudo', 'python']
required_programs += ['refind'] if loader == '2' else ['grub']

# Install basic software
install_basic_software()

# Generate fstab
generate_fstab()

# Enter chroot environment
print('\nTo enter chroot environment write: arch-chroot /mnt')
