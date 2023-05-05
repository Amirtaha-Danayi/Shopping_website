from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug' : ('name',)}



@admin.register(Product)
class Productadmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ["price", "available"]
    prepopulated_fields = {'slug' : ('name',)}

