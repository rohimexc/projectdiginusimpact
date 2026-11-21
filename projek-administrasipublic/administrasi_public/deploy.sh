#!/bin/bash
set -e

echo "=== 0. TARIK UPDATE TERBARU DARI GITHUB ==="
if [ -d "$HOME/projectdiginusimpact/.git" ]; then
  cd "$HOME/projectdiginusimpact"
  git pull origin dev-anggitamaharani
  cd "$HOME/projectdiginusimpact/projek-administrasipublic/administrasi_public"
fi

echo "=== BERSIHKAN FILE TIDAK PERLU UNTUK MENGHEMAT QUOTA ==="
rm -rf ~/.cache
rm -rf ~/projectdiginusimpact/belajarDJANGO
rm -rf ~/projectdiginusimpact/day-1companyprofile
rm -rf ~/projectdiginusimpact/projek-administrasipublic/env
rm -rf ~/projectdiginusimpact/projek-administrasipublic/venv

# Deteksi virtualenv yang sudah ada (kas-env atau myenv)
if [ -d "$HOME/.virtualenvs/kas-env/bin" ]; then
  VENV_DIR="$HOME/.virtualenvs/kas-env"
elif [ -d "$HOME/.virtualenvs/myenv/bin" ]; then
  VENV_DIR="$HOME/.virtualenvs/myenv"
elif [ -n "$VIRTUAL_ENV" ]; then
  VENV_DIR="$VIRTUAL_ENV"
else
  echo "=== 1. MEMBUAT VIRTUAL ENVIRONMENT ==="
  python3 -m venv ~/.virtualenvs/myenv
  VENV_DIR="$HOME/.virtualenvs/myenv"
fi

echo "=== 2. MENGAKTIFKAN VIRTUAL ENVIRONMENT: $VENV_DIR ==="
source "$VENV_DIR/bin/activate"

echo "=== 3. INSTALL REQUIREMENTS (HEMAT DISK) ==="
pip install --no-cache-dir -r requirements.txt

echo "=== 4. COLLECTSTATIC & MIGRATE ==="
python manage.py collectstatic --noinput
python manage.py migrate

# Otomatis reload web app jika file WSGI ada
WSGI_FILE="/var/www/${USER}_pythonanywhere_com_wsgi.py"
if [ -f "$WSGI_FILE" ]; then
  touch "$WSGI_FILE"
  echo "=== 5. WEB APP BERHASIL DIRELOAD ==="
fi

echo ""
echo "=========================================================="
echo "SUKSES! Semua dependensi dan database sudah siap!"
echo "Virtualenv: $VENV_DIR"
echo "=========================================================="
