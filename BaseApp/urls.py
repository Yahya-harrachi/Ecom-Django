from django.urls import path
from . import views
urlpatterns = [
  # path("home/", views.Home.as_view(), name="home"),
  path("", views.BaseURL.as_view(), name="BaseURL"),
  path('Admin/products/', views.ProductList.as_view(), name='ProductsList'),
  path('products/<int:productId>', views.ProductDetail.as_view(), name='ProductDetail'),
  path('AddProduct', views.AddProduct.as_view(), name="AddProduct"),
  path('ModifyProduct/<int:productId>', views.ModifyProduct.as_view(), name="ModifyProduct"),
  path('DeleteProduct/<int:productId>', views.DeleteProduct.as_view(), name='DeleteProduct')
  
  # ADMIN
  

]
