from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from api.filters import ProductFilter
from api.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, UpdateCartItemSerializer
from storeapp.models import Products, Category, Review, Cart, Cartitem
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin


@api_view(['GET','POST'])
def api_products(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True )
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
@api_view(['GET','PUT','DELETE'])
def api_product(request,pk):
    if request.method == 'GET':
        product = get_object_or_404(Products,id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Products, id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        product = get_object_or_404(Products, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view()
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
@api_view()
def category(request,pk):
    category = get_object_or_404(Category,id = pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
class ProductsListCreat(ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
class ProductRUD(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # def get_queryset(self):   --->  = queryset

class Products(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['product_category', 'old_price']
    filterset_class = ProductFilter
    search_fields = ['name','description']
    ordering_fields = ['old_price']
    pagination_class = PageNumberPagination

class Categories(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSets(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

class CartMixinView(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewsets(ModelViewSet):
    queryset = Cartitem.objects.all()
    serializer_class = CartItemSerializer

    def get_serializer_class(self):
        http_method_names = ['get', 'post', 'patch', 'delete']
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


