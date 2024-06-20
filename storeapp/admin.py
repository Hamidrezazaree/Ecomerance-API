from django.contrib import admin
from .import models


admin.site.register(models.Products)

admin.site.register(models.Category)
admin.site.register(models.Review)
admin.site.register(models.Cart)
admin.site.register(models.Cartitem)


