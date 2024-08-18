import os

# Ping test
print('Test Internet Connection')
os.system('ping nhentai.com')

# Time synchronization
os.system('timedatectl set-ntp true')
os.system('timedatectl status')
