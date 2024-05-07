# Vendor Management System 

The Vendor Management System (VMS) API provides functionalities for managing vendor profiles, purchase orders, and real-time vendor performance metrics. This documentation outlines the endpoints and their functionalities.


-[Installation](#installation)

-[Testing](#testing)

-[API Endpoints](#apiendpoints)

-[API Documentation](#api-documentation)



## Installation

To run the API on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Deepak3168/Vendor-Management-System.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

Now, the API should be up and running locally on your machine. You can access it using the provided endpoints.

## Testing

To test user authentication, run the following command:

```bash
python manage.py test users
```

To test the API endpoints and functionality, execute the following command:

```bash
python manage.py test vendor
```

This will run the test suite for the Vendor Management System API and ensure that all endpoints and functionalities are working as expected.


## API Endpoints

### Authentication

**1. Register User**

- **POST:** http://127.0.0.1/api/register/
  - **Description:** Register a new user.
  - **Request Body:** JSON containing the following fields:
    - `name`: Name of the user.
    - `email`: Email address of the user.
    - `password`: Password for the user account.
  - **Response:** JSON containing user ID, name, and email.

**2. Login**

- **POST:** http://127.0.0.1/api/login/
  - **Description:** Login to the system.
  - **Request Body:** JSON containing the following fields:
    - `email`: Email address of the user.
    - `password`: Password for the user account.
  - **Response:** JSON containing access token and refresh token.

**3. Logout**

- **POST:** https://127.0.0.1/api/logout/
  - **Description:** Logout from the system.
  - **Request Body:** JSON containing the refresh token.
  - **Response:** Successful logout.

### Vendor

**1. List Vendors**

- **GET:** http://127.0.0.1/api/vendors/
  - **Description:** Get a list of all vendors.
  - **Requires Authentication:** Yes

**2. Create Vendor**

- **POST:** http://127.0.0.1/api/vendors/
  - **Description:** Create a new vendor.
  - **Request Body:** JSON containing the following fields:
    - `name`: Name of the vendor.
    - `vendor_id`: ID of the vendor.
    - `contact_details`: Contact details of the vendor.
    - `address`: Address of the vendor.
  - **Response:** JSON containing the created vendor details.

**3. Get Vendor**

- **GET:** http://127.0.0.1/api/vendors/1/
  - **Description:** Get details of a specific vendor.

**4. Update Vendor**

- **PUT:** http://127.0.0.1/api/vendors/1/
  - **Description:** Update details of a specific vendor.
  - **Request Body:** JSON containing the fields to be updated.
  - **Response:** JSON containing the updated vendor details.

**5. Delete Vendor**

- **DELETE:** http://127.0.0.1/api/vendors/1/
  - **Description:** Delete a specific vendor.

**6. List Purchase Orders**

- **GET:** http://127.0.0.1/api/vendors/1/purchase_orders/
  - **Description:** Get a list of all purchase orders for a specific vendor.

**7. Create Purchase Order**

- **POST:** http://127.0.0.1/api/vendors/1/purchase_orders/
  - **Description:** Create a new purchase order for a specific vendor.
  - **Request Body:** JSON containing the following fields:
    - `po_number`: CharField - Unique number identifying the PO.
    - `vendor`: ForeignKey - Link to the Vendor model.
    - `order_date`: DateTimeField - Date when the order was placed.
    - `delivery_date`: DateTimeField - Expected or actual delivery date of the order.
    - `items`: JSONField - Details of items ordered.
    - `quantity`: IntegerField - Total quantity of items in the PO.
    - `status`: CharField - Current status of the PO (e.g., pending, completed, canceled).
    - `quality_rating`: FloatField - Rating given to the vendor for this PO (nullable).
    - `issue_date`: DateTimeField - Timestamp when the PO was issued to the vendor.
    - `acknowledgment_date`: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.
  - **Response:** JSON containing the created purchase order details.

**8. Get Purchase Order**

- **GET:** http://127.0.0.1/api/vendors/1/purchase_orders/1/
  - **Description:** Get details of a specific purchase order for a specific vendor.

**9. Update Purchase Order**

- **PUT:** http://127.0.0.1/api/vendors/1/purchase_orders/1/
  - **Description:** Update details of a specific purchase order for a specific vendor.
  - **Request Body:** JSON containing the fields to be updated.
  - **Response:** JSON containing the updated purchase order details.

**10. Delete Purchase Order**

- **DELETE:** http://127.0.0.1/api/vendors/1/purchase_orders/1/
  - **Description:** Delete a specific purchase order for a specific vendor.

**11. Acknowledge Purchase Order**

- **PUT:** http://127.0.0.1/api/purchase_orders/1/acknowledge/
  - **Description:** Acknowledge a specific purchase order for a specific vendor.

**12. Get Vendor Performance Metrics**

- **GET:** http://127.0.0.1/api/vendors/1/performance/
  - **Description:** Get performance metrics for a specific vendor.

## API Documentation

Explore the API endpoints further and understand their usage in detail:

- **Swagger UI (Local)**: [http://127.0.0.1/api/swagger](http://127.0.0.1/api/swagger)
- **ReDoc (Local)**: [http://127.0.0.1/api/redoc](http://127.0.0.1/api/redoc)

You can also access the API documentation for the deployed version on Render:

- **Swagger UI (Render)**: [https://vendor-management-system-dwtp.onrender.com/api/swagger/](https://vendor-management-system-dwtp.onrender.com/api/swagger/)
- **ReDoc (Render)**: [https://vendor-management-system-dwtp.onrender.com/api/redoc/](https://vendor-management-system-dwtp.onrender.com/api/redoc/)

These documentation links provide comprehensive information about the available endpoints, request parameters, and response formats.


