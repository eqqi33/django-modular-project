#!/bin/bash
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

echo "✅ Menjalankan server..."
exec python manage.py runserver 0.0.0.0:8000

echo "🚀 Server sudah jalan..."