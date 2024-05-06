from django.utils import timezone
from django.db.models import F
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import HistoricalPerformance
from datetime import datetime

def update_vendor_metrics(vendor):
    vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
    vendor.average_response_time = calculate_average_response_time(vendor)
    vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
    vendor.save()

def create_or_update_historical_performance(vendor):
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )

def calculate_on_time_delivery_rate(vendor):
    try:
        # Count the number of completed POs delivered on or before delivery_date
        on_time_delivery_count = vendor.purchaseorder_set.filter(status='completed', delivery_date__lte=F('order_date')).count()
        
        # Total number of completed POs for the vendor
        total_orders = vendor.purchaseorder_set.filter(status='completed').count()
        
        # Calculate the on-time delivery rate
        on_time_delivery_rate = (on_time_delivery_count / total_orders) * 100 if total_orders != 0 else 0
        return on_time_delivery_rate
    except ZeroDivisionError:
        return 0


def calculate_quality_rating_avg(vendor):
    completed_orders = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    total_quality_rating = completed_orders.aggregate(total=Coalesce(Sum('quality_rating'), 0))['total']
    total_orders = completed_orders.count()
    try:
        return total_quality_rating / total_orders
    except ZeroDivisionError:
        return 0

def calculate_average_response_time(vendor):
    completed_orders = vendor.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
    
    total_response_time = 0
    total_orders = 0
    
    for order in completed_orders:
        response_time = (order.acknowledgment_date - order.issue_date).total_seconds() / (24 * 3600)  # 
        total_response_time += response_time
        total_orders += 1
    try:
        return total_response_time / total_orders
    except ZeroDivisionError:
        return 0

def calculate_fulfillment_rate(vendor):
    try:
        total_orders = vendor.purchaseorder_set.count()
        successful_orders = vendor.purchaseorder_set.filter(status='completed').count()
        return (successful_orders / total_orders) * 100
    except ZeroDivisionError:
        return 0

