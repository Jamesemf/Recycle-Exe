from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import barcode_form, product_form

import urllib.request
import json

from home.models import Statistic, Product


def barcode_lookup(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        #form = barcode_form(request.POST)
        barcode = request.POST.get("barcode")
        print("Value is ", barcode)

        try:
            Product.objects.get(barcode=form.cleaned_data('barcode'))
            return redirect('index')
        except:
            dict = api_lookup(form.cleaned_data('barcode'))
            material = dict['material']
            title = dict['title']
            weight = dict['weight']
            images = dict['images']
            category = dict['category']
            new_dict = {'type': material,
                        'name': title,
                        'weight': weight,
                        'image': images[0],
                        'category': category,
                        'barcode': form.barcode,
            }
            productForm = product_form(initial=new_dict)

            HttpResponse(render(request, 'BCscanner/Scanner_page.html', productForm))

            new_product = Product.objects.create(barcode=form.barcode,
                                                 title=title,
                                                 image=images[0],
                                                 type=category,
                                                 weight=weight)
            new_product.save()

    else:
        return HttpResponse(render(request, 'BCscanner/Scanner_page.html'))


def api_lookup(barcode):
    api_key = "5bcg2pbed762819eeppkc2qhjak1l4"
    url = "https://api.barcodelookup.com/v3/products?barcode=" + barcode + "&formatted=y&key=" + api_key
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print(data)
    print("\n")
    data = data["products"][0]
    return data
