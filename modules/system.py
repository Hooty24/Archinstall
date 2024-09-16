import os
from utils import replace_line_in_file


def mount_partitions(disk_path, part_symbol, fs_partition_number):
    """
    Mounts the partitions for installing the system.
    """
    print('\n#Mounting the partitions for installing the system')
    os.system('mount /dev/mapper/main-root /mnt')
    os.system('mkdir /mnt/boot')
    os.system(f'mount {disk_path}{part_symbol}{fs_partition_number - 2} /mnt/boot')


def improve_pacman_performance():
    """
    Improves pacman performance by enabling colors and increasing parallel downloads.
    """
    print('\n#Improving pacman performance')
    replace_line_in_file('/etc/pacman.conf', '#Color', 'Color')
    replace_line_in_file('/etc/pacman.conf', '#ParallelDownloads = 5', 'ParallelDownloads = 15')


def install_basic_software(required_programs):
    """
    Installs basic software on a mounted partition.
    """
    print('\n#Installing basic software')
    os.system(f'pacstrap -K /mnt {" ".join(required_programs)}')


def generate_fstab():
    """
    Generates the fstab file for a mounted partition.
    """
    print('\n#Generating fstab')
    os.system('genfstab -U /mnt >> /mnt/etc/fstab')
