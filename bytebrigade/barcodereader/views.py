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
        form = barcode_form(request.POST)
        # Cams code to get the dictionary


        #  Check if the product is already in the database
        #  Assumption that if in the database we have all the data for the product
        try:
            Product.objects.get(barcode=form.barcode)
            return redirect('index')
        except:
            dict = api_lookup(form.barcode)
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


