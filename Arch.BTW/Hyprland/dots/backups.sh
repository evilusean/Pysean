# a script for getting all the old critical pieces from my old arch install and bringing them over, just in case
tar -czvf "/mnt/sdb4/Old Code/2025-10-01-ArchConfigBackups/hyprland_backup_dotfiles.tar.gz" \
    ~/.config \
    ~/.local/bin \
    ~/.ssh \
    ~/.gnupg \
    ~/.bashrc \
    ~/.zshrc
