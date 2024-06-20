from django_filters.rest_framework import FilterSet

from storeapp.models import Products


class ProductFilter(FilterSet):
    class Meta:
        model = Products
        fields = {
            'product_category': ['exact'],
            'old_price': ['gt', 'lt']
        }