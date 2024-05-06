from django.contrib import admin
from .models import Vendor,HistoricalPerformance,PurchaseOrder

# Register your models here.
admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)
admin.site.register(PurchaseOrder)

