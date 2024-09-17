import os
from modules.utils import replace_line_in_file


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

def generate_locales(locales):
    """
    Generates locales for chroot filesystem
    """
    print('\n#Generate locales')
    langs = {
        0: '#en_US.UTF-8 UTF-8',
        1: '#ru_RU.UTF-8 UTF-8'
    }
    for locale_number in locales:
        replace_line_in_file('/etc/locale.gen', langs[locale_number], langs[locale_number][1:])
    os.system('locale-gen')
