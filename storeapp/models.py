from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    discount = models.BooleanField(default=False, verbose_name='تخفیف')
    image = models.ImageField(upload_to='product_image',null=True,blank=True,verbose_name='تصویر محصول')
    old_price = models.FloatField(default=99.99, verbose_name='قیمت اصلی')
    product_category = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True, blank=True,verbose_name='دسته بندی')
    slug = models.SlugField(default=None)
    inventory = models.IntegerField(default=0, verbose_name='موجودی')
    top_deal = models.BooleanField(default=False)
    flash_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def price(self):
        if self.discount:
            new_price = self.old_price - ((30/100) * self.old_price)
        else:
            new_price = self.old_price
        return new_price

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(default=None)
    featured_product = models.OneToOneField(Products, on_delete=models.CASCADE, null=True, blank=True)
    icon = models.CharField(max_length=100, default=None, null=True, blank=True)


    def __str__(self):
        return self.title

class Review(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    date_created = models.DateTimeField(auto_now_add= True)
    description = models.TextField()


    def __str__(self):
        return self.description

class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class Cartitem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey('products', on_delete=models.CASCADE, related_name = 'cartitem', null = True, blank = True)
    quantity = models.IntegerField(default=0)


class ProImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='img', null=True, blank=True, default="")




