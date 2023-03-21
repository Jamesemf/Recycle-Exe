from django.shortcuts import render, redirect
from home.models import Transaction, TransactionLike
from products.models import Product
from bins.models import BinData
from datetime import datetime, time
from account.views import addstats, update_goal_stat


def scanner_page_view(request):
    """
        Web backend for '../scanner' (name 'barcode_lookup')

        This function returns a redirect to 'product_info' where the user is displayed information about the
        product if the barcode of the item scanned exists within the database. If not, the user is redirected
        to the 'create_product' to enter new information about the item.
    """
    # If the user not log-in, redirect them to login page
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        barcode_product = request.POST.get("barcode")
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

        This function handles if a user successfully reaches a bin after starting a quest. When they do,
        a new transaction is registered on the index page.
    """
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
        print(e)

    #  Retrieve the liked transactions by the current user
    liked = TransactionLike.objects.filter(user=request.user)
    likedList = []
    for x in liked:
        likedList.append(x.transaction_id)

    data = Transaction.objects.all().order_by('-time')[:5]
    data_dict = {
        'Transaction': data,
        'points': points,
        'peakTime': peak,
        'likedList': likedList,
    }

    return render(request, 'home/index.html', data_dict)