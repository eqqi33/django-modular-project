from django.urls import path
from .views import (
    ProductListView,
    ProductDeleteView,
    ProductCreateView,
    ProductUpdateView,
    ProductExportCSVView,
    ProductExportExcelView,
)

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_landing'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/export/csv/', ProductExportCSVView.as_view(), name='product_export_csv'),
    path('product/export/excel/', ProductExportExcelView.as_view(), name='product_export_excel'),
]
