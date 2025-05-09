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
            'admin', 'accounts', 'static', 'media', 'api', 'module', 'logout', 'login',
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
                    if request.user.is_superuser:
                        messages.error(request, f"Module '{expected_app_name}' is not installed.")
                        return redirect('home')
                    else:
                        messages.error(request, f"Your request is not valid.")
                        return redirect('home')
            except ModuleRegistry.DoesNotExist:
                if request.user.is_superuser:
                    messages.error(request, f"Module '{expected_app_name}' is not registered.")
                    return redirect('home')
                else:
                    messages.error(request, f"Your request is not valid.")
                    return redirect('home')
        else:
            if request.user.is_superuser:
                messages.error(request, f"Module '{expected_app_name}' is not in INSTALLED_APPS.")
                return redirect('home')
            else:
                messages.error(request, f"Your request is not valid.")
                return redirect('home')

        return self.get_response(request)