from django.contrib import admin
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from . import models

#Customize the Collection Table
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title'] 

    @admin.display(ordering='products')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id':str(collection.id) 
            }))
        return format_html('<a href="{}">{}</a>',url, collection.products_count)
        

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

# Customize the Order Table
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
   
# Customize the Customer Table
@admin.register(models.Customer)
class Customerdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
 
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory' 

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low ')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)



# Customize the Product Table
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price','inventory_status','collection_title']
    list_editable = ['unit_price'] 
    list_filter = ['collection', 'last_update']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


# Register your models here.
# admin.site.register(models.Collection)
