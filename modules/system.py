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


def set_time(timezone='Europe/Moscow'):
    """
    Sets the system time by configuring the timezone and updating the hardware clock.
    """
    print('\n#Setting the time')
    os.system(f'ln -sf /usr/share/zoneinfo/{timezone} /etc/localtime')
    os.system('hwclock --systohc')


def set_hostname(hostname='archlinux'):
    """
    Sets the system hostname by writing to the /etc/hostname file and updating the current session.
    """
    print('\n#Specifying the hostname')
    os.system(f'echo "{hostname}" > /etc/hostname')


def set_root_password():
    """
    Sets the password for the root user.
    """
    print('\n#Specifying the password for the root user')
    os.system('passwd')


def add_user_with_groups():
    """
    Adds a new user with specified groups and sets the user's password.
    """
    print('\n#Adding new user with groups')
    username = input('Enter username: ')
    os.system(f'useradd -m -G wheel,audio,video,storage {username}')
    os.system(f'passwd {username}')


def rebuild_kernel():
    """
    Rebuilds the kernel by modifying the mkinitcpio configuration
    and running the mkinitcpio command.
    """
    print('\n#Rebuilding the kernel')
    with open('/etc/mkinitcpio.conf', 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('HOOKS'):
            temp = line.replace('=', ' ').replace('(', ' ').replace(')', ' ').split()
            temp = temp[:-2] + ['encrypt', 'lvm2'] + temp[-2:]
            lines[i] = f'{temp[0]}=({" ".join(temp[1:])})\n'
            break
    with open('/etc/mkinitcpio.conf', 'w') as f:
        f.writelines(lines)
    os.system('mkinitcpio -p linux-zen')


def configure_sudo():
    """
    Configures sudo.
    """
    print('\n#sudo configuration')
    print('Uncomment: %wheel ALL=(ALL:ALL) ALL')
    input('Press enter to continue')
    os.system('sudo EDITOR=micro visudo')


def refind_install(disk_uuid):
    os.system('refind-install')
    refind_config = '# prepare boot options for refind\n' + \
                    f'BOOT_OPTIONS="cryptdevice=UUID={disk_uuid}:main root=/dev/mapper/main-root"\n\n' + \
                    '''# configure refind
    "Boot with standard options"  "${BOOT_OPTIONS} rw loglevel=3"
    "Boot to single-user mode"    "${BOOT_OPTIONS} rw loglevel=3 single"
    "Boot with minimal options"   "ro ${BOOT_OPTIONS}"'''
    with open('/boot/refind_linux.conf', 'w') as f:
        f.write(refind_config)


def grub_install(disk_path, disk_uuid):
    replace_line_in_file('/etc/default/grub', 'GRUB_CMDLINE_LINUX=""',
                         f'GRUB_CMDLINE_LINUX="cryptdevice=UUID={disk_uuid}:main root=/dev/mapper/main-root"')
    replace_line_in_file('etc/default/grub', '#GRUB_ENABLE_CRYPTODISK=y', 'GRUB_ENABLE_CRYPTODISK=y')
    os.system(f'grub-install {disk_path}')
    os.system('grub-mkconfig -o /boot/grub/grub.cfg')


def install_loader():
    loader = input('What loader you want to use:\n1. GRUB(BIOS)\n2. Refind(UEFI)\n>> ')
    disk_path = input('Input path to main disk: ')
    part_symbol = 'p' if 'nvme' in disk_path else ''
    os.system(f'blkid -s UUID {disk_path}{part_symbol}3 > inf.txt')
    with open('inf.txt', 'r') as f:
        disk_uuid = f.readline().split()[1][6:-1]
    os.remove('inf.txt')
    if loader == '1':
        grub_install(disk_path, disk_uuid)
    elif loader == '2':
        refind_install(disk_uuid)
    else:
        print('Invalid loader choice')
        install_loader()


def enable_services(services):
    """
    Enables specified services on the system.
    """
    print('\n#Enabling services')
    os.system(f'systemctl enable {" ".join(services)}')
