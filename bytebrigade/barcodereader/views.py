from django.shortcuts import render, redirect
import urllib.request
import json
from home.models import Transaction
from products.models import Product
from bins.models import BinData
from datetime import datetime
from account.views import addstats, update_goal_stat


def scanner_page_view(request):
    # If the user not log-in, redirect them to login page
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        barcode_product = request.POST.get("barcode")
        # We set the session barcode so that we can then use it in the other areas of the project
        request.session['barcode'] = barcode_product
        request.session['valid'] = 1
        if Product.objects.filter(barcode=barcode_product).exists():
            return redirect('product_info')
            # redirect to product recycle page
        else:
            return redirect('create_product')
    else:
        return render(request, 'BCscanner/Scanner_page.html')


def recycle_confirm_view(request):
    # This is function handles the user successfully getting to the bin
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        if not request.session['valid'] == 1:
            return redirect('index')
    except Exception as e:
        print(e)
        return redirect("index")
    try:
        print("a")
        barcode_product = request.session['barcode']
        bin_id = request.session['newHome']
        print(barcode_product)
        print(bin_id)
        if Product.objects.filter(barcode=barcode_product).exists() \
                and BinData.objects.filter(binId=bin_id).exists():
            product_data = Product.objects.get(barcode=barcode_product)
            user_data = request.user
            cur_time = (datetime.now()).strftime("%H:%M:%S")
            bin_data = BinData.objects.get(binId=bin_id)
            new_transaction = Transaction.objects.create(
                product=product_data,
                user=user_data,
                time=cur_time,
                bin=bin_data,
            )
            new_transaction.save()
            request.session['barcode'] = -1
            request.session['valid'] = -1
            request.session['newHome'] = -1
            # Call a function that will take in the calculate the points for the user
            # If the product is new add points, this is handle in the create product part
            weight = product_data.weight
            points = round(weight * 122)
            addstats(request.user, product_data, points, weight)  # need to include the product
            update_goal_stat(request.user, product_data)
    except Exception as e:
        print(e)
    return redirect("index")


def database_lookup(request):
    print(request.POST)
    barcode_camera = request.POST.get("barcode")
    print("Value is ", barcode_camera)
    if Product.objects.filter(barcode=barcode_camera).exists():
        print("in db")
        product_data = Product.objects.get(barcode=barcode_camera)
        print(product_data)
    else:
        print("not in db")
