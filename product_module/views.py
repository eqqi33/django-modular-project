import csv
import openpyxl
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from engine.mixin import AjaxResponseMixin, CustomPermissionRequiredMixin
from .forms import ProductForm
from .models import Product


class ProductListView(LoginRequiredMixin, CustomPermissionRequiredMixin, ListView):
    model = Product
    template_name = 'product_module/product_list.html'
    paginate_by = 10
    permission_required = 'product.view_product'
    permission_redirect_url = 'no_permission'

    def check_has_perm(self, access):
        user = self.request.user
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        return user.has_perm(f'{app_label}.{access}_{model_name}')

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')
        order_prefix = '' if order == 'asc' else '-'

        qs = Product.objects.filter(
            Q(name__icontains=query) | Q(barcode__icontains=query)
        ).order_by(f'{order_prefix}{sort}')

        stock_filter = self.request.GET.get('stock')
        if stock_filter == 'empty':
            qs = qs.filter(stock=0)
        elif stock_filter == 'low':
            qs = qs.filter(stock__lt=10)

        price_filter = self.request.GET.get('price')
        if price_filter == 'high':
            qs = qs.order_by('-price')
        elif price_filter == 'low':
            qs = qs.order_by('price')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Hak akses user
        user = self.request.user
        context['can_view'] = self.check_has_perm('view')
        context['can_add'] = self.check_has_perm('add')
        context['can_change'] = self.check_has_perm('change')
        context['can_delete'] = self.check_has_perm('delete')
        context['can_export'] = self.check_has_perm('export')
        context['can_search'] = self.check_has_perm('search')

        context['query'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', 'name')
        context['order'] = self.request.GET.get('order', 'asc')
        return context


class ProductCreateView(LoginRequiredMixin, AjaxResponseMixin, CustomPermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'product.add_product'
    permission_redirect_url = 'no_permission'

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.form_add(form=self.form_class,str_url='product_add'))

    def get_success_url(self):
        messages.success(self.request, "Data Product created successfully.")
        return reverse('product_landing')


class ProductUpdateView(LoginRequiredMixin, AjaxResponseMixin, CustomPermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'product.change_product'
    permission_redirect_url = 'no_permission'

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.form_edit(pk=int(kwargs['pk']),
                                           model=self.model,
                                           form=self.form_class,
                                           str_url='product_edit'))

    def get_success_url(self):
        messages.success(self.request, "Data Product updated successfully.")
        return reverse('product_landing')


class ProductDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'product.delete_product'
    permission_redirect_url = 'product_landing'

    def get_success_url(self):
        messages.success(self.request, "Data Product deleted successfully.")
        return reverse('product_landing')


class ProductExportCSVView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = 'product.export_product'
    permission_redirect_url = 'product_landing'

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=products.csv'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Barcode', 'Price', 'Stock'])

        for p in Product.objects.all():
            writer.writerow([p.name, p.barcode, p.price, p.stock])

        return response


class ProductExportExcelView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    permission_required = 'product.export_product'
    permission_redirect_url = 'product_landing'

    def get(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products"
        ws.append(['Name', 'Barcode', 'Price', 'Stock'])

        for p in Product.objects.all():
            ws.append([p.name, p.barcode, float(p.price), p.stock])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        wb.save(response)
        return response