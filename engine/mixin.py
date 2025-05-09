from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect


class AjaxResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def is_ajax(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return True
        else:
            return False

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax():
            context = {
                'form_class': form
            }
            html_form = render_to_string('components/partial_form.html', context)
            return JsonResponse({'form': html_form}, status=400)
        else:
            return response

    def form_valid(self, form):

        response = super().form_valid(form)

        if self.is_ajax():
            data = {
                'pk': self.object.pk,
                'redirect_url': response.url
            }
            return JsonResponse(data)
        else:
            return response

    def form_add(self, form, str_url):
        if self.is_ajax():
            html_form = render_to_string('components/partial_form.html',
                                         {'form_class': form}, request=self.request)
            data = {
                'action_url': reverse(str_url),
                'form': html_form
            }
            return data
        else:
            raise Http404 # pragma: no cover

    def form_edit(self, pk, model, form, str_url):
        if self.is_ajax():
            my_object = get_object_or_404(model, id=pk)
            html_form = render_to_string('components/partial_form.html',
                                         {'form_class': form(instance=my_object)}, request=self.request)
            data = {
                'action_url': reverse(str_url, kwargs={'pk': my_object.id}),
                'form': html_form
            }
            return data
        else:
            raise Http404  # pragma: no cover


class RoleMixin:

    def has_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()

    def get_role(self):
        user = self.request.user
        if self.has_group(user, 'manager'):
            return 'manager'
        elif self.has_group(user, 'user'):
            return 'user'
        return 'public'


class CustomPermissionRequiredMixin:
    permission_required = None  # str | list[str]
    permission_denied_message = "You do not have permission to perform this action."
    permission_redirect_url = None  # e.g., 'module_list' or any named url
    only_check_superuser = False
    check_superuser = False

    def has_permission(self):
        """Check if the user has the required permission(s)."""
        if not self.permission_required:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} requires `permission_required` to be set."
            )

        if isinstance(self.permission_required, (list, tuple)):
            return any(self.request.user.has_perm(perm) for perm in self.permission_required)
        if self.only_check_superuser:
            return self.request.user.is_superuser and self.request.user.has_perm(self.permission_required)
        elif not self.only_check_superuser and self.check_superuser:
            return self.request.user.is_superuser
        else:
            return self.request.user.has_perm(self.permission_required)

    def handle_no_permission(self):
        """Handle permission denial logic."""
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.get_permission_redirect_url())

    def get_permission_redirect_url(self):
        """Get redirect URL when permission denied."""
        return self.permission_redirect_url or self.request.META.get('HTTP_REFERER') or '/'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)