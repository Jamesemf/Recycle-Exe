from django.shortcuts import render, redirect
from bins.models import BinData
from account.models import Goal
from shop.models import ShopItems

def gamekeeperPage(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'gamekeeper/gamekeeper.html')


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
    newShopItem = ShopItems(name=name, cost=cost, description=description)
    newShopItem.save()
    return redirect('gamekeeperPage')
