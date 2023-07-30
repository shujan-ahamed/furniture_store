from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from accounts.models import UserProfile
from marketplace.forms import ReviewForm
from marketplace.models import Category, Colour, Products, ReviewRating, Size, ProductVariation, Tax
from django.db.models import Max, Min

from orders.forms import CouponApplyForm, OrderForm

from django.db.models import Avg, Count

from orders.models import Coupon, Order, OrderProduct, Shipping
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta

# Create your views here.
def products(request, cat_slug=None):
    categories = None
    products = None

    if cat_slug!= None:
        category = get_object_or_404(Category, slug = cat_slug)
        products = Products.objects.filter(category = category).order_by('-created_at')
    else:
        products = Products.objects.all()

    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'products' : products,
    }
    return render(request, "marketplace/products.html", context)

def product_detail(request, category_slug , product_slug):
    product = Products.objects.get(category__slug = category_slug, slug = product_slug)
    related_products = Products.objects.filter(category__slug = category_slug).exclude(slug = product_slug)[:4]
    colours = ProductVariation.objects.filter(product= product).values('colour__id', 'colour__title', 'colour__colour_code').distinct()
    sizes = ProductVariation.objects.filter(product= product).values('size__id', 'size__title', 'price', 'discount_price', 'colour__id').distinct()
    

    if request.user.is_authenticated:
        try:
            orderedProduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        except:
            orderedProduct = None
    else:
        orderedProduct = None

    # Get the review 
    reviews = ReviewRating.objects.filter(product_id=product.id, status = True)

    

    review_form = ReviewForm()
    context = {
        'product' : product,
        'related_products' : related_products,
        'colours' : colours,
        'sizes' : sizes,
        'review_form' : review_form,
        'reviews' : reviews,
        'orderedProduct' : orderedProduct,
    }
    return render(request, "marketplace/product_detail.html", context)


def categories(request):
    total_products = Products.objects.count()
    products = Products.objects.all().order_by('-created_at')[:3]
    categories = Category.objects.all()
    sizes = Size.objects.all()
    colours = Colour.objects.all()
    min_max_price = ProductVariation.objects.all().aggregate(Min('price'), Max('price'))
    
    context = {
        'categories' : categories,
        'products' : products,
        'products_count' : total_products,
        'sizes' : sizes,
        'colours' : colours,
        'total_products' : total_products,
        'min_max_price' : min_max_price,
    }
    return render(request, "marketplace/categories.html", context)


def search(request):
    query = request.GET['query']
    products = Products.objects.filter(product_title__icontains = query).order_by('-created_at')

    context = {
        'products' : products,
    }
    return render(request, "marketplace/search.html", context)

def filter_data(request):
    colours = request.GET.getlist('colour[]')
    sizes = request.GET.getlist('size[]')
    categories = request.GET.getlist('category[]')
    min = request.GET['minPrice']
    max = request.GET['maxPrice']

    products = Products.objects.all().distinct()
    
    if len(colours)>0:
        products = products.filter(productvariation__colour__id__in = colours).distinct()
    if len(sizes)>0:
        products = products.filter(productvariation__size__id__in = sizes).distinct()
    if len(categories)>0:
        products = products.filter(category__id__in = categories).distinct()
        
    products = products.filter(productvariation__price__gte = min)
    products = products.filter(productvariation__price__lte = max)

    t = render_to_string('ajax/product_list.html',{
        'data' : products,
    })
    return JsonResponse({'data': t})


def load_more_products(request):
    ofset = int(request.GET['ofset'])
    limit = int(request.GET['limit'])

    products = Products.objects.all().order_by('-created_at')[ofset:ofset+limit]

    print(ofset , limit)
    
    t = render_to_string('ajax/product_list.html',{
        'data' : products,
    })
    return JsonResponse({'data': t})

@login_required(login_url='login')
def checkout(request):
    coupon_form = CouponApplyForm()
    sub_total = 0
    grand_total = 0
    total_tax = 0
    discount = 0
    coupon = None
    is_used = False
    coupon_id = None
    id = None
    ship_cost = 0
    ship = 0
    min_delivery = 0
    tax =0
    #get shipping cost from session via js ajax 
    try:
        id = request.GET['id']
        print('id', id)
        ship = Shipping.objects.get(id = id, available = True)
        request.session['shipping_cost'] = ship.cost
        request.session['shipping_method'] = ship.method
        ship_cost = ship.cost

        
    except:
        ship_cost = 0

    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            sub_total += int(item['price']) * float(item['qty'])

    print(sub_total)
    
    try:
        coupon_id  = request.session['coupon_id']
        print(coupon_id, request.session['coupon_id'])
        is_used = Order.objects.filter(user= request.user, coupon_id = coupon_id).exists()
        print(is_used)
        if is_used:
            coupon = Coupon.objects.get(id= coupon_id)
            discount = 0
        else:
            coupon = Coupon.objects.get(id= coupon_id)
            discount = (coupon.discount / 100) * sub_total
    except:
        discount = 0
    print(coupon)
    dis_sub_total = sub_total- discount
    print(sub_total)

    # CALCULATE  Tax
    
    get_tax = Tax.objects.filter(is_active = True)
    tax_dict = {}
    for i in get_tax:
        tax_type = i.tax_type
        percentage = float(i.tax_percentage)
        tax = round(dis_sub_total* percentage/100, 2)
        tax_dict.update({tax_type:{str(percentage):tax}})

    
    # calculate shipping
    shipping = Shipping.objects.filter(available = True)
    date_obj = datetime.now().date()
        
    for key,val in tax_dict.items():
        for i,j in val.items():
            total_tax +=j

    print(total_tax)
    #Calculate Total
    grand_total = dis_sub_total + total_tax + ship_cost
    print("grand_total",grand_total)

    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address_line_1': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
        
    }
    order_form = OrderForm(initial=default_values)
    print(type(sub_total))

    # tax_item.tax_percentage = float(tax.tax_percentage)

    context = {
        'order_form' : order_form,
        'cart_data':request.session['cartdata'],
        'sub_total': sub_total,
        'dis_sub_total' : dis_sub_total,
        'total_cart_items':len(request.session['cartdata']),
        "tax" : tax,
        "tax_dict" : tax_dict,
        'total_tax': total_tax,
        'grand_total' : grand_total,
        'coupon_form' : coupon_form,
        'coupon': coupon,
        'coupon_id' : coupon_id,
        'discount' : discount,
        'is_used' : is_used,
        'shipping' : shipping,
        'date_obj' : date_obj,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'grand_total': grand_total})
    else:
        return render(request, 'marketplace/checkout.html',context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        user = request.user
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            # messages.success(request, 'Your review has been updated.')
            JsonResponse({'data': 't'})
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()

                # messages.success(request, 'Your review has been submitted.')
        data ={ 
            'user' : user.first_name,
            'profile_pic' : user.profile.profile_picture.url, 
            'subject' : form.cleaned_data['subject'],
            'review' : form.cleaned_data['review'],
            'rating' : form.cleaned_data['rating'],
        }
        product = Products.objects.get(id = product_id, is_available = True)
        avarage_rat = ReviewRating.objects.filter(product=product).aggregate(average=Avg('rating'))
        total = ReviewRating.objects.filter(product=product).aggregate(count=Count('id'))
    return JsonResponse({'bool': 't', 'data': data, 'avarage_rat' : avarage_rat, 'total': total})
