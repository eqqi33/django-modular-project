from django.core.management.base import BaseCommand
from engine.models import ModuleRegistry
from product_module.models import Product

class Command(BaseCommand):
    help = "Seed initial data for modules and products"

    def handle(self, *args, **kwargs):
        modules = [
            "product_module", "inventory_module", "sales_module",
            "supplier_module", "report_module", "user_activity_module",
            "notification_module", "audit_module"
        ]

        for name in modules:
            module, created = ModuleRegistry.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Module '{name}' created."))
            else:
                self.stdout.write(f"• Module '{name}' already exists.")

        if not Product.objects.exists():
            Product.objects.bulk_create([
                Product(name='Laptop', price=8000000, stock=10),
                Product(name='Mouse', price=150000, stock=30),
                Product(name='Keyboard', price=250000, stock=20),
                Product(name='Monitor', price=2000000, stock=15),
                Product(name='USB Hub', price=75000, stock=50),
            ])
            self.stdout.write(self.style.SUCCESS("✔ Products created."))
        else:
            self.stdout.write("• Products already exist.")