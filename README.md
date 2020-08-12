Django E-Commerce
===================
an E-commerce website for clothes allow customers to order clothes online with visa or
Mastercard using stripe API ,save their address for the next purchase ,use promo code for
getting discount


Features
-------------
- Products
	- [X] Products are displayed on the home page with the ability to search by name and filter by category.
	- [X] Admin can CRUD Products using Django admin dashboard with the ability to search with names and filter products by categories
	- [X] products have 2 different labels that can be changed or removed by admin.
	- [X] products might have a discount price. 

- shopping cart
	- [X] shopping cart is made in the database instead of using session (although using session will give better performance)  to keep the items in the shopping cart for life until they removed or the order is made and to allow continuing the order from another device
	-  [X] Customers can add items in the shopping cart is it's not created it creates a new shopping cart and add this item 
	- [X] Customers can change the number of products ordered from the same item or remove it.


- Coupons
	- [X] customers can add cupon to have a discount on their order 
	- [X] Customer can use the coupon only N of times and the admin who created the coupons can determine That N.
	- [X]  admin can create coupons that can be used by specific customers only.

- Checkout and Payment
	- [X] Customers can't go to payment page unless they have items  in their shopping cart
	- [X] Customers fill their information and can save this information for the next order.
	- [X] customers choose payment method Stripe or Paypal (Paypal is not completed yet)
	- [X] when using stripe customers enters their card information then finish the checkout if the card number is wrong then a message is sent back to them displaying the error and if everything is fine then a success message is sent back and the order is payment is done using stripe API.

----------------------

Visuals
-------------

![alt_text](https://raw.githubusercontent.com/mena18/Django-Ecommerce/master/Screenshots/home_page.png)

----------

![alt_text](https://raw.githubusercontent.com/mena18/Django-Ecommerce/master/Screenshots/checkout_page.png)

----------

![alt_text](https://raw.githubusercontent.com/mena18/Django-Ecommerce/master/Screenshots/Payment.png)

----------

![alt_text](https://raw.githubusercontent.com/mena18/Django-Ecommerce/master/Screenshots/admin%20Dashboard.png)

----------




Prerequisites
-------------
Before you begin, ensure you have met the following requirements:

- you have installed python3.6 or above

-------------- 

Installation and usage
-------------

1- fork or download this repository and then open the folder in your CLI

2- install all the dependencies 

On Linux and macOS:
``` bash
pip3 install -r requirements.txt
```
On Windows:

``` bash
pip install -r requirements.txt
```

3- run migration to create the database

On Linux and macOS:
``` bash
python3 manage.py migrate
```
On Windows:

``` bash
python manage.py migrate
```

> **Notes:**

 > - you can use virtual environment "venv" if you want to install all the requirements inside virtual environment instead of installing them directly on your operating system you [click here for more inforation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
 
 >- please contact me if you have problems in the Installation process  


----------------------

Usage 
------------
 after installing all the requirements run the app

On Linux and macOS:
``` bash
python3 manage.py runserver
```
On Windows:

``` bash
python manage.py runserver
```
----------


open your browser and write that link to view the project
``` bash
http://127.0.0.1:8000/
```
to enter the admin dashboard : 


first, create a superuser in the terminal
``` bash
python3 manage.py createsuperuser
```
then login in the admin dashboard found here
``` bash
http://127.0.0.1:8000/admin
```

----------------------




Dependencies
-------------------


- Front End
	- Bootstrap 4
	- mdbootstrap


- Back End
	- Django 2
	- Pillow
	- django-allauth
	- django-countries
	- stripe

----------------------

Credits
--------------
credits go to [JustDjango](https://www.youtube.com/channel/UCRM1gWNTDx0SHIqUJygD-kQ) Youtube channel for the [tutorial](https://www.youtube.com/watch?v=z4USlooVXG0&list=PLLRM7ROnmA9F2vBXypzzplFjcHUaKWWP5) about building Django e-commerce 


