from django.shortcuts import render, redirect
from .models import Product
from account.views import addstats
from home.views import withinRange


def create_product_view(request):
    # we need to send the user to a page that contains a form
    # Ask the user for the weight and material of the product
    # Then add the product to the database
    # request.session['new_product'] = False
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
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
    elif request.session['barcode'] != -1:
        if not Product.objects.filter(barcode=request.session['barcode']).exists():
            barcode = {'barcode': request.session['barcode']}
            return render(request, 'products/new_product_page.html', barcode)
        else:
            return redirect('index')
    return redirect('index')



def prompt_recycle_product_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
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
    data = {"name": product.name,
            "barcode": request.session['barcode'],
            "weight": product.weight,
            "material": product.material,
            "recycle": product.recycle,
            "present_button": 1,
            }
    return render(request, 'products/info_product.html', data)


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