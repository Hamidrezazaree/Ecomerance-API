from django.urls import path, include
from . import views
from .views import ProductsListCreat, ProductRUD

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
router = routers.DefaultRouter()
router.register('products', views.Products)
router.register('categories', views.Categories)
router.register('carts',views.CartMixinView)

product_router = routers.NestedDefaultRouter(router,'products', lookup='product')
product_router.register('reviews', views.ReviewViewSets, basename="product-review")

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewsets, basename='')


urlpatterns = router.urls

urlpatterns = [
      path('',include(product_router.urls)),
      path('',include(router.urls)),
      path('',include(cart_router.urls)),
#     path('products',views.api_products, name= 'products_list'),
#     path('product/<int:pk>/',views.api_product, name='single_product'),
#     path('category/<int:pk>/',views.category, name='single_category'),
#     path('categories',views.categories, name='categories'),
#     path('productsgeneric',ProductsListCreat.as_view(), name='products'),
#     path('productsrud/<int:pk>',ProductRUD.as_view(), name='productsrud'),
]
