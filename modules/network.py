import os


def ping_test():
    """
    Test the internet connection by pinging a website.
    """
    print('#Testing Internet connection')
    os.system('ping nhentai.net')


def time_synchronization():
    """
    Synchronize the system time with an NTP server.
    """
    print('\n#Time synchronization')
    os.system('timedatectl set-ntp true')
    os.system('timedatectl status')
