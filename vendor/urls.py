from django.urls import path 
from .views import VendorList,VendorDetail,PurchaseOrderDetail,PurchaseOrderList,VendorPerformance,VendorPerformanceHistory,PurchaseOrderAcknowledge


urlpatterns = [
    path('vendors',VendorList.as_view(),name='vendors_list'),
    path('vendors/<int:pk>',VendorDetail.as_view(),name='vendor_detail'),
    path('purchase_orders',PurchaseOrderList.as_view(),name='purchase_orders_list'),
    path('purchase_orders/<int:pk>',PurchaseOrderDetail.as_view(),name="purchase_order_detail"),
    path('purchase_orders/<int:pk>/acknowledge',PurchaseOrderAcknowledge.as_view(),name="acknowledge"),
    path('vendors/<int:vendor>/performance',VendorPerformance.as_view(),name="performance"),
    path('vendors/<int:vendor>/performance/history',VendorPerformanceHistory.as_view(),name="history"),
]