from django.shortcuts import render, redirect
from bins.models import BinData
from account.models import Goal, Statistic
from shop.models import ShopItems
from home.models import Transaction
from django.db.models import Count, Sum
from django.contrib.auth.models import User


def gamekeeperPage(request):

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
    name = request.POST.get('name')
    description = request.POST.get('description')
    target = request.POST.get('target')
    newGoal = Goal(name=name, description=description, target=target)
    newGoal.save()
    return redirect('gamekeeperPage')


def addShopItem(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    cost = request.POST.get('cost')
    stock = request.POST.get('stock')
    newShopItem = ShopItems(name=name, cost=cost,
                            description=description, stock=stock)
    newShopItem.save()
    return redirect('gamekeeperPage')


def deleteBin(request):
    id = request.POST.get('bin')
    BinData.objects.filter(binId=id).delete()
    return redirect('gamekeeperPage')


def deleteGoal(request):
    id = request.POST.get('goal')
    Goal.objects.filter(goalID=id).delete()
    return redirect('gamekeeperPage')


def deleteShopItem(request):
    id = request.POST.get('shopItem')
    ShopItems.objects.filter(item_id=id).delete()
    return redirect('gamekeeperPage')
