from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, OrderItem, Order, Collection
from django.db import transaction


# PERMING RAW QUERY
def say_hello(request):
    queryset = Product.objects.raw('SELECT * FROM store_product')


    return render(request, 'hello.html', {'name': 'Cathbert', 'results': list(queryset)})


# PERFOMING TRANSACTIONS
# def say_hello(request):
#     order = Order()

#     with transaction.atomic():
#         order = Order()
#         order.customer_id = 1
#         order.save()

#         item = OrderItem()
#         item.order = order
#         item.product_id= 1
#         item.quantity = 1
#         item.unit_price=10
#         item.save()

#     return render(request, 'hello.html', {'name': 'Cathbert'})

#def say_hello(request):
    
    # DELETING
    # collection = Collection(pk=11)
    # collection.delete()

    # Collection.objects.filter(id__gt=5).delete()


    #    INSERTING
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    #   UPDATING
    #METHOD 1 but if you don't specify all columns it will make them null

    # collection = Collection(pk=11)
    # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()
    
    #METHOD 2 but its reduces perfomance as you to query before updating
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    #METHOD 3 you can update by calling the update constractor in the collection
    #Collection.objects.filter(pk=11).update(featured_product=None)


     #    QUERYNG     
    #result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
    #queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # queryset = OrderItem.objects.select_related('product').prefetch_related('order').order_by('id').all()
    # queryset = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # queryset = Product.objects.select_related('collection').all()
    # queryset = Product.objects.only('id','title')
    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product_id').distinct()).order_by('title') 
    
    # queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
   
    #return render(request, 'hello.html', {'name': 'Cathbert'})
 