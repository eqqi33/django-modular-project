from engine.models import ModuleRegistry

def installed_modules(request):
    try:
        modules = ModuleRegistry.objects.filter(is_installed=True)
    except Exception as e:
        modules = []
    return {"installed_modules": modules}