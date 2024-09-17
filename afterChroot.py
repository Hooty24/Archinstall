from modules.system import improve_pacman_performance, generate_locales, set_time, set_root_password, \
    add_user_with_groups, rebuild_kernel, configure_sudo, install_loader, enable_services, set_hostname

# Improve pacman performance
improve_pacman_performance()

# Generate locales
langs = list(map(int, input('Languages to generate(type with space separate):\n1. Russian\n>> ').split()))
generate_locales([0] + langs)

# Set the time
set_time()

# Specify the hostname
set_hostname()

# Specify the password for the root user
set_root_password()

# Add new user with groups
add_user_with_groups()

# Rebuild the kernel
rebuild_kernel()

# sudo configuration
configure_sudo()

# Installation loader
install_loader()

# Enabling services
services = ['NetworkManager']
enable_services(services)
