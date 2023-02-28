from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import barcode_form, product_form
import urllib.request
import json
from home.models import Statistic, Product


def barcode_lookup(request):
    # If the user not log-in, redirect them to login page
    if not request.user.is_authenticated:
        return redirect('login')
    # If
    if request.method == 'POST':
        barcode_camera = request.POST.get("barcode")
        print("Value is ", barcode_camera)
        if Product.objects.filter(barcode=barcode_camera).exists():
            print("in db")
            product_data = Product.objects.get(barcode=barcode_camera)
            print(product_data)
            data_dict = {'Product': product_data}
            print(data_dict)
            return redirect('recycle_confirm')
            # redirect to product recycle page
        else:
            print("not in db")
            barcode = barcode_camera
            request.session['barcode'] = barcode
            return redirect('create_product')

    else:
        return render(request, 'BCscanner/Scanner_page.html')


def create_product(request):
    # we need to send the user to a page that contains a form
    # Ask the user for the weight and material of the product
    # Then add the product to the database
    print(request.method)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        request.session['barcode'] = ''
        print('Get Post')
        form = request.POST
        print("Made Form")
        new_product = Product.objects.create(
            barcode=form.get("barcode"),
            name=form.get("name"),
            type=form.get("type"),
            weight=form.get("weight"),
            category=form.get("category"),
        )
        print("temp_made")
        new_product.save()
        print("Saved")
        return redirect('recycle_confirm')
    if request.session['barcode']:
        barcode = {'barcode': request.session['barcode']}
        return render(request, 'BCscanner/new_product_page.html', barcode)


def success_submit(request):
    pass


def recycle_confirm(request):
    return HttpResponse("You Just submit it!")


def api_lookup(barcode):
    print("d")
    api_key = "5bcg2pbed762819eeppkc2qhjak1l4"
    url = "https://api.barcodelookup.com/v3/products?barcode=" + barcode + "&formatted=y&key=" + api_key
    print("j")
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print("l")
    print(data)
    print("\n")
    data = data["products"][0]
    return data


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