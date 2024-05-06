from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Vendor, PurchaseOrder
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from django.db.models import Avg



User = get_user_model()

class VendorManagementTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('sign_up')
        self.login_url = reverse('token_obtain_pair')

        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpassword123'
        }
        #User Registration
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       #User Login
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        #extracting Access key
        self.access_token = login_response.data['access']
        #vendor creation 
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact', address='Address', vendor_code='123')
        #vedor data
        self.data = {
            'name': 'Vendor Name',
            'contact_details': 'Contact Details',
            'address': 'Vendor Address',
            'vendor_code': '123456'
        }
        #items data
        self.items = [
            {"name": "Item 1", "description": "Description of item 1", "quantity": 10, "unit_price": 20.50},
            {"name": "Item 2", "description": "Description of item 2", "quantity": 5, "unit_price": 15.75}
        ]
        #purchase order creation
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=4),
            items=self.items,
            quantity=15,
            status="pending",
            quality_rating=0,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )
        #purchase order data
        self.po_data = {
            "po_number": "PO002",
            "vendor": self.vendor.id, 
            "order_date": "2024-05-06T10:00:00",
            "delivery_date": "2024-05-10T10:00:00",
            "items": [
                {
                    "name": "Item 1",
                    "description": "Description of item 1",
                    "quantity": 10,
                    "unit_price": 20.50
                },
                {
                    "name": "Item 2",
                    "description": "Description of item 2",
                    "quantity": 5,
                    "unit_price": 15.75
                }
            ],
            "quantity": 15,
            "status": "pending",
            "quality_rating": 0,  
            "issue_date": "2024-05-06T10:00:00",  
            "acknowledgment_date": "2024-05-06T10:00:00"
        }
    # TEST 1 /api/vendors POST
    def test_create_vendor(self):
        url = reverse('vendors_list')
        response = self.client.post(url, self.data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor = Vendor.objects.get(name='Vendor Name')
        self.assertEqual(vendor.contact_details, 'Contact Details')
        self.assertEqual(vendor.address, 'Vendor Address')
        self.assertEqual(vendor.vendor_code, '123456')
        print("TEST-1 PASSED POST /api/vendors")


    #TEST 2 /api/vendors GET
    def test_get_vendors(self):
        url = reverse('vendors_list')
        response = self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Test Vendor')
        self.assertEqual(response.data[0]['contact_details'], 'Contact')
        self.assertEqual(response.data[0]['address'], 'Address')
        self.assertEqual(response.data[0]['vendor_code'], '123')

        print("TEST-2 PASSED GET /api/vendors")
    #TEST 3 /api/vendors/1 GET
    def test_get_vendor(self):
        vendor = self.vendor
        url = reverse('vendor_detail', kwargs={'pk': vendor.pk})
        response = self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')
        self.assertEqual(response.data['contact_details'], 'Contact')
        self.assertEqual(response.data['address'], 'Address')
        self.assertEqual(response.data['vendor_code'], '123')
        print("TEST-3 PASSED GET /api/vendors/vendor_pk")

    #TEST 4 /api/vendors/1 PUT
    def test_update_vendor(self):
        vendor = self.vendor
        url = reverse('vendor_detail', kwargs={'pk': vendor.pk})
        data = {
            'name': 'New Name',
            'contact_details': 'New Contact',
            'address': 'New Address',
            'vendor_code': '124'
        }
        response = self.client.put(url, data, format='json',HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=vendor.pk).name, 'New Name')
        self.assertEqual(Vendor.objects.get(pk=vendor.pk).contact_details, 'New Contact')
        self.assertEqual(Vendor.objects.get(pk=vendor.pk).address, 'New Address')
        self.assertEqual(Vendor.objects.get(pk=vendor.pk).vendor_code, '124')
        print("TEST-4 PASSED UPDATE /api/vendors/vendor_pk")

    
    #TEST 5 /api/vendors/1 DELETE
    def test_delete_vendor(self):
        vendor = self.vendor
        url = reverse('vendor_detail', kwargs={'pk': vendor.pk})
        response = self.client.delete(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)
        print("TEST-5 PASSED DELETE /api/vendors/vendor_pk")

    
    #TEST 6 /api/purchase_orders  POST
    def test_create_purchase_orders(self):
        url = reverse('purchase_orders_list')
        response = self.client.post(url, self.po_data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("TEST-6 PASSED POST /api/purchase_oders")

    
    #TEST 7 /api/purchase_orders GET
    def test_get_purchase_orders(self):
        url = reverse('purchase_orders_list')
        purchase_order = self.purchase_order
        response = self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, purchase_order.po_number)
        self.assertContains(response, str(purchase_order.vendor_id)) 
        self.assertContains(response, purchase_order.order_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.delivery_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.quantity)
        self.assertContains(response, purchase_order.status)
        self.assertContains(response, purchase_order.quality_rating)
        self.assertContains(response, purchase_order.issue_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.acknowledgment_date.strftime('%Y-%m-%dT%H:%M:%S'))
        print("TEST-7 PASSED GET /api/purchase_orders/")

    #TEST-8 /api/purchase_orders/1 GET
    def test_get_purchase_order(self):
        purchase_order = self.purchase_order
        url = reverse('purchase_order_detail', kwargs = {'pk': purchase_order.pk})
        response = self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, purchase_order.po_number)
        self.assertContains(response, str(purchase_order.vendor_id)) 
        self.assertContains(response, purchase_order.order_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.delivery_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.quantity)
        self.assertContains(response, purchase_order.status)
        self.assertContains(response, purchase_order.quality_rating)
        self.assertContains(response, purchase_order.issue_date.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertContains(response, purchase_order.acknowledgment_date.strftime('%Y-%m-%dT%H:%M:%S'))
        print("TEST-8 PASSED GET /api/purchase_orders/purchase_order_pk")

    #TEST-9 /api/purchase_orders/1 PUT
    def test_update_purchase_order(self):
        purchase_order = self.purchase_order
        url = reverse('purchase_order_detail', kwargs = {'pk': purchase_order.pk})
        po_updated_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id, 
            "items": [
                {
                    "name": "Item 1",
                    "description": "Description of item 1",
                    "quantity": 10,
                    "unit_priceurl" : 20.50
                },
                {
                    "name": "Item 2",
                    "description": "Description of item 2",
                    "quantity": 5,
                    "unit_price": 15.75
                }
            ],
            "quantity": 15,
            "status": "completed",
            "quality_rating": 5,     
        }
        response = self.client.put(url,po_updated_data,format='json',HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("TEST-9 PASSED PUT /api/purchase_orders/purchase_order_pk")
    #TEST-10 /api/purchase_orders/1 DELETE
    def test_delete_purchase_order(self):
        purchase_order = self.purchase_order
        url = reverse('purchase_order_detail', kwargs = {'pk': purchase_order.pk})
        response = self.client.delete(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)   

        print("TEST-10 PASSED DELETE /api/purchase_orders/purchase_order_pk") 

    
    #TEST-11 /api/purchase_orders/1/acknowledge PUT
    def  test_update_acknowledge(self):
        purchase_order = self.purchase_order
        url = reverse('acknowledge',kwargs = {'pk': purchase_order.pk})
        data = {
            "acknowledgment_date" : timezone.now() + timedelta(hours=4)
        }
        response = self.client.put(url,data,format='json',HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print("TEST-11 PASSED PUT /api/purchase_orders/purchase_orders_pk/acknowledge")


    #TEST-12 /api/vendors/1/performance GET
    def test_get_performance(self):
        vendor = self.vendor
        purchase_order_1 = PurchaseOrder.objects.create(
            po_number="PO011",
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=4),
            items=self.items,
            quantity=15,
            status="pending",
            quality_rating=0,
            issue_date=timezone.now(),
            acknowledgment_date=None, 
        )
        purchase_order_2 = PurchaseOrder.objects.create(
            po_number="PO012",
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items=self.items,
            quantity=10,
            status="pending",
            quality_rating=0,
            issue_date=timezone.now(),
            acknowledgment_date=None,  
        )
        data1 = { "status":'completed',
            "quality_rating":7,
            "acknowledgment_date":timezone.now() + timedelta(days=3)}
        data2 = { "status":'completed',
            "quality_rating":5,
            "acknowledgment_date":timezone.now() + timedelta(days=2)}
        po_url1 = reverse('purchase_order_detail', kwargs = {'pk': purchase_order_1.pk})
        po_url2 = reverse('purchase_order_detail', kwargs = {'pk': purchase_order_2.pk})
        

        update1 = self.client.put(po_url1,data1,format='json',HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update2 = self.client.put(po_url2,data2,format='json',HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        completed_orders = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=F('order_date'))
        on_time_delivery_rate = (on_time_orders.count() / completed_orders.count()) * 100 if completed_orders.count() else 0

        
        # Quality Rating Average
        completed_orders_with_rating = completed_orders.exclude(quality_rating=None)
        quality_rating_avg = completed_orders_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
        
        # Average Response Time
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / (24*3600) 
                          for po in completed_orders if po.acknowledgment_date]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Fulfilment Rate
        fulfilled_orders = completed_orders.exclude(acknowledgment_date=None)
        fulfillment_rate = (fulfilled_orders.count() / PurchaseOrder.objects.filter(vendor=vendor).count()) * 100 if PurchaseOrder.objects.filter(vendor=vendor).count() else 0

        
        
        url = reverse('performance', kwargs={'vendor': vendor.pk})
        response = self.client.get(url,HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Compare the response data with manually calculated metrics
        self.assertEqual(response.data['on_time_delivery_rate'], on_time_delivery_rate)
        self.assertEqual(response.data['quality_rating_avg'], quality_rating_avg)
        self.assertEqual(response.data['average_response_time'], average_response_time)
        self.assertEqual(response.data['fulfillment_rate'], fulfillment_rate)
        print("TEST-12 PASSED GET /api/vendors/1/performance")



