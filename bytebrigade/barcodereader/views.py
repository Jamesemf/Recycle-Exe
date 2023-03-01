from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib.request
import json
from home.models import Statistic, Product, BinData, Transaction, UserGoal
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q


def barcode_lookup(request):
    # If the user not log-in, redirect them to login page
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        barcode_product = request.POST.get("barcode")
        # We set the session barcode so that we can then use it in the other areas of the project
        request.session['barcode'] = barcode_product
        if Product.objects.filter(barcode=barcode_product).exists():
            return redirect('recycle_confirm')
            # redirect to product recycle page
        else:
            return redirect('create_product')

    else:
        return render(request, 'BCscanner/Scanner_page.html')


def create_product(request):
    # we need to send the user to a page that contains a form
    # Ask the user for the weight and material of the product
    # Then add the product to the database
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

        return redirect('recycle_confirm')
    elif request.session['barcode']:
        if not Product.objects.filter(barcode=request.session['barcode']).exists():
            barcode = {'barcode': request.session['barcode']}
            return render(request, 'BCscanner/new_product_page.html', barcode)
        else:
            return redirect('index')


# create a function that is called by barcode_lookup() once the whole product shit is done
# This function adds the transaction but doesn't render anything, it is a procedure


def create_product_success(request):
    pass
    # This function is called after a new product is made
    # it present to the user what the product is and the points that they get
    # Then it sends then to recycle_confirm


def recycle_confirm(request):
    # The function that handles recording a transaction
    # Then it shows you to a popup showing what stats you gained on the home_page
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        barcode_product = request.session['barcode']
        bin_data = request.session['bin_data']
        if Product.objects.filter(barcode=barcode_product).exists() \
                and BinData.objects.filter(binId=bin_data).exists():
            product_data = Product.objects.get(barcode=barcode_product)
            user_data = request.user
            cur_time = (datetime.now()).strftime("%H:%M:%S")
            bin_data = BinData.objects.get(binId=bin_data)
            new_transaction = Transaction.objects.create(
                product=product_data,
                user=user_data,
                time=cur_time,
                bin=bin_data,
            )
            new_transaction.save()
            request.session['barcode'] = -1
            request.session['bin_data'] = -1
        # Call a function that will take in the calculate the points for the user
        # If the product is new add points, this is handle in the create product part
        # def addstats(points,kg)
            weight = product_data.weight
            points = round(weight * 122)
            print("h")
            addstats(request.user, product_data, points, weight)  # need to include the product
            print("j")

            # Add points to user goals
            current_user = request.user
            if(bin_data.bin_recycle):
                binType = 'Recycling'
            if(bin_data.bin_paper):
                binType = 'Paper'
            if(bin_data.bin_cans):
                binType = 'Cans'
            if(bin_data.bin_glass):
                binType = 'Glass'
            if(bin_data.bin_plastic):
                binType = 'Plastic'
            else:
                pass

            if(binType):
                thisUserGoals = UserGoal.objects.filter(Q(goalType=binType) & Q(user=current_user))
                for item in thisUserGoals:
                    item.value += points
                
                # Delete full goals and add points
                for item in thisUserGoals:
                    if(item.value >= 100):
                        item.delete()
                        points += 100

            data = Transaction.objects.all()
            data_dict = {
                'Transaction': data,
                'popup': 1,
                'newPoints': 1,
                'product': product_data.name,
                'points': points,

            }
            print("k")
            print(data_dict)
            return render(request, 'home/index.html', data_dict)
        return redirect('barcode_lookup')
    except Exception as e:
        print(e)
        # They tried to scam us and haven't scanned a product
        return redirect('barcode_lookup')


def recycle_result_stats_view(request):
    # The function that shows when user finished recycle
    # The page have stats of points,
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


def addstats(user, product, points: int, kg=0):
    user_stats = Statistic.objects.get(user=user)
    user_stats.points += points
    kg *= 0.09
    print("added points")
    user_stats.curweek += kg  # change field
    print("added curweek")
    user_stats.curmonth += kg
    print("added curmonth")
    user_stats.curyear += kg
    print("added curyear")
    user_stats.lastRecycle = product
    print("added lastRecycle")
    user_stats.save()  # this will update only


