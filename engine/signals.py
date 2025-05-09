from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from engine.models import ModuleRegistry
from product_module.models import Product  # Adjust this path if needed

@receiver(post_migrate)
def setup_modules_products_roles(sender, **kwargs):
    # 1. Modules (with description & version)
    modules = [
        ("product_module", "Manage and display products", 1.0),
        ("inventory_module", "Track inventory changes", 1.0),
        ("sales_module", "Handle sales records", 1.0),
        ("supplier_module", "Manage suppliers and their products", 1.0),
        ("report_module", "Generate various reports", 1.0),
        ("user_activity_module", "Track user activities", 1.0),
        ("notification_module", "Send system notifications", 1.0),
        ("audit_module", "Approval and audit system", 1.0),
    ]

    for name, desc, version in modules:
        module, created = ModuleRegistry.objects.get_or_create(
            name=name,
            defaults={
                "description": desc,
                "version": version
            }
        )
        if created:
            print(f"✔ Module '{name}' created.")
        else:
            print(f"• Module '{name}' already exists.")

    # 2. Products (with barcode)
    if not Product.objects.exists():
        Product.objects.bulk_create([
            Product(name='Laptop', barcode='PRD001', price=8000000, stock=10),
            Product(name='Mouse', barcode='PRD002', price=150000, stock=30),
            Product(name='Keyboard', barcode='PRD003', price=250000, stock=20),
            Product(name='Monitor', barcode='PRD004', price=2000000, stock=15),
            Product(name='USB Hub', barcode='PRD005', price=75000, stock=50),
        ])
        print("✔ Products created.")
    else:
        print("• Products already exist.")

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
        'user': 'user123',
        'public': 'public123'
    }

    for username, password in test_users.items():
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.groups.add(Group.objects.get(name=username))
            user.is_staff = True  # Optional: for admin login access
            user.save()

    # Create superuser manager
    if not User.objects.filter(username='manager').exists():
        admin = User.objects.create_superuser('manager', 'manager@example.com', 'manager123')
        admin.groups.add(manager_group)

    # Create superuser admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.groups.add(manager_group)