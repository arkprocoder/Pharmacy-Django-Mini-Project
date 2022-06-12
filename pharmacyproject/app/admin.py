from django.contrib import admin
from .models import Contact,Medicines,ProductItems,MyOrders
# Register your models here.
admin.site.register(Contact)
admin.site.register(Medicines)
admin.site.register(ProductItems)
admin.site.register(MyOrders)