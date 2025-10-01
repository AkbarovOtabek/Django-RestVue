from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display=['name', 'slug']
  prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display=['category','name', 'slug','price', 'date_added',]
  list_filter = ['category','price','date_added']
  list_editable = ['price' ]
  prepopulated_fields = {'slug': ('name',)}
