from django.shortcuts import render, redirect
from home.models import Transaction, TransactionLike
from products.models import Product
from bins.models import BinData
from datetime import datetime, time
from account.views import addstats, update_goal_stat
from django.utils import timezone


def scanner_page_view(request):
    """
    Web backend for '../scanner/' (name 'barcode_lookup')
    This view is the back of the scanner page, it to render the barcode scanner and allows the user to scan a barcode. Once
    it has been scanned the view will collect the barcode and allow the system to progress to the next stage of the recycling
    journey.

    Returns:
      If 'POST':
        * Redirect to product information page '../product/' if the barcode scanned match one in the database.
        * Redirect to create product page '../product/create/' if the barcode is new.
      If 'Get':
        * Return the scanner page 'Scanner_page.html'
    """
    # If the user not log-in, redirect them to login page
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        # If the product is in transaction top and there is a 30 minute difference
        # then let the code below run if not render home
        barcode_product = request.POST.get("barcode")
        user_recent = Transaction.objects.filter(user=request.user)[:50]
        for x in user_recent:
            if (x.product.barcode == barcode_product) and (((timezone.now() - x.time).total_seconds())/60 <= 30):
                request.session['index_info'] = {"refuse": "This product was already a recent transaction. Points not added. "}
                return redirect('index')
        # We set the session barcode so that we can then use it in the other areas of the project
        request.session['barcode'] = barcode_product
        request.session['valid'] = 1
        if Product.objects.filter(barcode=barcode_product).exists():
            return redirect('product_info')
            # redirect to product recycle page
        else:
            return redirect('create_product')
    else:
        return render(request, 'BCscanner/Scanner_page.html')


def recycle_confirm_view(request):
    """
    Web backend for '../scanner/recycle/confirm/' (name 'recycle_confirm')
    This function handles if a user successfully reaches a bin after starting a quest. When they do, a new transaction
    is registered on the index page.

    Returns:
      If user not log-in:
        * Redirect to login page '../account/login/'.
      If user have invalid session value 'valid' == -1:
        * Redirect to index page.
      If

    """
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        if not request.session['valid'] == 1:
            return redirect('index')
    except Exception as e:
        pass
        return redirect("index")
    try:
        if request.session['success_recycle'] == -1:
            return redirect("index")
        barcode_product = request.session['barcode']
        bin_id = request.session['newHome']
        if Product.objects.filter(barcode=barcode_product).exists() \
                and BinData.objects.filter(binId=bin_id).exists():
            product_data = Product.objects.get(barcode=barcode_product)
            user_data = request.user
            cur_time = (datetime.now()).strftime("%H:%M:%S")
            bin_data = BinData.objects.get(binId=bin_id)
            new_transaction = Transaction.objects.create(
                product=product_data,
                user=user_data,
                time=cur_time,
                bin=bin_data,
            )
            new_transaction.save()
            request.session['barcode'] = -1
            request.session['valid'] = -1
            request.session['newHome'] = -1

            weight = product_data.weight
            now = datetime.now().time()  # get the current time
            if now >= time(9, 0) and now <= time(15, 0):  #  If peak time points are doubled
                points = round(weight * 122) * 2
                peak = True  # peak is used for rendering messages
            else:
                points = round(weight * 122)
                peak = False
            addstats(request.user, product_data, points, weight)  # need to include the product
            update_goal_stat(request.user, product_data)
    except Exception as e:
        pass
    index_data = {
        "points": points,
        "peakTime": peak
    }
    request.session['index_info'] = index_data
    return redirect('index')