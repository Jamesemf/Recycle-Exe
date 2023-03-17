from django.shortcuts import render, redirect
from .models import Product
from account.views import addstats
from home.views import withinRange
from home.models import Transaction
from django.db.models import Q, Count
from django.http import HttpResponse

def product_dex(request):
    """
    Web backend for '../product/dex/' (name 'product_dex')
    
    This function creates a information page on the number of every product that a user has binned
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

    print(items)
    product_count = {
        'product': items
    }

    return render(request, 'products/pokedex.html', product_count)  #  Render pokedex page

def create_product_view(request):
    """
    This view handles the product creation page. When the user scans a product if the product is not in the database
    we then ask the user to fill out a form about this product. If the request is a get request we load the page containing
    the product form. When a post request occurs we collect the product information and add it to the database.

    The page will automatically contain the barcode which the user has scanned.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST': # Add the product to the database
        form = request.POST
        new_product = Product.objects.create(
            barcode=form.get("barcode"),
            name=form.get("name"),
            weight=float(form.get("weight")) / 1000,
            material=form.get("material"),
            recycle=form.get("recycle")
        )
        new_product.save()

        product_data = Product.objects.get(barcode=form.get("barcode"))
        addstats(request.user, product_data, 50)

        request.session['new_product'] = True

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
    This view handles the viewing of a product that the user has just scanned or previously scanned
    If they have just scanned the product then they will be prompted with a button to recycle the product.
    Below we calculate what bin the product should go into, and then use this data to load the map of bins.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.session['barcode'] != -1:
        product = Product.objects.get(barcode=request.session['barcode'])
        if request.method == 'POST':
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
            shortestDistance, close_bin, bin_object = withinRange(request, binType)
            request.session['newHome'] = bin_object.binId  # Directly correlates to a bin
            print(request.session['newHome'])
            return redirect("bin_map")
        else:
            data = {"name": product.name,
                    "barcode": request.session['barcode'],
                    "weight": product.weight,
                    "material": product.material,
                    "recycle": product.recycle,
                    "present_button": 1,
                    }
    if request.session['pokedex_barcode'] != -1:
        product = Product.objects.get(barcode=request.session['pokedex_barcode'])
        data = {"name": product.name,
                "barcode": request.session['pokedex_barcode'],
                "weight": product.weight,
                "material": product.material,
                "recycle": product.recycle,
                "present_button": 0,
                }
    return render(request, 'products/info_product.html', data)

    # product = Product.objects.get(barcode=request.session['barcode'])
    # if request.method == 'POST':
    #     binType = "General"
    #     match (product.material, product.recycle):
    #         case ("Paper", "True"):
    #             binType = 'Paper'
    #         case ("Plastic", "True"):
    #             binType = 'Plastic'
    #         case ("Cans", "True"):
    #             binType = 'Cans'
    #         case ("Glass", "True"):
    #             binType = 'Glass'
    #         case ("Plastic", "False"):
    #             binType = 'General'
    #         case ("Cans", "False"):
    #             binType = 'General'
    #         case ("Non-Recyclable", "False"):
    #             binType = 'General'
    #         case ("Glass", "False"):
    #             binType = 'General'
    #     shortestDistance, close_bin, bin_object = withinRange(request, binType)
    #     request.session['newHome'] = bin_object.binId  # Directly correlates to a bin
    #     print(request.session['newHome'])
    #     return redirect("bin_map")
    # data = {"name": product.name,
    #         "barcode": request.session['barcode'],
    #         "weight": product.weight,
    #         "material": product.material,
    #         "recycle": product.recycle,
    #         "present_button": 1,
    #         }
    # return render(request, 'products/info_product.html', data)


def database_lookup(request):
    """
    This function is used to check if a product exists in the database already.
    """
    print(request.POST)
    barcode_camera = request.POST.get("barcode")
    print("Value is ", barcode_camera)
    if Product.objects.filter(barcode=barcode_camera).exists():
        print("in db")
        product_data = Product.objects.get(barcode=barcode_camera)
        print(product_data)
    else:
        print("not in db")