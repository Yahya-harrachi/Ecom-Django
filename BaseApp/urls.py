from django.shortcuts import render
from django.urls import path
from . import views
urlpatterns = [
  # path("home/", views.Home.as_view(), name="home"),
  path("", views.BaseURL.as_view(), name="BaseURL"),
  path("products/", views.UserProductsList.as_view(), name="UserProductsList"),
  path("UserLogin/",views.Login.as_view(), name="Login"),
  path("CreateAccount/",views.CreateAcc.as_view(), name="CreateAcc"),
  path("UserLogout",views.Logout.as_view()),
  path("Profile", views.Profile.as_view(), name="Profile"),
  path('add-to-cart/<int:product_id>/', views.add_to_cart.as_view(), name='add_to_cart'),
  path('cart/', views.CartView.as_view(), name='cart'),
  path('cart/update/<int:product_id>/', views.UpdateQuantityView.as_view(), name='update_quantity'),
  path('cart/delete/<int:product_id>/', views.DeleteItemView.as_view(), name='delete_item'),
  path('cart/clear/', views.ClearCartView.as_view(), name='clear_cart'),
  path('checkout/', views.ProcessCheckoutView.as_view(), name='checkout'),
  path('Billing/', views.Billing.as_view(), name='Billing'),
  path('success/', views.Success.as_view(), name='success'), 
  path('About/', views.About.as_view(), name='About'),
  
  # ADMIN
  path('administration/products', views.ProductList.as_view(), name='ProductsList'),  
  path('administration/dashboard', views.Dashboard.as_view(), name='dashboard'),
  path('products/<int:productId>', views.ProductDetail.as_view(), name='ProductDetail'),
  path('AddProduct', views.AddProduct.as_view(), name="AddProduct"),
  path('ModifyProduct/<int:productId>', views.ModifyProduct.as_view(), name="ModifyProduct"),
  path('DeleteProduct/<int:productId>', views.DeleteProduct.as_view(), name='DeleteProduct'),

]
