from rest_framework import serializers
from .models import Vendor,PurchaseOrder,HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','name','contact_details','address','vendor_code')
        model = Vendor

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']
        model = PurchaseOrder



class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['vendor','date','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']
        model = HistoricalPerformance


class AcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id','acknowledgment_date']
        read_only_fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date']



