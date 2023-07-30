from django.shortcuts import get_object_or_404, render, redirect

from accounts.models import User, UserProfile
from accounts.utils import send_activation_mail, send_varification_email
from marketplace.models import Products, WishList
from orders.models import Order
from .forms import User_Profile_Form, UserInfoForm
from django.contrib import auth
from django.contrib import messages
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

#Varification Mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.http import JsonResponse

import requests

# Create your views here.
def registerUser(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(first_name = first_name, last_name= last_name, username = username, email=email, password=password)
            user.save()
            send_activation_mail(request, user)
            messages.success(request, "Regidtrattion successfull, Please go tot the link to activate youjr account.")

            return redirect('registerUser')

        else:
            messages.error(request, "Invailed form.")
            print(form.errors)
    else:
        form = UserRegistrationForm()
    
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You have successfully logged in.")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                param = dict(x.split('=') for x in query.split('&'))
                if 'next' in param:
                    nextPage = param['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, "Invailed creadentials.")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.error(request, "Logged out.")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated.')
        return redirect('login')

    else:
        messages.error('invailed activation link')
        return redirect('register')

def dashboard(request):
    orders = Order.objects.filter(user = request.user, is_ordered = True)
    recent_orders = orders[:5]
    order_count = orders.count()

    context = {
        'orders' : recent_orders,
        'order_count' : order_count,
    }
    
    return render(request, "accounts/dashboard.html", context)

def my_orders(request):
    orders = Order.objects.filter(user = request.user, is_ordered = True).order_by('-created_at')

    context = {
        'orders' : orders,
    }
    return render(request, "accounts/my_orders.html", context)

def profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)    
    if request.method == "POST":
        profile_form = User_Profile_Form(request.POST, request.FILES, instance = profile)
        user_form = UserInfoForm(request.POST, instance= request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = User_Profile_Form(instance = profile)
        user_form = UserInfoForm(instance= request.user)
        
    context = {
        'profile_form' : profile_form,
        'user_form' : user_form,
        'profile' : profile,
    }
    return render(request, "accounts/profile.html",context)

def wishlist(request):
    wish_list = WishList.objects.filter(user = request.user)


    context = {
        'wish_list' : wish_list,
    }
    return render(request, "accounts/wish_list.html",context)

def addto_wish_list(request, product_id):
    product = Products.objects.get(id = product_id)
    wishlist_exist = WishList.objects.filter(user = request.user, product = product).exists()

    if wishlist_exist:
        return JsonResponse({'status': 'error','message': 'Product already in the wish list.'})
    else:
        wishlist = WishList.objects.create(product= product,user= request.user)
        wishlist.save()
        return JsonResponse({'status': 'success','message': 'Added to the wish list.'})


@login_required(login_url = 'login')
def change_password(request):
    if request.method == "POST":
        currnt_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact = request.user.username)
        if new_password == confirm_password:
            success = user.check_password(currnt_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your Password has been updated succesfully.')
                #auth.logout()
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password.')
                return redirect('change_password')
        else:
            messages.error(request, "Password doesn't match")
            return redirect('change_password')
            
    return render(request, 'accounts/change_password.html')


#reset password
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please, reset your password.')
        return redirect('reset_password')
    else:
        messages.error('This link has been expaired.')
        return redirect('myAccount')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user  = User.objects.filter(email=email).exists()

        if user:
            user = User.objects.get(email__exact = email)
            
            #send reset password mail
            mail_subject = 'Please, reset your password by going to the below link.'
            email_template = 'accounts/emails/reset_password_varification_email.html'

            send_varification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent.Please, check your mail.")
            return redirect('forgot_password')
        else:
            messages.error(request, "Sorry, unknown email.")
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk = pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Your password has been updated successfully.")
            return redirect('login')
        else:
            messages.error(request, "password doesn't match!")
            return render(request, 'accounts/reset_password.html')

    else:
        return render(request, 'accounts/reset_password.html')
