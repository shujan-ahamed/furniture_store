from django.shortcuts import render

from marketplace.models import Category, Products

def home(request):
    try:
        categories = Category.objects.all()
        products = Products.objects.filter(is_available = True, is_featured=True).order_by('-created_at')
    except:
        pass
    
    context = {
        'categories' : categories,
        'products' : products,
    }
    return render(request, 'home.html',context)

def about(request):
    
    return render(request, 'about.html')