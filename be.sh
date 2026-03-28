#!/bin/bash

# Warna
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Setup VPS Go Public (No Password Mode) ===${NC}"

# 1. Aktifkan Tailscale SSH (Fitur Login Tanpa Password)
echo -e "\n${BLUE}[1/3] Mengaktifkan Tailscale SSH...${NC}"
# Command ini bakal minta Tailscale buat handle autentikasi SSH
sudo tailscale up --ssh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Tailscale SSH aktif! Kamu bisa login tanpa password via network Tailscale.${NC}"
else
    echo -e "${YELLOW}[!] Gagal setup Tailscale SSH. Pastikan Tailscale sudah login.${NC}"
fi

# 2. Update SSH Config untuk Root
echo -e "\n${BLUE}[2/3] Mengizinkan akses Root...${NC}"
sudo sed -i 's/^#?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
# Opsional: Matikan password login via SSH biasa biar makin aman (hanya lewat Tailscale)
# sudo sed -i 's/^#?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 3. Restart SSH
echo -e "\n${BLUE}[3/3] Restarting SSH Service...${NC}"
sudo systemctl restart ssh

# Output Akhir
MY_TS_IP=$(tailscale ip -4)
echo -e "\n${GREEN}Selesai! Sekarang coba login dari perangkat lain:${NC}"
echo -e "${BLUE}Command: ssh root@$MY_TS_IP${NC}"
echo -e "\n${YELLOW}Note: Karena kita pake Tailscale SSH, kamu mungkin bakal diminta${NC}"
echo -e "${YELLOW}klik link verifikasi di browser saat pertama kali connect. Setelah itu, LANGSUNG MASUK.${NC}"
