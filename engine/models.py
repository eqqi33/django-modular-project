from django.db import models

class ModuleRegistry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    version = models.FloatField(default=0)
    is_installed = models.BooleanField(default=False)
    installed_at = models.DateTimeField(auto_now_add=True)
    last_upgraded = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("install_moduleregistry", "Can install module"),
            ("uninstall_moduleregistry", "Can uninstall module"),
            ("upgrade_moduleregistry", "Can upgrade module"),
        ]