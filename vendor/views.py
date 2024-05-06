from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics 
from .models import Vendor,PurchaseOrder,HistoricalPerformance
from .serializers import VendorSerializer,PurchaseOrderSerializer,HistoricalPerformanceSerializer,AcknowledgeSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
@swagger_auto_schema(operation_id='GET Vendors List  or POST Vendor')
class VendorList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

@swagger_auto_schema(operation_id='GET/PUT/DELETE specific vendor with id')
class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


@swagger_auto_schema(operation_id='GET Purchase orders List  or POST Purchase Order')
class  PurchaseOrderList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
@swagger_auto_schema(operation_id='GET/PUT/DELETE specific  purchase order')
class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
@swagger_auto_schema(operation_id='GET vendor Performance metrics')
class VendorPerformance(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'vendor'
    def get_queryset(self):
        # Retrieve the latest historical performance record
        latest_metrics = HistoricalPerformance.objects.order_by('-date').first()
        return HistoricalPerformance.objects.filter(id=latest_metrics.id)
@swagger_auto_schema(operation_id='GET Vendor performance History over Time')
class VendorPerformanceHistory(generics.ListAPIView):
    queryset = HistoricalPerformance.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'vendor'

@swagger_auto_schema(operation_id='PUT purchase order Acknowledgement date ')
class PurchaseOrderAcknowledge(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgeSerializer




