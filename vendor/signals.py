from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor, HistoricalPerformance
from .utils import update_vendor_metrics, create_or_update_historical_performance

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_and_performance(sender, instance, created, **kwargs):
    if not created:
        update_vendor_metrics(instance.vendor) 
        create_or_update_historical_performance(instance.vendor)


