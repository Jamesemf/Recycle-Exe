from django.shortcuts import render, redirect
from home.models import Transaction, TransactionLike
from account.models import Statistic
from bins.models import BinData


# function for the home page backend
def home_view(request):
    """
    Web backend for '../' (name 'index')

    This function intialises / resets session variables and handles POST and GET requests.
    If the request is a GET, then the function retrieves the first 5 entries from the transaction
    model and returns a render to 'index.html' passing a data_dict with the latest transaction
    information.
    If the request is a POST then the user is redirected to the scanner page.
    """
    reset_sessions(request)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if (request.user and Transaction.objects.filter(transaction_id=request.POST.get("trans_id"))):
            trans = Transaction.objects.get(transaction_id=request.POST.get("trans_id"))
            if(not TransactionLike.objects.filter(user=request.user, transaction=trans)):
                trans_like = TransactionLike(user=request.user, transaction=trans)
                trans.likes += 1
                trans_like.save()
                trans.save()
    if BinData.objects.count() == 0:
        bins = [['FORUM-MAIN-OUT', 'Forum main entrance Outside', 50.735666895923100001, -3.533641953682420000, True, True, True, True, True, True, False, False],
                ['IN-1-SWIOT-1', 'Innovation 1 SWIOT 1', 50.737929365592700001, -3.530370602541640000, False, False, False, True, False, True, True, False],
                ['INTO-OUT', 'INTO Outside carpark', 50.7359469093508000018, -3.534357688043370000, True, False, False, True, False, True, True, False],
                ['LAF-MAB', 'Lafrowda MA MB Bin shed', 50.734501000805200001, -3.527055005716390000, True, True, True, True, True, True, False, False],
                ['ROWE', 'Rowe House Bin shed', 50.734291038584400001, -3.528512745930170000, True, True, True, True, True, True, False, False],
                ['XFI-LEC', 'XFI Building Lecture', 50.735844192079400001, -3.529726038441900000, True, False, False, True, False, True, False, False]]
        for item in bins:
            bin_ob = BinData(binId=item[0], binName=item[1], binLat=item[2], binLong=item[3], binPhoto='figures/bins/default.jpg', bin_general=item[4], bin_recycle=item[5], bin_paper=item[6], bin_cans=item[7], bin_glass=item[8], bin_plastic=item[9], bin_non_rec=item[10])
            bin_ob.save()

    #  Retrieve liked transactions by the current user
    liked = TransactionLike.objects.filter(user=request.user)
    likedList = []
    for x in liked:
        likedList.append(x.transaction_id)
    data = Transaction.objects.all().order_by('-time')[:4]

    data_dict = {
        'Transaction': data,
        'likedList': likedList
    }
    try:
        if request.session['index_info']:
            for key, value in request.session['index_info'].items():
                data_dict.update({key: value})
            request.session['index_info'] = {}
    except Exception as e:
        pass
    return render(request, 'home/index.html', data_dict)

# Handles a request for the leaderboard page, ordering the users by their points
def getLeaderboard(request):
    """
    Web backend for '../leaderboard/' (name 'leaderboard')

    This function retrieves all entries from the statistic model ordered by the points
    value in the model. It then returns a render of 'Leaderboard.html' passing the data_dict
    with the model information.
    """
    reset_sessions(request)
    if not request.user.is_authenticated:
        return redirect('login')  #  Redirects to login page if not logged in
    statData = Statistic.objects.all().order_by('-points')
    data_dict = {
        'Statistics': statData,
    }
    return render(request, 'home/Leaderboard.html', data_dict)

def instruction_view(request):
    """
    Web backend for '../abouts/' (name 'instruction')
    Returns:
        * The instruction about page.
    """
    reset_sessions(request)
    return render(request, 'home/about-me.html')


def privacy_policy(request):
    """
    Web backend for '../privacy/' (name 'privacy')
    Returns:
        * The privacy_policy page.
    """
    reset_sessions(request)
    return render(request, 'home/privacypolicy.html')


def license_view(request):
    """
    Web backend for '../license/' (name 'license')
    Returns:
        * The license page.
    """
    reset_sessions(request)
    return render(request, 'home/license.html')


def about_us_view(request):
    """
    Web backend for '../about-us/' (name 'aboutus')
    Returns:
        * The about-us page.
    """
    reset_sessions(request)
    return render(request, 'home/about-us.html')

def reset_sessions(request):
    """
    This function resets all the sessions storing information about the web application use
    """
    request.session['shownMap'] = -1 # Indicates whether the map has been shown with a specific marker
    request.session['barcode'] = -1  # The barcode that the user has scanned
    request.session['newHome'] = -1  # The closest bin
    request.session['valid'] = -1  # If the user has scanned a product, they are valid for the scanner page
    request.session['pokedex_barcode'] = -1 # The barcode of a product selected within the pokedex
    request.session['success_recycle'] = -1  # A session to verify if a user is valid for the addition of stats
