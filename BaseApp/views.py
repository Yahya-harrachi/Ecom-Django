from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.hashers import check_password

from django.contrib import messages
from .forms import ProductForm
from .forms import UsersForm
from .models import Product
from .models import Users
# Create your views here.

# class Home(View):
#     def get(self,Request):
#         return render(Request, "home.html")

# ADMIN
    
class ProductList(View):
    def get(self, Request):
        products = Product.objects.all()
        return render(Request, 'ProductsList.html', {'products': products})

class ProductDetail(View):
    def get(self, request, productId):
        product = Product.objects.get(id=productId)
        return render(request, 'ProductDetail.html', {'product': product})
    
class AddProduct(View):
    def get(self, request):
        form = ProductForm()
        return render(request, "AddProduct.html", {'form': form})

    def post(self, request):
        # product_name = request.POST.get('name')
        # product_category = request.POST.get('category')
        # product_brand = request.POST.get('brand')
        # product_description = request.POST.get('description')
        # product_stockQte = request.POST.get('stockQte')
        # product_price = request.POST.get('price')
        # product_image = request.POST.get('image')
        # new_product = Product(name = product_name, brand = product_brand, category = product_category,
        #                       description = product_description, countInStock = product_stockQte, price = product_price, image = product_image)
        # new_product.save()
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/administration/products')
        return render(request, 'AddProduct.html', {'form': form})

class ModifyProduct(View):
    def get(self, request, productId):
        product = Product.objects.get(id=productId)
        form = ProductForm(instance=product)
        return render(request, "ModifyProduct.html", { 'form' : form})
    
    def post(self, request, productId):
        product = Product.objects.get(id=productId)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/administration/products')
        return render(request, 'ModifyProduct.html', {'form' : form})
        
class DeleteProduct(View):
    def get(self, request, productId):
        product = Product.objects.get(id=productId)
        product.delete()
        return redirect('/administration/products')
    

# USER

class BaseURL(View):
    def get(self, request):
        products = Product.objects.all()
        user = request.session.get('user')
        if user:
            print("Logged-in user:", user["username"])
        else:
            print("No user is logged in")
        return render(request, "base.html", { 'products': products})

class UserProductsList(View):
    def get(self, request):
        category = request.GET.get('category')

        products = Product.objects.all()
        if category:
            products = products.filter(category=category)

        categories = Product.objects.values_list('category', flat=True).distinct()

        return render(request, 'UserProductsList.html', {
            'products': products,
            'categories': categories,
            'selected_category': category,
        })

class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"[LOGIN ATTEMPT] Username: {username}")

        try:
            user = Users.objects.get(username=username)
            if user.password.strip() == password.strip():
                request.session['user'] = {
                    "username": user.username,
                    "email": user.email,
                }
                print(f"\n\n[LOGIN SUCCESS] {user.username} logged in.")
                return redirect("/")
            else:
                messages.error(request, "Invalid password")
        except Users.DoesNotExist:
            print(f"[LOGIN FAILED] User '{user.username}' not found")
            messages.error(request, "User not found")

        return render(request, "login.html")
    

class CreateAcc(View):
    def get(self, request):
        return render(request, "CreateAcc.html")
    
    def post(self, request):
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'CreateAcc.html', {'form': form})

class Logout(View):
    def get(self, request):
        request.session.flush()  
        return redirect("/") 