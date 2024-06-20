from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from storeapp.models import Products, Category, Review, Cart, Cartitem, ProImage
from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProImage
        fields = ['id', 'product', 'image']

class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True, read_only= True)
    # uploded_images = serializers.ListField(
    #     child= serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
    #     write_only=True
    # )
    class Meta:
        model = Products
        fields = ['id','name','description','inventory', 'product_category']

        # 'old_price', 'price','product_category','slug','images','uploded_images'

    # def create(self, validated_data):
    #     uploded_images = validated_data.pop('uploded_images')
    #     product = Products.objects.create(**validated_data)
    #     for image in uploded_images:
    #         newproduct_image = ProImage.objects.create(product = product, image= image)
    #     return product

    # product_category = serializers.StringRelatedField()
    product_category = CategorySerializer()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date_created', 'name', 'description']

    # def create(self, validated_data):
    #     product_id = self.context["product_id"]
    #     product = Products.objects.get(id=product_id)
    #     review = Review.objects.create(
    #         product=product,
    #         **validated_data
    #     )
    #     return review
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = Cartitem
        fields = ['id', 'product', 'quantity','sub_total']

    def total(self, cartitem:Cartitem):
        return cartitem.quantity * cartitem.product.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    # global_total = serializers.SerializerMethodField(method_name='main_total')
    class Meta:
        model = Cart
        fields = ['id', 'items']

    # def main_total(self, cart:Cart):
    #     items = cart.items.all()
    #     total = sum([item.quantitiy * item.product.price for item in items])
    #     return total

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    def validate_product_id(self,value):
        if not Products.objects.filter(pk = value).exists():
            raise ValidationError('this id not exist')
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem= Cartitem.objects.get(product_id = product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            self.instance = cartitem
        except Cartitem.DoesNotExist:
            self.instance = Cartitem.objects.create(**self.validated_data, cart_id=cart_id)
    class Meta:
        model = Cartitem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitem
        fields = ['id', 'quantity']
