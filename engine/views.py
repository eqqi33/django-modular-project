import os

from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
import subprocess, sys

from django.views.generic import ListView, TemplateView

from engine.mixin import CustomPermissionRequiredMixin
from engine.models import ModuleRegistry

class ModuleListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = ModuleRegistry
    template_name = 'engine/module_list.html'
    context_object_name = 'modules'
    paginate_by = 10
    permission_required = 'engine.view_moduleregistry'
    permission_redirect_url = 'no_permission'
    only_check_superuser = True

    def check_has_perm(self, access):
        user = self.request.user
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        return user.has_perm(f'{app_label}.{access}_{model_name}')

    def get_queryset(self):
        queryset = super().get_queryset()
        for module in queryset:
            module.path_exists = os.path.isdir(os.path.join(settings.BASE_DIR, module.name))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['module_title'] = "Modules"
        context['module_items_name'] = "modules"
        context['module_item_name'] = "module"

        # Hak akses user
        user = self.request.user
        context['can_view'] = self.check_has_perm('view')
        context['can_install'] = self.check_has_perm('install')
        context['can_uninstall'] = self.check_has_perm('uninstall')
        context['can_upgrade'] = self.check_has_perm('upgrade')
        context['is_superuser'] = user.is_superuser

        context['redirect_url'] = self.request.session.pop('module_redirect_url', None)

        return context

class ModuleInstallView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = 'engine.install_moduleregistry'
    permission_redirect_url = 'module_list'
    only_check_superuser = True

    def get(self, request, module_name):
        module, _ = ModuleRegistry.objects.get_or_create(name=module_name)
        module.is_installed = True
        module.save()
        redirect_url = f'/{module_name.replace("_module", "")}/'
        messages.success(
            request,
            f"Module '{module_name}' berhasil di-install. Anda akan diarahkan ke modul tersebut dalam 5 detik. "
            f"<a href='{redirect_url}' class='underline font-semibold text-gray-800 hover:text-black dark:text-white dark:hover:text-gray-200'>Klik di sini jika tidak otomatis</a>."
        )
        request.session['module_redirect_url'] = redirect_url
        return redirect('module_list')


class ModuleUninstallView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = 'engine.uninstall_moduleregistry'
    permission_redirect_url = 'module_list'
    only_check_superuser = True

    def get(self, request, module_name):
        module = get_object_or_404(ModuleRegistry, name=module_name)
        module.is_installed = False
        module.save()
        messages.success(request, f"Module '{module_name}' berhasil di-uninstall.")
        return redirect('module_list')


class ModuleUpgradeView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = 'engine.upgrade_moduleregistry'
    permission_redirect_url = 'module_list'
    only_check_superuser = True

    def get(self, request, module_name):
        module = get_object_or_404(ModuleRegistry, name=module_name)
        try:
            subprocess.run([sys.executable, 'manage.py', 'makemigrations', module.name], check=True)
            subprocess.run([sys.executable, 'manage.py', 'migrate', module.name], check=True)
            module.last_upgraded = timezone.now()
            module.save()
            messages.success(request, f"Module '{module.name}' upgraded successfully.")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Failed to upgrade module '{module.name}'. {str(e)}")
        return redirect('module_list')


class CustomLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or '/module/'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('custom_login')


class NoPermissionView(LoginRequiredMixin, TemplateView):
    template_name = 'components/no_permission.html'

    def dispatch(self, request, *args, **kwargs):
        # Add the error message (only once per session)
        if not any(m.message == "You do not have permission to access this page." for m in messages.get_messages(request)):
            messages.error(request, "You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)