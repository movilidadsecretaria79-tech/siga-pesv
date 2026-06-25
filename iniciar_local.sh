#!/usr/bin/env bash
# Script de arranque rápido para uso local en Linux/Mac.
set -e
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_catalogo_pesv
echo ""
echo "Si es la primera vez, cree el usuario administrador con:"
echo "  python manage.py createsuperuser"
echo ""
python manage.py runserver
