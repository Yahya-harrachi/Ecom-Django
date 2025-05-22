from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
    
class Profile(View):
    def get(self, request):
        user_data = request.session.get('user')
        if not user_data:
            return redirect('/UserLogin')
        return render(request, 'Profile.html', {'user_data': user_data})

class add_to_cart(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get("quantity", 1))

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] = int(cart[str(product_id)]) + quantity
        else:
            cart[str(product_id)] = quantity

        request.session['cart'] = cart
        messages.success(request, "Produit ajouté au panier avec succès.")
        return redirect('/products/' + str(product_id))

        

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image_url': product.image.url,
                'total': round(product.price * quantity, 2),  #
            })

        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

class UpdateQuantityView(View):
    def post(self, request, product_id):
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        return redirect('cart')

class DeleteItemView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
        return redirect('cart')

class ClearCartView(View):
    def post(self, request):
        request.session['cart'] = {}
        return redirect('cart')
    
class ProcessCheckoutView(View):
    def post(self, request):
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        exp_date = request.POST.get('exp_date')
        cvv = request.POST.get('cvv')

        # For demo only — DO NOT store this in production!
        print("Payment Info:", card_name, card_number, exp_date, cvv)

        # Example order saving or confirmation message
        messages.success(request, "Payment processed (mock)! Order placed successfully.")
        request.session['cart'] = {}

        return redirect('checkout')
    
    
class Billing(View):
    def get(self, request):
        return render(request, "Billing.html")

class Success(View):
    def get(self, request):
        return render(request, "success.html")

    def post(self, request):
        cart = request.session.get('cart', {})
        if not cart:
            # Cart empty or missing
            return render(request, "empty_cart.html")

        out_of_stock_products = []

        # Iterate over all product ids in cart
        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            product = get_object_or_404(Product, pk=product_id)

            if product.countInStock >= quantity:
                product.countInStock -= quantity
                product.save()
            else:
                out_of_stock_products.append(product)

        if out_of_stock_products:
            return render(request, "out_of_stock.html", {"products": out_of_stock_products})

        # Clear cart after successful purchase
        request.session['cart'] = {}
        request.session.modified = True  # to ensure session save

        return redirect('success')  # redirect to success GET page
