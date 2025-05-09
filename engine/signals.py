from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_admin_and_groups(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        user.is_superuser = True
        user.is_staff = True
        user.save()

    for group_name in ['manager', 'user', 'public']:
        Group.objects.get_or_create(name=group_name)

    admin_user = User.objects.get(username='admin')
    manager_group = Group.objects.get(name='manager')
    admin_user.groups.add(manager_group)