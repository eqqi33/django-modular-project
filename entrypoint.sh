#!/bin/bash
if [ -f .env_docker ]; then
  cp .env_docker docker/.env_docker
else
  echo > docker/.env_docker  # empty placeholder
fi

echo "⏳ Menunggu database siap..."
sleep 5

echo "🚀 Menjalankan migrate..."
python manage.py migrate --noinput

echo "📦 Menjalankan collectstatic..."
python manage.py collectstatic --noinput

echo "👤 Mengecek default superuser..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created.')
else:
    print('Superuser already exists.')
EOF

echo "🌱 Menjalankan seed_data.py (jika ada)..."
if [ -f seed_data.py ]; then
    python manage.py seed
fi

echo "🧪 Menjalankan test_roles.py (jika ada)..."
if [ -f test_roles.py ]; then
    python manage.py test_roles
fi

echo "✅ Menjalankan Gunicorn..."
exec gunicorn modular_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3

# 🚀 Jalankan sesuai environment
if [ "$RAILWAY_ENVIRONMENT" = "production" ] || [ "$IS_PRODUCTION" = "1" ]; then
    echo "✅ Menjalankan Gunicorn (Production)..."
    exec gunicorn modular_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3
else
    echo "✅ Menjalankan Django Runserver (Development)..."
    exec python manage.py runserver 0.0.0.0:8000
fi
echo "🚀 Server sudah jalan..."