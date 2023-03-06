from django.shortcuts import render, redirect
import urllib.request
import json
from home.models import Statistic, Product, BinData, Transaction, UserGoal
from datetime import datetime
from django.db.models import Q
from home.views import withinRange


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
        request.session['newHome'] = binType
        shortestDistance, close_bin, bin_object = withinRange(request)
        request.session['newHome'] = bin_object  # Directly correlates to a bin
        return redirect("bin_map")
    data = {"name": product.name,
            "weight": product.weight,
            "material": product.material,
            "recycle": product.recycle,
            }
    return render(request, 'info_product.html', data)


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
            return redirect('prompt_product')
            # redirect to product recycle page
        else:
            return redirect('create_product')
    else:
        return render(request, 'BCscanner/Scanner_page.html')


def create_product_view(request):
    # we need to send the user to a page that contains a form
    # Ask the user for the weight and material of the product
    # Then add the product to the database
    #request.session['new_product'] = False
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

        return redirect('prompt_recycle_product_view')
    elif request.session['barcode'] != -1:
        if not Product.objects.filter(barcode=request.session['barcode']).exists():
            barcode = {'barcode': request.session['barcode']}
            return render(request, 'BCscanner/new_product_page.html', barcode)
        else:
            return redirect('index')
    return redirect('index')


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
            request.session['valid'] = -1
            # Call a function that will take in the calculate the points for the user
            # If the product is new add points, this is handle in the create product part
            weight = product_data.weight
            points = round(weight * 122)
            addstats(request.user, product_data, points, weight)  # need to include the product
            update_goal_stat(request.user, product_data)
    except Exception as e:
        print(e)
    return redirect("index")



"""
def recycle_confirm(request):
    # The function that handles recording a transaction
    # Then it shows you to a popup showing what stats you gained on the home_page
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        if not request.session['valid'] == 1:
            return redirect('index')
    except Exception as e:
        print(e)
        return redirect("index")

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
            request.session['valid'] = -1
        # Call a function that will take in the calculate the points for the user
        # If the product is new add points, this is handle in the create product part
        # def addstats(points,kg)
            weight = product_data.weight
            points = round(weight * 122)
            addstats(request.user, product_data, points, weight)  # need to include the product

            # If statement that checks what the products type is and then we set a variable that is litrally
            # var = 'Put in the red bin'

            product_type = product_data.material
            could_recycle = product_data.recycle
            new_home = ""
            match (product_type, could_recycle):
                case ("Paper", "True"):
                    new_home = "My new home is the Paper bin, please help me find my home! :)"
                    binType = 'Paper'
                case ("Plastic", "True"):
                    new_home = "My new home is the Plastic bin, please help me find my home! :)"
                    binType = 'Plastic'
                case ("Cans", "True"):
                    new_home = "My new home is the Cans bin, please help me find my home! :)"
                    binType = 'Cans'
                case ("Glass", "True"):
                    new_home = "My new home is the Glass bin, please help me find my home! :)"
                    binType = 'Glass'
                case ("Plastic", "False"):
                    new_home = "I am non-recyclable, please put me into General Waste :("
                case ("Cans", "False"):
                    new_home = "I am non-recyclable, please put me into General Waste :("
                case ("Non-Recyclable", "False"):
                    new_home = "I am non-recyclable, please put me into General Waste :("
                case ("Glass", "False"):
                    new_home = "I am non-recyclable, please put me into General Waste :("

            # Add points to user goals
            current_user = request.user

            if(binType):
                print(binType)
                thisUserGoals = UserGoal.objects.filter(Q(goalType=binType) & Q(user=current_user))
                for item in thisUserGoals:
                    item.value += 1
                    item.save()
                
                # Delete full goals and add points
                for item in thisUserGoals:
                    if(item.value >= 100):
                        item.delete()
                        points += 100


            data = Transaction.objects.all()[:5]
            data_dict = {
                'Transaction': data,
                'popup': 1,
                'newPoints': 1,
                'product': product_data.name,
                'points': points,
                'newhome': new_home
            }
            print("k")
            print(data_dict)
            return render(request, 'home/index.html', data_dict)
        return redirect('barcode_lookup')
    except Exception as e:
        print(e)
        # They tried to scam us and haven't scanned a product
        return redirect('barcode_lookup')
"""

"""
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
"""

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
    kg = round(kg, 3)
    user_stats.curweek = round((user_stats.curweek + kg), 3)  # change field
    user_stats.curmonth = round((user_stats.curmonth + kg), 3)
    user_stats.curyear = round((user_stats.curyear + kg), 3)
    user_stats.lastRecycle = product
    user_stats.save()  # this will update only


def update_goal_stat(user, product):
    material = product.material
    recyclable = product.recycle
    if recyclable:
        bin_type = material
    else:
        bin_type = 'General Waste'
    user_goals = UserGoal.objects.filter(Q(goalType=bin_type) & Q(user=user))
    for item in user_goals:
        item.value += 1
        item.save()
    # Delete full goals and add points
    for item in user_goals:
        if item.value >= 100:
            item.delete()
            user.points += 100
