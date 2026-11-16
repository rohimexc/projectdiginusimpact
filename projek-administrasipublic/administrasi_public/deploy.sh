#!/bin/bash
set -e

echo "=== MEMULAI SETUP OTOMATIS PYTHONANYWHERE ==="
echo "1. Membuat virtual environment..."
python3 -m venv ~/.virtualenvs/myenv

echo "2. Mengaktifkan virtual environment..."
source ~/.virtualenvs/myenv/bin/activate

echo "3. Menginstall dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "4. Menjalankan collectstatic & migrate..."
python manage.py collectstatic --noinput
python manage.py migrate

echo ""
echo "=========================================================="
echo "SUKSES! Semua dependensi dan database sudah siap!"
echo "Virtualenv: /home/$USER/.virtualenvs/myenv"
echo "=========================================================="
