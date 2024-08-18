import os

# Ping test
print('Test Internet Connection')
os.system('ping nhentai.com')

# Time synchronization
os.system('timedatectl set-ntp true')
os.system('timedatectl status')

# Disk partition
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