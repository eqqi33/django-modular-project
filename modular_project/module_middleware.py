from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from engine.models import ModuleRegistry

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.strip("/").split("/")

        if not path_parts or not path_parts[0]:
            return self.get_response(request)

        module_prefix = path_parts[0]

        EXCLUDED_PREFIXES = [
            'admin', 'static', 'media', 'api', 'module', 'logout', 'login',
            'favicon.ico', 'robots.txt', 'sitemap.xml'
        ]

        if module_prefix in EXCLUDED_PREFIXES or module_prefix.endswith('.ico') or '.' in module_prefix:
            return self.get_response(request)

        expected_app_name = f"{module_prefix}_module"

        # Validasi app yang terinstall
        if any(expected_app_name in app for app in settings.INSTALLED_APPS):
            try:
                mod = ModuleRegistry.objects.get(name=expected_app_name)
                if not mod.is_installed:
                    messages.error(request, f"Module '{expected_app_name}' is not installed.")
                    return redirect('module_list')
            except ModuleRegistry.DoesNotExist:
                messages.error(request, f"Module '{expected_app_name}' is not registered.")
                return redirect('module_list')
        else:
            messages.error(request, f"Module '{expected_app_name}' is not in INSTALLED_APPS.")
            return redirect('module_list')

        return self.get_response(request)