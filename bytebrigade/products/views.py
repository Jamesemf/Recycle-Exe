from django.shortcuts import render, redirect
from .models import Product
from account.views import addstats
from bins.views import withinRange
from home.models import Transaction
from django.db.models import Q
import json
import urllib.request
import urllib.parse


def product_dex(request):
    """
    Web backend for '../product/dex/' (name 'product_dex')
    
    This function creates an information page on the number of every product that a user has binned
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        request.session['pokedex_barcode'] = request.POST.get('barcode')
        return redirect('product_info')

    # Data is all transactions from the current user
    data = Transaction.objects.filter(Q(user=request.user))
    # Create a dictionary of unique items that appear in transaction and keep a count
    items = {}
    for obj in data:
        key = obj.product
        if key not in items.keys():
            items[key] = 1
        else:
            items[key] +=1

    product_count = {
        'product': items
    }
    return render(request, 'products/pokedex.html', product_count)  #  Render pokedex page

def create_product_view(request):
    """
    Web backend for'../product/create)' (name 'create_product')

    This view handles the product creation page. When the user scans a product if the product is not in the database
    we then ask the user to fill out a form about this product. If the request is a get request we load the page containing
    the product form. When a post request occurs we collect the product information and add it to the database.

    The page will automatically contain the barcode which the user has scanned.

    Return:
        Nothing, but a product is added to the db
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = request.POST
        new_product = Product.objects.create(
            barcode=form.get("barcode"),
            name=form.get("name"),
            weight=float(form.get("weight")) / 1000,
            material=form.get("material"),
            recycle=form.get("recycle"),
            image=product_image(form.get("name")),
        )
        new_product.save()
        product_data = Product.objects.get(barcode=form.get("barcode"))
        addstats(request.user, product_data, 50)  # Adding 50 points for registering a new product
        request.session['new_product'] = True
        request.session['index_info'] = {"points": 50}

        return redirect('product_info')
    elif request.session['barcode'] != -1: # Collect the barcode that the user has provided
        if not Product.objects.filter(barcode=request.session['barcode']).exists():
            barcode = {'barcode': request.session['barcode']}
            return render(request, 'products/new_product_page.html', barcode) # Present the barcdoe in the page
        else:
            return redirect('index')
    return redirect('index')



def prompt_recycle_product_view(request):
    """
    Web backend for’../product/’ (name ‘product_info’)

    This view handles the viewing of a product that the user has just scanned or previously scanned
    If they have just scanned the product then they will be prompted with a button to recycle the product.
    Below we calculate what bin the product should go into, and then use this data to load the map of bins.

    Return:
        Nothing, but a product is presented to the user
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.session['barcode'] != -1:
        product = Product.objects.get(barcode=request.session['barcode'])
        binType = check_bin(product)
        if request.method == 'POST':
            shortestDistance, close_bin, bin_object = withinRange(request, binType)
            request.session['newHome'] = bin_object.binId  # Directly correlates to a bin
            request.session['shownMap'] = 1
            return redirect("bin_map")
        else:
            data = {"name": product.name,
                    "barcode": request.session['barcode'],
                    "weight": product.weight,
                    "material": product.material,
                    "recycle": product.recycle,
                    "present_button": 1,
                    "binType": binType,
                    "history": Transaction.objects.filter(user=request.user, product=product)[:5],
                    "image": product.image,
                    }
            try:
                if request.session['index_info']:
                    for key, value in request.session['index_info'].items():
                        data.update({key: value})
                    request.session['index_info'] = {}
            except Exception as e:
                pass
    if request.session['pokedex_barcode'] != -1:
        product = Product.objects.get(barcode=request.session['pokedex_barcode'])
        binType = check_bin(product)
        data = {"name": product.name,
                "barcode": request.session['pokedex_barcode'],
                "weight": product.weight,
                "material": product.material,
                "image": product.image,
                "recycle": product.recycle,
                "present_button": 0,
                "binType": binType,
                "history": Transaction.objects.filter(user=request.user, product=product)[:5],
                }

    return render(request, 'products/info_product.html', data)


def check_bin(product):
    """
    Check bin recycle material and recycle data and return the bin type which should go.
    Parameter:
        product: the product being recycled
    Return:
        binType: the type of bin the product goes in
    """
    binType = "General"
    match (product.material, product.recycle):
        case ("Paper", "True"):
            binType = 'Paper'
        case ("Plastic", "True"):
            binType = 'Plastic'
        case ("Cans", "True"):
            binType = 'Cans'
        case ("Glass", "True"):
            binType = 'Glass'
        case ("Plastic", "False"):
            binType = 'General'
        case ("Cans", "False"):
            binType = 'General'
        case ("Non-Recyclable", "False"):
            binType = 'General'
        case ("Glass", "False"):
            binType = 'General'
    return binType


def product_image(name):
    """
    Search and return the image url with the product name given.
    Parameters:
        name: string name of the product
    Return:
        url string of the related product image
    """
    api_key = 'AIzaSyAOqNfgoVAOG4Lnu0-eBPq_vSzQeD7DDNA'
    engine_id = 'd20669afb9bf147dc'
    # Send the request to the Google Custom Search API
    name = urllib.parse.quote(name)
    try:
        url = f"https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&searchType=image&safe=active" % (api_key, engine_id, name)
        with urllib.request.urlopen(url) as response:
            # Parse the response JSON to get the image URL
            data = json.loads(response.read().decode())
            image_url = data['items'][1]['link']
        return image_url
    except:
        return 'https://trolleymate.co.uk/assets/img/error_404.jpeg'
