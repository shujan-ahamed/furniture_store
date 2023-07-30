from django.urls import path
from .views import filter_data, products, product_detail, categories, search, load_more_products, checkout, submit_review


urlpatterns = [
    path('products/', products, name= 'products'),
    path('search/', search, name= 'search'),
    path('filter_data', filter_data, name= 'filter_data'),
    path('load_more_products', load_more_products, name= 'load_more_products'),
    path('products/<slug:cat_slug>/', products, name= 'categories'),
    path('product_by_categories/', categories, name= 'product_by_categories'),
    path('product_detail/<slug:category_slug>/<slug:product_slug>', product_detail, name= 'product_detail'),


    path('checkout/', checkout, name= 'checkout'),
    path('submit_review/<int:product_id>', submit_review, name="submit_review"),

]