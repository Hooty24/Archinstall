import os

optional_programs = ['linux-zen-headers', 'base-devel', 'bluez-utils', 'btop', 'fastfetch', 'firefox', 'fish',
                     'fuse2', 'git', 'github-cli', 'code',
                     'micro', 'pass', 'pyenv', 'python-poetry', 'speedtest-cli', 'telegram-desktop', 'timeshift',
                     'torbrowser-launcher', 'wireguard-tools']

hyprland = ['kitty', 'hyprland', 'waybar', 'wofi']

kde = ['plasma', 'dolphin', 'ark', 'gwenview', 'kate', 'elisa', 'spectacle',  'kdeconnect', 'sshfs']

yay = ['waydroid', 'onlyoffice-bin', 'code-marketplace']

deps = ['less', 'openresolv']

print('if no Internet connection write: nmcli device wifi connect SSID password "password"')

# Fish shell
print('\n#Fish shell')
os.system('chsh')

# Software and DE
print('\n#Installing software and DE')
os.system(f'sudo pacman -S --needed {' '.join(optional_programs + kde)}')

# Enabling services
print('\n#Enabling services')
os.system('systemctl enable sddm.service')
os.system('systemctl enable bluetooth.service')

# Deps install
print('\n#Installing dependencies')
os.system(f'sudo pacman -S {" ".join(deps)}')
