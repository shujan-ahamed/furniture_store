from django.http import JsonResponse
from django.shortcuts import render

from orders.models import Order, OrderProduct
from django.db.models import Sum, Avg, Count
import datetime
from django.utils import timezone

from django.db.models.functions import ExtractMonth

# def by_week_range(self, week_ago, number_of_weeks):
#     day_ago_start = week_ago * 7
#     day_ago_end = week_ago - (number_of_weeks * 7 )

#     now = timezone.now()
#     print(';',now)

#     start_date = now - datetime.timedelta(days=day_ago_start)
#     end_date = now -  datetime.timedelta(days=day_ago_end)
#     return self.by_range(start_date, end_date = end_date)

# def by_range(self, start_date, end_date=None):
#     if end_date is None:
#         return self.filter(updated_at__gte = start_date)
#     return self.filter(updated_at__gte = start_date, updated_at__lte = end_date)


def sales_ajax_data(request):
        data = {}
        if request.user.is_admin:
                qs = Order.objects.all()
                if request.GET.get('type') == 'week':
                        days = 7
                        start_date = timezone.now().today() - datetime.timedelta(days = days-1)
                        # print('strdt', start_date)
                        date_time_list = [] 
                        labels = []
                        saleItems = []
                        for x in range(0, days):
                                new_time = start_date + datetime.timedelta(days = x)
                                date_time_list.append(
                                       new_time
                                )
                                labels.append(
                                       new_time.strftime('%a')
                                )
                               
                                #last week data
                                qs = Order.objects.all().order_by('-created_at','-updated_at')
                                this_week = start_date
                                this_week_sales = qs.filter(updated_at__day = new_time.day, updated_at__month = new_time.month)
                                day_total = this_week_sales.aggregate(
                                Sum('order_total'),
                                        )['order_total__sum']
                                if day_total is None:
                                       day_total = 0
                                # print('this_week_sales',this_week_sales)
                                saleItems.append(
                                       day_total
                                )

                        data['labels'] = labels
                        data['data'] = saleItems

                #4weeks
                if request.GET.get('type') == '4weeks':
                        data['labels'] = ['Four weeks ago', 'three weeks ago', 'two weeks ago', 'Last week', 'this week']
                        data['data'] = []
                        current = 5
                        for i in range(0, 5):
                                day_ago_start = (current * 7)
                                day_ago_end = day_ago_start - (1 * 7 )
                                # print('start_date',day_ago_start)
                                # print('end_date',day_ago_end)
                                now = timezone.now().today()
                                start_date = now - datetime.timedelta(days=day_ago_start)
                                end_date = now -  datetime.timedelta(days=day_ago_end)
                                # print('start_date',start_date)
                                # print('end_date',end_date)

                                qs = Order.objects.all().order_by('-created_at','-updated_at')
                                if end_date is None:
                                        new_qs =  qs.filter(updated_at__gte = start_date)
                                else:
                                        new_qs = qs.filter(updated_at__gte = start_date, updated_at__lte = end_date)
                                # print('new_qs',new_qs)
                                sales_total = new_qs.aggregate(
                                Sum('order_total'),
                                        )['order_total__sum']
                                if sales_total is None:
                                       sales_total = 0
                                data['data'].append(sales_total)
                                current -=1
                                # print('data', data['data'])
                #month
                import calendar
                if request.GET.get('type') == 'month':
                        qs = Order.objects.all().annotate(month=ExtractMonth('updated_at')).values('month').annotate(count=Count('id')).values('month', 'count')
                        month_number = []
                        total_orders = []
                        for i in qs:
                                month = calendar.month_name[i['month']]
                                month_number.append(
                                        month
                                )
                                total_orders.append(
                                        i['count']
                                )
                        data['labels'] = month_number
                        data['data'] = total_orders
                        print('month_number', month_number)
                        print('total_orders', total_orders)
                                
        return JsonResponse(data)


def sales_data(request):
    qs = Order.objects.all().order_by('-created_at','-updated_at')
    #last week data
    this_week = timezone.now().today() - datetime.timedelta(days=6)
#     print('end_date',this_week)
    
    now = timezone.now().today()
    start_date = now - datetime.timedelta(days=7)
    end_date = now -  datetime.timedelta(days=0)
#     print('start_date',start_date)
#     print('end_date',end_date)
    
    recent_orders =  qs.filter(updated_at__gte = start_date, updated_at__lte = end_date)
    
#     print('recent_orders', recent_orders)
    shipped_orders = recent_orders.filter(status = 'shipped')
    paid_orders = recent_orders.filter(status = 'paid')
    cancel_orders = recent_orders.filter(status = 'Cancelled')
#     print(shipped_orders)


    # recent_orders_total = 0
    # for i in qs:
    #     recent_orders_total += i.order_total
    ordered_products = OrderProduct.objects.all()
    recent_total = recent_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    shipped_orders_total = shipped_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    paid_orders_total = paid_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    cancel_orders_total = cancel_orders.count()
    recent_products = ordered_products.aggregate(
                                Sum('quantity'),
                                )
    
    #Todays data
    today_data = timezone.now().date()

    today_data_orders = qs.filter(updated_at__gte = today_data)
#     print('today_data_orders', today_data_orders)
    today_data_shipped_orders = today_data_orders.filter(status = 'shipped')
    today_data_paid_orders = today_data_orders.filter(status = 'paid')
    today_data_cancel_orders = today_data_orders.filter(status = 'Cancelled')
    
    ordered_products = OrderProduct.objects.all()
    today_data_recent_total = today_data_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    today_data_shipped_orders_total = today_data_shipped_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    today_data_paid_orders_total = today_data_paid_orders.aggregate(
                                Sum('order_total'),
                                Avg('order_total'),
                                        )
    today_data_cancel_orders_total = today_data_cancel_orders.count()

    today_data_ordered_products = ordered_products.filter(updated_at__gte = today_data)
#     print('today_data_ordered_products', today_data_ordered_products)

    today_data_recent_products = today_data_ordered_products.aggregate(
                                Sum('quantity'),
                                )
    
    context = {
        'recent_orders' : recent_orders,
        'shipped_orders' : shipped_orders,
        'paid_orders' : paid_orders,
        'cancel_orders'  : cancel_orders,


        'recent_total' : recent_total,
        'recent_products' : recent_products,

        'shipped_orders_total' : shipped_orders_total,
        'paid_orders_total' : paid_orders_total,
        'cancel_orders_total' : cancel_orders_total,

        #today
        
        'today_data_orders' : today_data_orders,
        'today_data_shipped_orders' : today_data_shipped_orders,
        'today_data_paid_orders' : today_data_paid_orders,
        'today_data_cancel_orders'  : today_data_cancel_orders,


        'today_data_recent_total' : today_data_recent_total, 
        'today_data_shipped_orders_total' : today_data_shipped_orders_total,
        'today_data_paid_orders_total' : today_data_paid_orders_total,
        'today_data_cancel_orders_total' : today_data_cancel_orders_total,
        'today_data_recent_products' : today_data_recent_products,
    }
    return render(request, 'analytics/sales_data.html', context)