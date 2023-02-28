from django.shortcuts import render, redirect
from django.http import HttpResponse
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
        database_lookup(request)
    else:
        return render(request, 'BCscanner/Scanner_page.html')


def user_add_product_view(request):
    # we need to send the user to a page that contains a form
    # Ask the user for the weight and material of the product
    # Then add the product to the database
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        pass


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
        return HttpResponse(render(request, 'BCscanner/new_product_page.html'))
