#!/bin/bash
set -e

echo "=== BERSIHKAN FILE TIDAK PERLU UNTUK MENGHEMAT QUOTA ==="
rm -rf ~/.cache
rm -rf ~/projectdiginusimpact/belajarDJANGO
rm -rf ~/projectdiginusimpact/day-1companyprofile
rm -rf ~/projectdiginusimpact/projek-administrasipublic/env
rm -rf ~/projectdiginusimpact/projek-administrasipublic/venv

echo "=== 1. MEMBUAT VIRTUAL ENVIRONMENT ==="
python3 -m venv ~/.virtualenvs/myenv

echo "=== 2. MENGAKTIFKAN VIRTUAL ENVIRONMENT ==="
source ~/.virtualenvs/myenv/bin/activate

echo "=== 3. INSTALL REQUIREMENTS (HEMAT DISK) ==="
pip install --no-cache-dir -r requirements.txt

echo "=== 4. COLLECTSTATIC & MIGRATE ==="
python manage.py collectstatic --noinput
python manage.py migrate

echo ""
echo "=========================================================="
echo "SUKSES! Semua dependensi dan database sudah siap!"
echo "Virtualenv: /home/$USER/.virtualenvs/myenv"
echo "=========================================================="
