import importlib
from django.conf import settings

def load_plugin_urls(pattern_type="urlpatterns"):
    urlpatterns = []

    for app in settings.INSTALLED_APPS:
        try:
            mod = importlib.import_module(f"{app}.urls")
            if hasattr(mod, pattern_type):
                plugin_urls = getattr(mod, pattern_type)
                urlpatterns += plugin_urls
        except ModuleNotFoundError:
            continue  # plugin tidak punya urls.py

    return urlpatterns