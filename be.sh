#!/bin/bash

# Warna buat output biar estetik
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Tailscale & SSH Root Access Setup ===${NC}"

# 1. Cek Status Tailscale
echo -e "\n${BLUE}[1/3] Mengecek status Tailscale...${NC}"
if command -v tailscale >/dev/null 2>&1; then
    TS_STATUS=$(tailscale status)
    echo -e "${GREEN}Tailscale terdeteksi! Berikut daftar device kamu:${NC}"
    echo "$TS_STATUS"
else
    echo -e "\e[31m[!] Tailscale belum terinstall. Install dulu ya pake: curl -fsSL https://tailscale.com/install.sh | sh\e[0m"
    exit 1
fi

# 2. Update SSH Config (PermitRootLogin)
echo -e "\n${BLUE}[2/3] Mengupdate konfigurasi SSH...${NC}"

# Backup config asli buat jaga-jaga
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Pake sed buat nyari baris PermitRootLogin dan ganti jadi 'yes'
# Kalau barisnya dikomentari (#), kita buka komentarnya
sudo sed -i 's/^#?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config

echo -e "${GREEN}Config berhasil diupdate: PermitRootLogin -> yes${NC}"

# 3. Restart Service SSH
echo -e "\n${BLUE}[3/3] Merestart service SSH...${NC}"
sudo systemctl restart ssh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Semua beres! SSH sudah siap digunakan.${NC}"
    
    # Menampilkan IP Tailscale VPS untuk kamu copy
    MY_TS_IP=$(tailscale ip -4)
    echo -e "\n${BLUE}Sekarang kamu bisa login dari luar pake command:${NC}"
    echo -e "${GREEN}ssh root@$MY_TS_IP${NC}"
else
    echo -e "\e[31m[!] Gagal merestart SSH. Cek manual pake 'sudo systemctl status ssh'\e[0m"
fi

echo -e "\n${BLUE}=== Done! Stay safe & keep cooking! ===${NC}"
