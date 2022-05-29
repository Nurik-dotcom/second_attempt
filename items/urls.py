from django.urls import path
from .views import *


urlpatterns = [
#just pages
    path('search/', main, name='main'),
    path('', home, name='homepage'),
    path('<slug:slug>', category_products, name='category'),
    path('svoistva/<slug:slug>', svoisvtaProducts, name='svoistva'),
# Corsina Pages
    path('add_to_corsin/<int:pk>', add_to_corsina, name='add_corzina'),
    path('add_quantity/<int:pk>', add_quantite, name='add_quantite'),
    path('minus_quantity/<int:pk>', minus_quantite, name='minus_quantity'),
    path('remove_from_corsin/<int:pk>', remove_from_corsina, name='remove_corzina'),
    path('shop/corsina/', corsina_view, name='corsina'),

#Product
    path('item/<int:pk>', product_detail, name='product_detail'),


# Brand
    path('brand/<slug:slug>', brand_detail, name='brand_detail'),
    path('product_brand/<slug:slug>', brand_products, name='brand_products'),
    path('create_product/', create_product, name='create_product'),
    path('admin/<slug:slug>', show_unaviable_user, name='admin'),
    path('admin_product/<slug:slug>', show_unaviable_product, name='admin_product'),
    path('make_aviable/<int:pk>', make_aviable_user, name='make_user_aviable'),
    path('make_unaviable/<int:pk>', make_unaviable_user, name='make_user_unaviable'),
    path('admin_make_aviable/<int:pk>', admin_make_aviable_user, name='admin_make_user_aviable'),
    path('admin_make_unaviable/<int:pk>', admin_make_unaviable_user, name='admin_make_user_unaviable'),
    path('make_aviable_product/<int:pk>', make_aviable_product, name='make_aviable_product'),
    path('make_unaviable_product/<int:pk>', make_unaviable_product, name='make_unaviable_product'),
    path('become_member/<slug:slug>', become_member, name='become_member'),
    path('update_product/<int:pk>', update_product, name='update_product'),

# Shop
    path('create_product/', create_product_shop, name='create_product_shop'),
    path('delete_mag/<int:pk>', delete_product, name='delete_product'),
    path('update_for_shop/<int:pk>', update_product_in_shop, name='update_product_in_shop'),
    path('all_shops/', show_all_shop, name='all_shop'),
    path('shop_detail/<slug:slug>', shop_detail, name='shop_detail'),
    path('products/<slug:slug>', show_product_to_add, name='show'),
    path('add_product/<int:pk>/', shop_add_product, name='add_to_shop'),
    path('shop_products/<slug:slug>', show_shop_product, name='shop_product'),
    path('make_product_aviable/<int:pk>', make_in_showable, name='make_in_showable'),
    path('make_product_unaviable/<int:pk>', make_in_unshowable, name='make_in_unshowable'),
]