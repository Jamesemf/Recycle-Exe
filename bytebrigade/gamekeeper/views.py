from django.shortcuts import render, redirect
from bins.models import BinData
from account.models import Goal, Statistic
from shop.models import ShopItems
from home.models import Transaction
from django.db.models import Count, Sum
from django.contrib.auth.models import User


def gamekeeperPage(request):
    """
    Web backend for’../gamekepper/’ (name ‘gamekeeperPage’)

    This function handles the rendering and viewing of the gamekeeper page. This page allows an Admin to create bins,shop
    items, and gaols for users in the system. All data is collected for the system so that it can be presented in another
    section where the Admin can delete items which they have created.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        goalData = Goal.objects.all()
        shopData = ShopItems.objects.all()
        binData = BinData.objects.all()
        mostRecycled = 0
        mostUsedBin = 0
        if Transaction.objects.exists():
            transactionCount = Transaction.objects.annotate(
                num_transactions=Count('product'))
            mostRecycled = transactionCount.first()
            binCount = Transaction.objects.annotate(
                num_transactions=Count('bin'))
            mostUsedBin = binCount.first()

        regularUsers = User.objects.filter(is_superuser=False)

        totalCarbon = Statistic.objects.aggregate(Sum('carbon'))

        averageCarbon = totalCarbon['carbon__sum']/regularUsers.count()

        totalWeight = 0
        for item in Transaction.objects.all():
            totalWeight += item.product.weight

        data_dict = {'Goals': goalData,
                     'ShopItems': shopData,
                     'Bins': binData,
                     'mostRecycled': mostRecycled,
                     'mostUsedBin': mostUsedBin,
                     'numUsers': regularUsers.count(),
                     'totalCarbon': totalCarbon['carbon__sum'],
                     'averageCarbon': averageCarbon,
                     'totalWeight': totalWeight,
                     'averageWeight': totalWeight/regularUsers.count()}
        return render(request, 'gamekeeper/gamekeeper.html', data_dict)
    return redirect('index')


def addBin(request):
    """
    Web backend for’../gamekepper/addBin’ (name ‘addBin’)

    This function handles the procedure of adding a bin to the system. The bin being added is one specified by the
    admin in the gamekeeper page.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    binId = request.POST.get('binId')
    binName = request.POST.get('binName')
    binLat = request.POST.get('binLat')
    binLong = request.POST.get('binLong')
    binPhoto = request.POST.get('binPhoto')
    bin_general = request.POST.get('bin_general', False)
    bin_recycle = request.POST.get('bin_recycle', False)
    bin_paper = request.POST.get('bin_paper', False)
    bin_cans = request.POST.get('bin_cans', False)
    bin_glass = request.POST.get('bin_glass', False)
    bin_plastic = request.POST.get('bin_plastic', False)
    bin_non_rec = request.POST.get('bin_non_rec', False)
    newBin = BinData(binId=binId, binName=binName, binLat=binLat, binLong=binLong, binPhoto=binPhoto,
                     bin_general=bin_general, bin_recycle=bin_recycle, bin_paper=bin_paper, bin_cans=bin_cans,
                     bin_glass=bin_glass, bin_plastic=bin_plastic, bin_non_rec=bin_non_rec)
    newBin.save()
    return redirect('gamekeeperPage')


def addGoal(request):
    """
    Web backend for’../gamekepper/addGoal’ (name ‘addGoal’)

    This procedure handles the adding of a goal to the system which the admin has specified
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    name = request.POST.get('name')
    description = request.POST.get('description')
    target = request.POST.get('target')
    newGoal = Goal(name=name, description=description, target=target)
    newGoal.save()
    return redirect('gamekeeperPage')


def addShopItem(request):
    """
    Web backend for’../gamekepper/addShopItem’ (name ‘addShopItem’)

    This procedure handles the adding of a shop item to the system which the admin has specified
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    name = request.POST.get('name')
    description = request.POST.get('description')
    cost = request.POST.get('cost')
    stock = request.POST.get('stock')
    newShopItem = ShopItems(name=name, cost=cost,
                            description=description, stock=stock)
    newShopItem.save()
    return redirect('gamekeeperPage')


def deleteBin(request):
    """
    Web backend for’../gamekepper/deleteBin’ (name ‘deleteBin’)

    This procedure handles the removal of a bin object in the system
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    id = request.POST.get('bin')
    BinData.objects.filter(binId=id).delete()
    return redirect('gamekeeperPage')


def deleteGoal(request):
    """
    Web backend for’../gamekepper/deleteGoal’ (name ‘deleteGoal’)

    This procedure handles the deletion of a goal item in the database
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    id = request.POST.get('goal')
    Goal.objects.filter(goalID=id).delete()
    return redirect('gamekeeperPage')


def deleteShopItem(request):
    """
    Web backend for’../gamekepper/deleteShopItem’ (name ‘deleteShopItem’)

    This procedure handles the deletion of a shop item in the system
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return redirect('index')
    id = request.POST.get('shopItem')
    ShopItems.objects.filter(item_id=id).delete()
    return redirect('gamekeeperPage')
