from django.shortcuts import render, redirect
from .models import Product
from account.views import addstats


def create_product(request):
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

        return redirect('recycle_confirm')
    elif request.session['barcode'] != -1:
        if not Product.objects.filter(barcode=request.session['barcode']).exists():
            barcode = {'barcode': request.session['barcode']}
            return render(request, 'BCscanner/new_product_page.html', barcode)
        else:
            return redirect('index')
    return redirect('index')


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