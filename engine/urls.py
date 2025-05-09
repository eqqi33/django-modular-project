from django.urls import path
from .views import (
    ModuleListView,
    ModuleInstallView,
    ModuleUninstallView,
    ModuleUpgradeView,
)

urlpatterns = [
    path('module/', ModuleListView.as_view(), name='module_list'),
    path('module/install/<str:module_name>/', ModuleInstallView.as_view(), name='install_module'),
    path('module/uninstall/<str:module_name>/', ModuleUninstallView.as_view(), name='uninstall_module'),
    path('module/upgrade/<str:module_name>/', ModuleUpgradeView.as_view(), name='upgrade_module'),
]