import os

## Ping test
print('Test Internet Connection')
os.system('ping nhentai.com')

## Time synchronization
os.system('timedatectl set-ntp true')
os.system('timedatectl status')

## Disk partition
disk_path = input('Input path to main disk: ')

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
if 'nvme' in disk_path:
    os.system(f'cryptsetup luksFormat {disk_path}p3')
    os.system(f'cryptsetup open {disk_path}p3 luks')
else:
    os.system(f'cryptsetup luksFormat {disk_path}3')
    os.system(f'cryptsetup open {disk_path}3 luks')

# Check the partitions
os.system('ls /dev/mapper/*')

# Create logical partitions inside the encrypted partition
os.system('pvcreate /dev/mapper/luks')
os.system('vgcreate main /dev/mapper/luks')

# Put 100% of the encrypted partition into the root logical partition
os.system('lvcreate -l 100%FREE main -n root')

# View all logical partitions
os.system('lvs')
