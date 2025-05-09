from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from engine.models import ModuleRegistry
from product_module.models import Product  # Adjust this path if needed

@receiver(post_migrate)
def setup_groups_and_users(sender, **kwargs):
    # Get or create all groups
    manager_group, _ = Group.objects.get_or_create(name='manager')
    user_group, _ = Group.objects.get_or_create(name='user')
    public_group, _ = Group.objects.get_or_create(name='public')

    # Assign all permissions to manager group
    manager_group.permissions.set(Permission.objects.all())

    # Assign specific permissions to user group
    user_perms = [
        # Model perms
        'add_product', 'change_product', 'view_product', 'search_product', 'export_product'
    ]
    user_group.permissions.set(Permission.objects.filter(codename__in=user_perms))

    # Assign only view permissions to public group
    public_perms = [
        'view_product', 'search_product', 'export_product'
    ]
    public_group.permissions.set(Permission.objects.filter(codename__in=public_perms))

    # Create demo users for each group
    test_users = {
        'manager': 'manager123',
        'user': 'user123',
        'public': 'public123'
    }

    for username, password in test_users.items():
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.groups.add(Group.objects.get(name=username))
            user.is_staff = True  # Optional: for admin login access
            user.save()

    # Create superuser admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.groups.add(manager_group)  # Optional