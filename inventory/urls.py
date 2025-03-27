from django.urls import path
from inventory.views import *
from inventory.templates import *

urlpatterns = [
    # path('', home, name='home'),
    path('', index, name='index'),
    path('category-register/', category_register, name='category_register'),
    path('user-register/', user_register, name='user_register'),
    path('product-register/', product_register, name='product_register'),

    path('list-products/',list_products_view,name="list_products_view"),
    path('list-categories/',list_category_view,name="list_category_view"),

    path('view-product/',view_product,name="view_product"),
    path('view-category/',view_category,name="view_category"),
    
    path('delete-category-view/',delete_category_view,name="delete_category_view"),
    path('delete-product-view/',delete_product_view,name="delete_product_view"),
    
    
]
