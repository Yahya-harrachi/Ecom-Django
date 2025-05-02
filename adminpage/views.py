from django.contrib.auth.decorators import login_required, user_passes_test 
from django.shortcuts import render 
def is_admin(user): 
    return user.is_superuser   

@login_required 
@user_passes_test(is_admin) 
def dashboard(request): 
    return render(request, 'dashboard.html')